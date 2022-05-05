"""
<plugin key="Volumio" name="Volumio Audiophile Music Player" author="Frantisek Repkovsky" version="0.9.5"
    wikilink="https://github.com/frepkovsky/Domoticz-Volumio-Plugin" externallink="https://volumio.com">
    <description>
        <h2>Volumio Plugin</h2><br/>
        <h4>Favourite Playlists</h4>
        Comma separrated list of your favourite playlists existing in Volumio device.<br/>
            Example:
            <div style="width:700px; padding: .2em;" class="text ui-widget-content ui-corner-all">
                My Mix1, Sting - My Songs, Fun Radio
            </div><br/>
    </description>
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="Port" width="30px" required="true" default="3000"/>
        <param field="Mode1" label="Favourite Playlists" width="700px" default=""/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import json
import secrets
import base64


class BasePlugin:
    volumioConn = None
    reconAgain = 3
    initStateReceived = False
    playerState = 0
    volumeLevel = 100
    mediaPlaying = ""
    playPlaylist = 0
    favPlaylists = []
    isMuted = False
    debug = False

    def onStart(self):
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
            DumpConfigToLog()
            self.debug = True

        if 'volumio' not in Images:
            Domoticz.Image('volumio_icons.zip').Create()

        self.favPlaylists = str(Parameters["Mode1"]).split(",")
        self.favPlaylists = [s.strip() for s in self.favPlaylists]
        self.favPlaylists.insert(0, "")
        if len(self.favPlaylists) > 1:
            playlist_dev_used = 1
        else:
            playlist_dev_used = 0
        playlist_dev_opts = {"LevelActions": (len(self.favPlaylists) - 1) * "|",
                             "LevelNames": "|".join(self.favPlaylists),
                             "LevelOffHidden": "false",
                             "SelectorStyle": "1"}

        if len(Devices) == 0:
            player_dev_opts = {"LevelActions": "0|10|20|30|",
                               "LevelNames": "Off|Play|Pause|Stop",
                               "LevelOffHidden": "true",
                               "SelectorStyle": "0"}
            icon_id = Images["volumio"].ID
            Domoticz.Log("Icon ID: " + str(icon_id))
            Domoticz.Device(Name="Player", Unit=1, TypeName="Selector Switch", Options=player_dev_opts,
                            Image=icon_id, Used=1).Create()
            Domoticz.Device(Name="Now Playing", Unit=2, Type=243, Subtype=19, Image=icon_id, Used=1).Create()
            Domoticz.Device(Name="Volume", Unit=3, Type=244, Subtype=73, Switchtype=7,
                            Image=8, Used=1).Create()
            Domoticz.Device(Name="Play Playlist", Unit=4, TypeName="Selector Switch", Options=playlist_dev_opts,
                            Image=icon_id, Used=playlist_dev_used).Create()
            Domoticz.Log("Devices created.")
        if 1 in Devices:
            self.playerState = Devices[1].nValue
        if 2 in Devices:
            self.mediaPlaying = Devices[2].sValue
        if 3 in Devices:
            self.volumeLevel = Devices[3].sValue
        if 4 in Devices:
            self.playPlaylist = Devices[4].sValue
            Devices[4].Update(nValue=0, sValue=self.playPlaylist, Options=playlist_dev_opts, Used=playlist_dev_used,
                              SuppressTriggers=True)

        self.volumioConn = Domoticz.Connection(Name="volumioConn", Transport="TCP/IP", Protocol="WS",
                                               Address=Parameters["Address"], Port=Parameters["Port"])
        self.volumioConn.Connect()
        Domoticz.Heartbeat(20)   # max 25 seconds
        return True

    def onConnect(self, Connection, Status, Description):
        if Status == 0:
            Domoticz.Log("Connected successfully to: " + Connection.Address + ":" + Connection.Port)
            self.playerState = 1
            send_data = {'URL': '/socket.io/?EIO=3&transport=websocket',
                         'Verb': 'GET',
                         'Headers': {'Host': Parameters["Address"],
                                     'User-Agent': 'Domoticz/1.0',
                                     'Accept': '*/*',
                                     'Accept-Language': 'en-US,en;q=0.5',
                                     'Accept-Encoding': 'gzip, deflate',
                                     'Sec-WebSocket-Version': '13',
                                     'Origin': 'http://' + Parameters["Address"],
                                     'Sec-WebSocket-Extensions': 'permessage-deflate',
                                     'Sec-WebSocket-Key': get_sec_key(),
                                     'Connection': 'keep-alive, Upgrade',
                                     'Pragma': 'no-cache',
                                     'Cache-Control': 'no-cache',
                                     'Upgrade': 'websocket'}}
            Connection.Send(send_data)
        else:
            Domoticz.Log("Failed to connect (" + str(Status) + ") to: " + Connection.Address + ":" + Connection.Port)
            Domoticz.Debug("Failed to connect (" + str(
                Status) + ") to: " + Connection.Address + ":" + Connection.Port + " with error: " + Description)
        return True

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")
        if self.debug:
            DumpWSResponseToLog(Data)
        if "Payload" in Data:
            payload = str(Data["Payload"])
            if payload == '3':
                Domoticz.Debug("Pong packet received.")
            elif payload.startswith('42'):
                Domoticz.Debug("Websocket event packet with data received (42).")
                payload = payload.lstrip('0123456789')
                event = get_event_data(payload)
                if event["type"] == "pushState":
                    Domoticz.Debug("Player status information received (pushState event)")
                    if not self.initStateReceived:
                        self.initStateReceived = True
                    response = event["data"]
                    #for key in response:
                    #    Domoticz.Log("---> " + str(key) + " : " + str(response[key]))
                    try:
                        if response["status"] == 'play':
                            self.playerState = 10
                        elif response["status"] == 'pause':
                            self.playerState = 20
                        elif response["status"] == 'stop':
                            self.playerState = 30
                        artist = ''
                        if "artist" in response:
                            if response["artist"] is not None:
                                artist = response["artist"]
                        title = ''
                        if "title" in response:
                            if response["title"] is not None:
                                title = response["title"]
                        if artist and title:
                            title = artist + ' - ' + title
                        else:
                            title = artist + title
                        if self.playerState == 10:   # Play
                            self.mediaPlaying = title
                        elif self.playerState == 20:   # Pause
                            if title:
                                self.mediaPlaying = "Paused: " + title
                            else:
                                self.mediaPlaying = "Pause"
                        elif self.playerState == 30:   # Stop
                            self.mediaPlaying = "Stopped"
                        self.volumeLevel = response["volume"]
                        if response["mute"]:
                            self.isMuted = True
                        else:
                            self.isMuted = False
                    except KeyError:
                        Domoticz.Error("Some information is missing in pushState event.")
                    self.SyncDevices()
                else:
                    Domoticz.Debug("Unhadled event in event type packet (42): " + event["type"])
            elif payload.startswith('0'):
                Domoticz.Debug("Websocket connection upgrade packet received (0).")
                Domoticz.Log("Websocket connection to Volumio successful.")
                self.volumioConn.Send({'Mask': get_mask(), 'Payload': '42["getState"]'})
                Domoticz.Debug("Player status request sent (getState event).")
            elif payload == '1000':
                Domoticz.Debug("Websocket connection close packet received (1000)")
                Domoticz.Log("Connection closed by Volumio.")
                self.onDisconnect(self.volumioConn)
            else:
                Domoticz.Debug("Unhandled packet type with payload: " + payload)

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log(
            "onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

        Command = Command.strip()
        action, sep, params = Command.partition(' ')
        action = action.capitalize()
        Domoticz.Debug("Command: " + str(Command))
        Domoticz.Debug("action: " + str(action))
        Domoticz.Debug("params: " + str(params))

        if self.volumioConn.Connected():
            if action == 'Set':
                if params.capitalize() == 'Level':
                    if Unit == 1:  # Player control
                        self.playerState = Level
                        if self.playerState == 10:
                            self.volumioConn.Send({'Mask': get_mask(), 'Payload': '42["play"]'})
                        elif self.playerState == 20:
                            self.volumioConn.Send({'Mask': get_mask(), 'Payload': '42["pause"]'})
                        elif self.playerState == 30:
                            self.volumioConn.Send({'Mask': get_mask(), 'Payload': '42["stop"]'})
                        self.SyncDevices()
                    elif Unit == 3:  # Volume Level control
                        self.volumioConn.Send({'Mask': get_mask(), 'Payload': '42["volume",' + str(Level) + ']'})
                    elif Unit == 4:  # Play Playlist
                        self.playPlaylist = Level
                        i = int(int(Level) / 10)
                        playlist = str(self.favPlaylists[i])
                        Domoticz.Log("Playlist: " + playlist)
                        self.volumioConn.Send(
                            {'Mask': get_mask(), 'Payload': '42["replaceAndPlay",{"uri":"playlists/' + playlist +
                             '","title":"' + playlist + '","albumart":null,"service":"mpd"}]'})
            elif action == 'Off' or action == 'On':
                if Unit == 3:  # Mute control
                    if action == 'Off':
                        self.isMuted = True
                        self.volumioConn.Send({'Mask': get_mask(), 'Payload': '42["mute"]'})
                    elif action == 'On':
                        self.isMuted = False
                        self.volumioConn.Send({'Mask': get_mask(), 'Payload': '42["unmute"]'})

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," +
                     Sound + "," + ImageFile)

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        if self.volumioConn is not None:
            self.volumioConn.Send({'Mask': get_mask(), 'Payload': '2'})
            Domoticz.Debug("Ping packet sent")
            # if player status was not received yet since start, request it again
            if not self.initStateReceived:
                Domoticz.Log("Requesting player status.")
                self.volumioConn.Send({'Mask': get_mask(), 'Payload': '42["getState"]'})
        else:
            self.reconAgain -= 1
            if self.reconAgain <= 0:
                if self.volumioConn is None:
                    self.volumioConn = Domoticz.Connection(Name="volumioConn", Transport="TCP/IP", Protocol="WS",
                                                           Address=Parameters["Address"], Port=Parameters["Port"])
                    self.volumioConn.Connect()
                    self.reconAgain = 3
            else:
                Domoticz.Debug("Will try reconnect again in " + str(self.reconAgain) + " heartbeats.")
        return True

    def onDisconnect(self, Connection):
        Domoticz.Log("Volumio device disconnected")
        self.volumioConn = None
        self.playerState = 0
        self.volumeLevel = 100
        self.mediaPlaying = "Off"
        self.isMuted = False
        self.SyncDevices()
        return

    def onStop(self):
        Domoticz.Log("onStop called")
        return True

    def SyncDevices(self):
        # Make sure that the Domoticz devices are in sync (by definition, the device is connected)
        if 1 in Devices:
            UpdateDevice(1, self.playerState, self.playerState)
        if 2 in Devices:
            UpdateDevice(2, 0, self.mediaPlaying)
        if 3 in Devices:
            if self.isMuted:
                UpdateDevice(3, 0, self.volumeLevel)
            else:
                UpdateDevice(3, 2, self.volumeLevel)
        if 4 in Devices:
            UpdateDevice(4, self.playerState, self.playPlaylist)
        return


global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)


def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)


def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)


def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)


def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()


# Generic helper functions


def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return


def DumpWSResponseToLog(httpDict):
    if isinstance(httpDict, dict):
        Domoticz.Debug("WebSocket Details ("+str(len(httpDict))+"):")
        for x in httpDict:
            if isinstance(httpDict[x], dict):
                Domoticz.Debug("--->'"+x+" ("+str(len(httpDict[x]))+"):")
                for y in httpDict[x]:
                    Domoticz.Debug("------->'" + y + "':'" + str(httpDict[x][y]) + "'")
            else:
                Domoticz.Debug("--->'" + x + "':'" + str(httpDict[x]) + "'")


def UpdateDevice(Unit, nValue, sValue):
    if Unit in Devices:
        if Devices[Unit].nValue != nValue or Devices[Unit].sValue != str(sValue):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue))
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
    return


def get_mask():
    return str(secrets.randbits(32))


def get_sec_key():
    return base64.b64encode(secrets.token_bytes(16)).decode("utf-8")


def get_event_data(event: str) -> dict:
    event_dict = {"type": ""}
    try:
        data = json.loads(event)
    except ValueError as e:
        Domoticz.Error("get_event_data(): not in json format")
        return event_dict
    if isinstance(data, list):
        event_dict = {"type": str(data[0]), "data": data[1]}
    else:
        event_dict = {"type": str(data)}
    return event_dict
