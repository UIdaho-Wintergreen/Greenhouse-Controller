#https://www.piddlerintheroot.com/capacitive-soil-moisture-sensor-v2-0/

import time
import json
import board
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


max_val = None
min_val = None

# Create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# Create the MCP object
mcp = MCP.MCP3008(spi, cs)

# Create single-ended input on channel 0
chan = AnalogIn(mcp, MCP.P0)

baseline_check = input("Is Capacitive Sensor Dry? (enter 'y' to proceed): ")
if baseline_check == 'y':
	max_val = chan.value
	print("------{:>5}\t{:>5}".format("raw", "v"))
	for x in range(0, 10):
		if chan.value > max_val:
			max_val = chan.value
		print("CHAN 0: "+"{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
		time.sleep(0.5)
print('\n')

water_check = input("Is Capacitive Sensor in Water? (enter 'y' to proceed): ")
if water_check == 'y':
	min_val = chan.value
	print("------{:>5}\t{:>5}".format("raw", "v"))
	for x in range(0, 10):
		if chan.value < min_val:
			min_val = chan.value
		print("CHAN 0: "+"{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
		time.sleep(0.5)
config_data = dict()
config_data["full_saturation"] = min_val
config_data["zero_saturation"] = max_val
with open('cap_config.json', 'w') as outfile:
	json.dump(config_data, outfile)
print('\n')
print(config_data)
time.sleep(0.5)
