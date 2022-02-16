# Volumio plugin for Domoticz

[Domoticz](https://www.domoticz.com) is free and open-source Home Automation system.

[Volumio](https://volumio.com) is a free and open-source Linux Distribution, designed and fine-tuned exclusively for music playback.

Plugin enables to control Volumio player from Domoticz via network. It uses Volumio Websocket API for communication. If player state is changed out of Domoticz, Volumio notifies the plugin about the change so current status in Domoticz always reflects real status of the player at that time.  

Currently, the following functions are implemented:
- Player control: Play, Pause,Stop
- Volume level control
- Mute control
- Show media being played (Artist - Title)

### Installation

Plugin has been tested with Domoticz 2021.1 and Volumio 2 and Volumio 3. Do not use with Domoticz 2022.1 yet! See _Known issues_ below.
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
- _Port_ - tcp port Volumio is listening on (by default on port 3000).
- click _Add_ button

![image](https://user-images.githubusercontent.com/51033177/152552849-2dd3f0e0-edbb-4b17-bfad-9d7db4cdf39d.png)


Plugin will create 3 devices and shows them in related device tabs (Switches, Utilities):

- Player (Switch device)
- Volume control (Switch device)
- Playing Now (Text device)

![image](https://user-images.githubusercontent.com/51033177/152555243-0362b517-6920-4ba8-878b-31b31ecbb7f7.png)

### Troubleshooting

If you experience any issues with the plugin, enable debugging by setting option Debug to True in your _Volumio_ hw device configuration, re-enable the plugin and check logs in Domoticz Log screen.


### Known issues

- **Domoticz 2022.1** - When the plugin is enabled in debug mode, repeating errors about Acquiring/Releasing lock for the plugin are logged in Domoticz. Patches for Domoticz Plugin System to fix this issue are on the way  [see discussion in Domoticz forum](https://www.domoticz.com/forum/viewtopic.php?p=286906#p286906). 
- **Volumio 3** - Domoticz may throw errors `Error: (ProcessWholeMessage) Unknown Operation Code (x) encountered.` in loghen Websocket frame with special operation code number is received from Volumio. It is not affecting plugin functionality. I'm investigating how to get rid of these errors.