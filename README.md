# autonomous-rc-car
There is currently a race among the tech giants to develop the first fully autonomous vehicle. [1] This project explores autonomous features on a smaller scale by focusing on radio controlled (RC) vehicles. The Vaterra 2012 Nissan GTR Nismo GT3 V100-C RC car will be connected to both an Arduino Uno and a Raspberry Pi. The Arduino Uno R3 is connected to the Dynamite Waterproof 60A FWD/REV brushed ESC (Electronic Speed Controller), which in turn controls the speed of the Dynamite 540 brushed motor. For steering, the Arduino is also connected to the Spektrum RC S6170 standard digital surface steering servo. The Raspberry Pi 3 model B focuses on converting the Raspberry Pi Camera Module V2’s input into steering instructions for the Arduino to execute; the Raspberry Pi will utilize the OpenCV 3.2.0 software for those calculations. Aside from servo controls, the Arduino Uno will contain five  HC-SR04 ultrasonic sensors to help the vehicle avoid obstacles such as pedestrians and other vehicles.

View Video on YouTube: https://www.youtube.com/watch?v=82_54o01CTQ

![alt text](http://dinocajic.xyz/screenshots/autonomous-rc-vehicle.gif)
