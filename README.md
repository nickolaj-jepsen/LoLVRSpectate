# LoLVRSpectate

A tool for spectating League of Legends in VR

A video of an earlier version

[![ ](http://img.youtube.com/vi/VVQz1icy_mI/0.jpg)](http://www.youtube.com/watch?v=VVQz1icy_mI "Video Title")

## Requirements 
* a HTC Vive or another VR headset that support for the [OpenVR](https://github.com/ValveSoftware/openvr) SDK
* VorpX or another program to project League of Legends onto the HMD

#### Optional
* 1 or 2 Motion controllers that support for the [OpenVR](https://github.com/ValveSoftware/openvr) SDK

## Installation
Download the latest release from [here](../../releases)

OR

1. Install python3
2. Install the python dependencies by running `pip install -r requirements.txt`

## Running 
Before running i would recommend that you create a new LoL account, this program is NOT approved by Riot, and by 
modifying the memory it might be caught by some kind of anti-cheat, however, there are multiple other programs that does
 this, and i haven't heard anything about any of their users getting banned.

1. Make sure VorpX is running
2. Make sure the VR environment is active, ie. start SteamVR
3. Start spectating a game or a replay
4. When the game is fully loaded, start the program by running `python run.py`

## Controls
#### Camera
##### Without controllers 
Walk around and admire the landscape
##### With 1 controller
Hold down the trigger and move the controller to readjust the view along the x, y and z axis
##### With 2 controllers 
Hold down one trigger to readjust the view along the x and y axis
Hold down both triggers and "pinch" to zoom and rotate the controllers in relation to each other to rotate the camera

## Recommended settings
These settings are probably far from perfect, buts its the ones i use for testing
#### League of Legends
Reduce the resolution to a lower value, i use 1280x1024
#### VorpX
Enable these two settings in the settings dialog

![image](https://cloud.githubusercontent.com/assets/1039554/15651345/2bc1b912-267f-11e6-9460-574598eecc36.png)

In the ingame settings menu set image zoom to 0.70 and and set the head tracking sensetivity to 0.0 to avoid it moving the cursor

## Known issues and TODO
Please check out the [issues tab](../../issues)

## Disclaimer
LoLVRSpectate isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games 
or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are 
trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.