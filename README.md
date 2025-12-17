# Volumio plugin for Domoticz

[Domoticz](https://www.domoticz.com) is free and open-source Home Automation system.

[Volumio](https://volumio.com) is a free and open-source Linux Distribution, designed and fine-tuned exclusively for music playback.

Plugin enables to control Volumio player from Domoticz via network. It uses Volumio Websocket API for communication. If player state is changed out of Domoticz, Volumio notifies the plugin about the change so current status in Domoticz always reflects real status of the player at that time.  

Currently, the following functions are implemented:
- Player control: Play, Pause, Stop
- Volume level control
- Mute control
- Now Playing
- Play Playlist

Works with Domoticz version 2022.2 and newer and Volumio version 2/3/4

### Installation

- Connect to Domoticz via ssh 
- Go to Domoticz plugin folder: `cd domoticz/plugins`
- Download plugin: 
`git clone https://github.com/frepkovsky/Domoticz-Volumio-Plugin`
- Restart Domoticz

### Update

- Connect to Domoticz via ssh
- Go to Domoticz plugin folder: `cd domoticz/plugins/Domoticz-Volumio-Plugin`
- Download updates: `git pull`
- Restart Domoticz

### Configuration

From Domoticz web UI, go to _Setup -> Hardware_ and select _Volumio Audiophile Music Player_ from drop-down menu.

Configure plugin:

- _Name_ - name of Volumio hardware device in Domoticz (i.e. Volumio)
- _IP Address_ - IP address of your Volumio device
- _Port_ - tcp port Volumio is listening on (by default on port 3000)
- _Favourite Playlists_ - Comma separrated list of your favourite playlists existing in Volumio device (you can use space after comma for better readability, it is ignored)
- click _Add_ button

![image](https://user-images.githubusercontent.com/51033177/156994675-d5a94703-c397-42c7-8075-9dd1818e5866.png)

Plugin will create 4 devices and shows them in related device tabs (Switches, Utilities):

- Player (Switch device)
- Volume control (Switch device)
- Playing Now (Text device)
- Play Playlist (Switch device)

![image](https://user-images.githubusercontent.com/51033177/156995214-520f192f-b294-46e6-9bd5-108491ce26e6.png)

### Troubleshooting

If you experience any issues with the plugin, enable debugging by setting option Debug to True in your _Volumio_ hw device configuration, re-enable the plugin and check logs in Domoticz Log screen.

