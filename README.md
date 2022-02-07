# Volumio plugin for Domoticz

[Domoticz](https://www.domoticz.com) is free and open-source Home Automation system.

[Volumio](https://volumio.com) is a free and open-source Linux Distribution, designed and fine-tuned exclusively for music playback.

Plugin enables to control Volumio player from Domoticz via network. It uses Volumio Websocket API for communication. If player state is changed out of Domoticz, Volumio notifies the plugin about the change so current status in Domoticz always reflects real status of the player at that time.  

Currently, the following functions are implemented:
- Player control: Play, Pause,Stop
- Volume level control
- Mute control
- Show media being played (Artist - Title)

#### PLEASE NOTE:

Plugin is still **work in progress!** 

It has been tested and is working fine with **Domoticz 2021.1** and **Volumio 2** and **Volumio 3** 

**Do not use the plugin with Domoticz 2022.1 yet!**

See _Known issues_ below.


### Installation


- Go to Domoticz plugin folder: `cd domoticz/plugins`
- Download plugin: 
`git clone https://github.com/frepkovsky/Domoticz-Volumio-Plugin`
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

If you experience any issues with the plugin, enable debugging by setting option Debug to True in the plugin configuration, re-enable the plugin and check logs in Domoticz Log screen.


### Known issues

- **Volumio 3** - Domoticz may throw errors `Error: (ProcessWholeMessage) Unknown Operation Code (x) encountered.` in log when Websocket frame with special operation code number is received from Volumio. It seems to be rather cosmetic issue only, it is not affecting plugin functionality. I will try to check with Domticz developers how to get rid of these errors. 
- **Domoticz 2022.2** - When the plugin is enabled, repeating errors about Acquiring/Releasing lock for Volumio plugin are logged in Domoticz. It seems to be a problem in Domoticz [see discussion in Domoticz forum](https://www.domoticz.com/forum/viewtopic.php?p=286255#p286255). 
