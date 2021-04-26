import time
import json
import board
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

soilFile = open("soil_results.txt","w+")
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
	
with open("cap_config.json") as json_data_file:
	config_data = json.load(json_data_file)
# print(json.dumps(config_data))
def percent_translation(raw_val):
	per_val = abs((raw_val- config_data["zero_saturation"])/(config_data["full_saturation"]-config_data["zero_saturation"]))*100
	return round(per_val, 3)
if __name__ == '__main__':
	print("----------  {:>5}\t{:>5}".format("Saturation", "Voltage\n"))
	while True:
		try:
			L = "SOIL SENSOR: " + "{:>5}%\t{:>5.3f}".format(percent_translation(chan.value), chan.voltage)
			print(L)
			soilFile.write(L)
		except Exception as error:
			raise error
		except KeyboardInterrupt:
			print('exiting script')
			soilFile.close()
		time.sleep(1)
