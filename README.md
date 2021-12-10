# Greenhouse-Controller
-----------------------
A University of Idaho senior design project, 2021. No license, just an open source project utilizing other resources. <br>
This is more like proof of concept, and this should be optimized and improved by future teams. <br>
The code in this project should be used with the Wintergreen hardware setup, but may be flexible with other systems. 

## Usage and Description
------------------------
The main usage of this code is to be able to use multiple sensors and relays to monitor and change conditions in a greenhouse setting. <br>
It utilizes MySQL for internal information storage, Google Sheets for external information storage, and SMS to alert users. 

## Instructions 
-------------------------
See SetupInstructions.txt for additional information/ troubleshooting tips. 
1. Install necessary libraries and clone code.
2. Edit JSON file config_sensors.json. 

To clone the code:
```
git clone https://github.com/UIdaho-Wintergreen/Greenhouse-Controller.git
```

Recommended libraries to install:

```
sudo apt-get install rpi.gpio
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py 
sudo apt-get install mariadb-server php-mysql -y
sudo apt-get install apache2 -y
pip3 install Flask
sudo apt-get install libapache2-mod-wsgi-py3 python-dev
sudo apt-get install python3-pymysql  
pip3 install gspread
pip3 install --upgrade google-api-python-client oauth2client 
```
To get full saturation/ zero saturation values for soil sensor in config_sensors.json, use code specific to your sensor type. 
For capacitive soil moisture sensors v1.2, calibration code to get those values is in SensorTests/soil_sensor_calib.py.

Recommended configuration to set up MySQL database after entering in with sudo mysql –u –p : 
```
CREATE DATABASE sensor_database;
USE sensor_database; 
CREATE TABLE allSensorLog(datetime DATETIME, sensornum CHAR, temperature FLOAT, humidity FLOAT, soilsaturation FLOAT);
``` 
If database or table name is changed, please change the code to match it in controller_SQL.py. 
Make sure to update the password too. 

Recommended crontab configuration to run controller_SQL.py (enter after crontab -e): 
```
*/5 * * * * export GOOGLE_APPLICATION_CREDENTIALS = "(insert path to client_key.json here)"; cd (path to controller_SQL.py directory) && ./controller_SQL.py
```

Directory explanations: 

The SensorTests directory contains scripts for individual sensors and functionality.
All of it is combined in controller_SQL.py, which will be the main executable code.

Right now, the most "complete" (but in-progress) version is controller_SQL.py, which involves the use of a database.
To set up the database, the current settings are...
  - MySQL database flavor: mariadb
  - Database name: sensor_database
  - Table name: allSensorLog
  - Table entries: datetime(DATETIME), sensornum(CHAR), temperature(FLOAT), humidity(FLOAT), soilsaturation(FLOAT)
