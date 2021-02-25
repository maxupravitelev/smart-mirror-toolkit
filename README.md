# smart mirror toolkit
 
## about
 
This kit provides a set of different smart mirror applications. All of them work with the following hardware setup in mind:
- a screen and a camera connected to a machine running python
- a two-way mirror on top of the screen
 
The scripts are also usable without smart mirrors, e.g. for drawing with gestures in front of a webcam.
 

## usage
 
### smart mirror painter
 
This app tracks an object in a specific color range (default: red). The x and y coordinates of the object translate to the x and y coordinates of the brush that is rendered on the canvas.
Move your brush (respectively your red object) to the "save"-area to write the current canvas to file or to the "reset"-area for resetting the canvas.
 
Run `python painter.py` to start.
 
 
### smart mirror tracker
 
Track either faces or a specific color (default: red) and show a white frame around the detected area on the smart mirror. Set the `--track` flag to `face` or `color` accordingly.
 
Optional: If you run this script on a raspberry pi with a gpio motor and mount your camera on top of it, you can add the flag `--gpio true` to move your camera (and/or the whole smart mirror) according to the direction of the tracked object.
 
Run `python tracker.py` to start.
 
 
### smart mirror effects
 
Apply filter effects to the video stream. The default (and currently only) option is computing a threshold version of the input frame.
 
Run `python effects.py` to start.
 
 
## current stage
 
All of the scripts are runnable but still in development at the moment.