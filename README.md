# Greenhouse-Controller
A University of Idaho senior design project, 2021. <br>
This is more like proof of concept, and this should be optimized and improved by future teams. <br>
The code in this project should be used with the Wintergreen hardware setup, but may be flexible with other systems. 

## Usage and Description
The main usage of this code is to be able to use multiple sensors and relays to monitor and change conditions in a greenhouse setting. <br>
It utilizes MySQL for internal information storage, Google Sheets for external information storage, and SMS to alert users. 

## Instructions 
See SetupInstructions.txt. 
1. Install necessary libraries and branch code.
2. Edit JSON file config_sensors.json. 

Directory explanations: 

The SensorTests directory contains scripts for individual sensors and functionality.
All of it is combined in controller_SQL.py, controller_manual.py (for sensors, relays at least).

Despite what it seems, controller_manual.py is used for combined testing of sensors and relays.
It is not the most recent, nor will it be the final version used.

Right now, the most "complete" (but in-progress) version is controller_SQL.py, which involves the use of a database.
To set up the database, the current settings are...
  - MySQL database flavor: mariadb
  - Database name: sensor_database
  - Table name: allSensorLog
  - Table entries: datetime(DATETIME), sensornum(CHAR), temperature(FLOAT), humidity(FLOAT), soilsaturation(FLOAT)
