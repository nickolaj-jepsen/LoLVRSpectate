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
1. Install python3
2. Install the python dependencies by running `pip install -r requirements.txt`

or wait for me to build a executable. (soon™) 

## Running 
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

## Known issues and TODO
Please check out the issues tab https://github.com/Fire-Proof/LoLVRSpectate/issues
