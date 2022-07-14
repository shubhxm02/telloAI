# telloAI
Letting AI take control of the tello drone

## Presentation

![Flying Selfie Stick](https://user-images.githubusercontent.com/74921415/179098892-280b1f3f-d4f1-4ff9-ba5a-89d37f5f5a94.png)

View the complete presentation [here](https://github.com/shubhxm02/telloAI/blob/main/AIdrone%20presentation.pdf)

## Working

#### Person Detection and Tracking
* Person detection is done using YOLO v3
* Coordinates of the center of the person is set as the target
* Speed Command is sent to the Tello after PID processing

#### Gesture recognition
* Gesture recoginition is done on the hand
* Image/Video/TakeOff/Landing commands are sent to the drone based on the gesture

## Screenshots

![Gesture recognition](https://user-images.githubusercontent.com/74921415/179096725-dedd533f-d320-4153-a9ee-b7ca01e8f762.png)

## Face Tracking demo

[Face Tracking Tello video on youtube](https://youtu.be/1FL3wZyvOJ8)

## Requirements
* DJI Tello drone
* Python 3.7
## Installation

Clone the project

```bash
  git clone https://github.com/shubhxm02/telloAI
```

Go to the project directory

```bash
  cd telloAI
```

Install requirements

```bash
  pip install -r requirements.txt
```


## Running Face Tracker

To run the face tracker program, run the following command

```bash
  python FaceTrackerTello.py
```

## Running Person Tracker

To run the person tracker program, run the following file : `tello_yolo.ipynb`


# Upcoming project preview

[Obstacle Avoidance and Path planning for Tello](https://www.canva.com/design/DAE-4JBoS8w/m8XRCqE6BV8M7DSDp_QfmQ/view?utm_content=DAE-4JBoS8w&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink#1)

[![Presentation](https://user-images.githubusercontent.com/74921415/179099404-5a52898b-d4a2-4ab2-9803-e200c7ced842.png)](https://www.canva.com/design/DAE-4JBoS8w/m8XRCqE6BV8M7DSDp_QfmQ/view?utm_content=DAE-4JBoS8w&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink#1)




