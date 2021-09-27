#!/usr/bin/env python3
import json
import time
import datetime
from time import strftime
import Adafruit_DHT
import board
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO

with open('config_sensors.json') as json_file:
    data = json.load(json_file)
 
# For temp sensor.
sensor_dht11 = Adafruit_DHT.DHT11

# For ADC, soil moisture sensor.
# Create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# Create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# Create the MCP object
mcp = MCP.MCP3008(spi, cs)
# Create single-ended input on channel 0
chan = AnalogIn(mcp, MCP.P0)

# Set up relay pins
GPIO.setmode(GPIO.BCM)
for r in data["relays"]:
    GPIO.setup(r["pin"], GPIO.OUT) 
#GPIO.cleanup()
 
def percent_translation(raw_val, zero_sat, full_sat):
	per_val = abs((raw_val-zero_sat)/(full_sat-zero_sat))*100
	return round(per_val, 3)

response=0
while response!=3:
    print("Choose the following options: ")
    print("1. Check sensor values.")
    print("2. Turn on/ off relays.")
    print("3. Quit.")
    
    response=(int)(input("What would you like to do? "))
    
    if response==1:         
        i=0
        # Get the date, time.
        datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
        print(datetimeWrite)
        
        # Get temp sensors.
        for t in data["temp_sensors"]:
            print("Temperature sensor "+str(i)+"\n")
            if (t["type"]=="dht11"):
                humidity, temp = Adafruit_DHT.read_retry(sensor_dht11, t["pin"])
                while humidity is None and temp is None:    
                    humidity, temp = Adafruit_DHT.read_retry(sensor_dht11, t["pin"])
                L = "Temp={0:0.1f}*C   Humidity={1:0.1f}%".format(temp, humidity)
                print(L)
            else: 
                print("Sensor type specified is not supported.")
            i=i+1
        i=0
        # Get soil sat sensors.            
        for s in data["soil_sensors"]:
            print("Temperature sensor "+str(i)+"\n")
            soil_sat = percent_translation(chan.value, s["zero_saturation"], s["full_saturation"])
            L = "SOIL SENSOR: " + "{:>5}%\t{:>5.3f}".format(soil_sat, chan.voltage)
            print(L)
            i=i+1
    elif response==2:
        GPIO.setmode(GPIO.BCM)
        i=1
        print("Which relay would you like to turn on/ off?")
        for r in data["relays"]:
            print("%d. Relay on pin %d", i, r["pin"])
            i=i+1
        r1_relay=(int)(input("Which relay would you like to choose? Just choose one relay."))
        if (r1_relay<i):
            i=1
            rpin=0
            for r in data["relays"]: 
                if r1_relay==i:
                    rpin=r["pin"]
                else:
                    i=i+1
            # Decide on/off
            r2_relay=(int)(input("Type 1 to turn on, 0 to turn off."))
            if r2_relay==1:
                GPIO.output(rpin, GPIO.HIGH)
                print("Relay on pin %d is on.", rpin)
            elif r2_relay==0:
                GPIO.output(rpin, GPIO.LOW)
                print("Relay on pin %d is off.", rpin)
            else:
                print("Invalid number.")
        else:
            print("Invalid number.")
        #GPIO.cleanup()
    elif response==3:
        break
    else:
        print("Input was not understood. Please try again.")
