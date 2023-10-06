

# INSTRUCTIONS

Hello there!
This is a HeadSpin Speedtest SandBox module. It consists of 2 python scripts, which automate the `SpeedTest by Ookla` app on android and iOS headspin devices. Anybody can run these python scripts on their system having any of the operating systems given below:

* macOS
* Linux
* Windows 

Just flow the below steps to try it out.


## PREREQUISITE   
The commands used in this file can be executed using one of the Command Line Interface (CLI) given below.

* Command prompt for Windows
* Terminal for macOS and Linux


### STEP 1 : Python3 Installation 
Check for Python3 is available using the command

> python3 --version

It will return a python version if python is installed properly on your system. Otherwise, follow the steps to install python.


####		For macOS :
Install Homebrew using the command.
> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Homebrew or simply brew is a command line tool to install packages on mac.

Now install Python3 using the command.
> brew install python


####     	For Linux :
Execute the below command to get an updated list of packages from the Internet (This is executed to get the latest python version). 
> sudo apt update

Now install python3 using the below command.
> sudo apt install python3 python3-pip build-essential python3-dev

####    	For Windows : 
Download the latest python3 installer from [here](https://www.python.org/downloads/).
Then open the installer and follow the steps in the installation wizard to install python3.

[Here](https://www.digitalocean.com/community/tutorials/install-python-windows-10) is a reference in case you are stuck somewhere while installing.


### STEP 2 : Install required Python Modules 
Once the python3 is successfully installed, We need to install 2 python modules, that are used in the SandBox script.

* requests
* appium-python-client

Just execute the below command to install these 2 modules.
> pip3 install Appium-Python-Client==2.6.1  requests==2.28.1


### STEP 3 : Install SpeedTest by Ookla App on Device
Before executing the python script, make sure the Speedtest app is installed on the device. Which is used to execute the scripts. Use the below link to identify the correct SpeedTest app and install it on the device if it is not installed.

* [Play Store Link](https://play.google.com/store/apps/details?id=org.zwanoo.android.speedtest&hl=en_IN&gl=US)
* [App Store Link](https://apps.apple.com/us/app/speedtest-by-ookla/id300704847)

## Executing the Automation Scripts. 

Make sure that you are inside the `Speedtest_SandBox` directory(the extracted folder) on your CLI. Otherwise, python won't be able to find the scrips.

Use the `cd <path to the Speedtest_SanBox directory>` command to change the directory to the correct one if you are not inside the correct directory.



####        Syntax For a single Android Runs:
>python3 speed\_test\_android_SB.py --udid \<device udid\>  --url \<web driver url\>

####        Syntax For a single iOS Runs:
> python3 speed\_test\_ios\_SB.py --udid \<device udid\>  --url \<web driver url\>

####        Syntax For repeated iOS Runs:   

>python3 speed\_test\_ios\_SB.py --udid \<device udid\>  --url \<web driver url\> --repeat \<count\>

#### Example Runner Command:
> python3 speed\_test\_ios\_SB.py --udid 00008020-000D14A03608003A  --url https://dev-in-blr-0.headspin.io:3012/v0/********************/wd/hub  --repeat 4

* `speed_test_ios_SB.py` is the name of the python automation script.
* `00008020-000D14A03608003A` is the device id(udid) of the device used for executing the script. Which is given as the argument value for `--udid`
* `https://dev-in-blr-0.headspin.io:3012/v0/********************/wd/hub --repeat 4` is the web driver url(gets from the automation tab in the Headspin remote control UI). Which is given as the value for `--url`
* `4` is the repeat count. Which is given as the value for `--repeat`. Here the script will be executed 4 times sequentially. This is an optional argument.
