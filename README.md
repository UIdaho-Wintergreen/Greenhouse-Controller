# Greenhouse-Controller
A UIdaho senior design project, 2021.

Instructions: 
1. Install necessary libraries and branch code.
2. Edit JSON file config_sensors.json. 

Right now, the most "complete" (but in-progress) version is controller_SQL.py, which involves the use of a database.
To set up the database, the current settings are...
  - MySQL database flavor: mariadb
  - Database name: sensor_database
  - Table name: allSensorLog
  - Table entries: datetime(DATETIME), sensornum(CHAR), temperature(FLOAT), humidity(FLOAT), soilsaturation(FLOAT)
