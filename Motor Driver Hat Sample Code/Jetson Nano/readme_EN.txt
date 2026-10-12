/*****************************************************************************
* | File      	:   Readme_CN.txt
* | Author      :   Waveshare team
* | Function    :   Help with use
* | Info        :
*----------------
* |	This version:   V1.0
* | Date        :   2019-06-25
* | Info        :   Here is an English version of the documentation for your quick use.
******************************************************************************/
This file is to help you use this routine.

1. Basic information:
This routine was developed based on the jetson-nano-sd-r32.1.1-2019-05-31 system image and was developed using I2C.
This routine was developed based on the Jetson Nano and the routines were verified on the Jetson Nano;
This routine was verified using the Mtor Driver HAT module.

2. Pin connection:
Pin connections can be viewed in Config.py and will be repeated here:
Motor  =>    Jetson Nano/RPI(BCM)
VIN    ->    6V
GND    ->    GND
SDA    ->    2(SDA)
SDA    ->    3(SDA)


3. Basic use:
Since this project is a comprehensive project, you may need to read the following for use:
python2:
    sudo apt-get install python-smbus
python3:
    sudo apt-get install python3-smbus

Then you need to execute:
python2
    Run: sudo python main.py
python3
    Run: sudo python3 main.py
