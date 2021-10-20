#!/usr/bin/env python3
import json
import time
import datetime
import glob
import pymysql
from time import strftime
import Adafruit_DHT
import board
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os #For environment variables.
import shelve

with open('config_sensors.json') as json_file:
    data = json.load(json_file) 
    
alarm_s = shelve.open("alarm_tracking.db",  flag="c", writeback=True)
 
# For temp sensor.
sensor = Adafruit_DHT.DHT11

# For ADC, soil moisture sensor.
# Create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# Create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# Create the MCP object
mcp = MCP.MCP3008(spi, cs)
# Create single-ended input on channel 0
chan = AnalogIn(mcp, MCP.P0)

# Variables for MySQL
db = pymysql.connect(host="localhost", user="root",passwd="WinterGreen", db="sensor_database")
cur = db.cursor()
    
# For SMS alarm
for e in data["sms_details"]:
    email = e["email_address"]
    pas = e["email_password"]
    
    if (e["phone_carrier"]).lower()=="at&t":
        gateway="@txt.att.net"
    elif (e["phone_carrier"]).lower()=="sprint":
        gateway="@messaging.sprintpcs.com"
    elif (e["phone_carrier"]).lower()=="tmobile":
        gateway="@tmomail.net"  
    elif (e["phone_carrier"]).lower()=="verizon":
        gateway="@vtext.com"  
    elif (e["phone_carrier"]).lower()=="cricket":
        gateway="@sms.mycricket.com"  
    elif (e["phone_carrier"]).lower()=="boostmobile":
        gateway="@myboostmobile.com"  
    
    sms_gateway = e["phone_number"]+gateway 

smtp = "smtp.gmail.com" 
port = 587
 
# Takes in number to compare to upper-lower threshold, sound alarm when pass out of bounds limit.
def check_threshold(num, up_thresh, low_thresh, oob_lim, key, key_name, spec):
    if ((up_thresh<num) or (low_thresh>temp)):
        if (int(key)>=oob_lim):
            send_alarm("Your sensor "+key_name+"'s "+spec+" has been out of bounds beyond the limit set.")
        else:
            return key+1
    else: #Reset if solved.
        return 0

def percent_translation(raw_val, zero_sat, full_sat):
	per_val = abs((raw_val-zero_sat)/(full_sat-zero_sat))*100
	return round(per_val, 3)

def send_alarm(message):
	# This will start our email server
	server = smtplib.SMTP(smtp,port)
	# Starting the server
	server.starttls()
	# Now we need to login
	server.login(email,pas)
	# Now we use the MIME module to structure our message.
	msg = MIMEMultipart()
	msg['From'] = email
	msg['To'] = sms_gateway
	# Make sure you add a new line in the subject
	msg['Subject'] = "WinterGreen Alarm: \n"
	# Make sure you also add new lines to your body
	body = message
	# and then attach that body furthermore you can also send html content.
	msg.attach(MIMEText(body, 'plain'))
	sms = msg.as_string()
	server.sendmail(email,sms_gateway,sms)
	# lastly quit the server
	server.quit()

while True:
    
    humidityList=[]
    tempList=[]
    soilList=[]
    name = "batch1"
    
    # Get the date, time.
    datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    print(datetimeWrite)
    
    # Get temp sensors.
    for i, t in enumerate(data["temp_sensors"]):
        
        key_name = "tempsensor"+str(i)
        if not (key_name in alarm_s.keys()):
            alarm_s[key_name]={"temp": 0, "humid":0}
        
        humidity, temp = Adafruit_DHT.read_retry(sensor, t["pin"])
        while humidity is None and temp is None:    
            humidity, temp = Adafruit_DHT.read_retry(sensor, t["pin"])
        L = "Temp={0:0.1f}*C   Humidity={1:0.1f}%".format(temp, humidity)
        print(L)
        humidityList.append(humidity)
        tempList.append(temp) 
        
        # Check temp threshold.
        alarm_s[key_name]["temp"] = check_threshold(temp, t["temp_upper_threshold"], t["temp_lower_threshold"], t["alarm_when_OOB"], alarm_s[key_name]["temp"], key_name, "temperature")
        alarm_s[key_name]["humid"] = check_threshold(humidity, t["humid_upper_threshold"], t["humid_lower_threshold"], t["alarm_when_OOB"], alarm_s[key_name]["humid"], key_name, "humidity")
        
    # Get soil sat sensors.            
    for i, s in enumerate(data["soil_sensors"]):
        
        key_name = "soilsensor"+str(i)
        if not (key_name in alarm_s.keys()):
            alarm_s[key_name]=0
        
        soil_sat = percent_translation(chan.value, s["zero_saturation"], s["full_saturation"])
        L = "SOIL SENSOR: " + "{:>5}%\t{:>5.3f}".format(soil_sat, chan.voltage)
        print(L)
        soilList.append(soil_sat)
        alarm_s[key_name] = check_threshold(soil_sat, s["upper_threshold"], s["lower_threshold"], s["alarm_when_OOB"], alarm_s[key_name], key_name, "soil saturation")
    
    for h, t, s in zip(humidityList, tempList, soilList):
        sql = ("""INSERT INTO allSensorLog (datetime, sensornum, temperature, humidity, soilsaturation) VALUES (%s,%s,%s,%s,%s)""",(datetimeWrite, name, t, h, s))
        try:
            print("Writing to database...")
            # Execute the SQL command
            cur.execute(*sql)
            # Commit your changes in the database
            db.commit()
            print("Write Complete")
     
        except:
            # Rollback in case there is any error
            db.rollback()
            print("Failed writing to database")
 
    cur.close()
    db.close() 
    alarm_s.close()
    
    send_alarm("Sensor data has been collected at "+datetimeWrite)
    
    break
