/*****************************************************************************
* | File      	:   Readme_CN.txt
* | Author      :   Waveshare team
* | Function    :   Help with use
* | Info        :
*----------------
* |	This version:   V1.0
* | Date        :   2019-06-25
* | Info        :   在这里提供一个中文版本的使用文档，以便你的快速使用
******************************************************************************/
这个文件是帮助您使用本例程。

1.基本信息：
本例程是基于jetson-nano-sd-r32.1.1-2019-05-31系统镜像而开发的，使用I2C开发。
本例程是基于Jetson Nano进行开发的，例程均在Jetson Nano上进行了验证;
本例程使用Motor Driver HAT模块进行了验证。

2.管脚连接：
管脚连接你可以在Config.py中查看，这里也再重述一次：
Motor  =>    Jetson Nano/RPI(BCM)
VIN    ->    6V
GND    ->    GND
SDA    ->    2(SDA)
SDA    ->    3(SDA)



3.基本使用：
由于本工程是一个综合工程，对于使用而言，你可能需要阅读以下内容:
安装对应的库smbus.
python2
    sudo apt-get install python-smbus
python3
    sudo apt-get install python3-smbus

然后你需要执行：
python2
    运行: sudo python main.py
python3
    运行: sudo python3 main.py
