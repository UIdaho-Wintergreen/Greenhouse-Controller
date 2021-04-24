# From adafruit site

import time
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT11(board.D4)
dhtFile = open("dht11_results.txt", "w+")

while True:
	try:
		temperature_c = dhtDevice.temperature
		temperature_f = temperature_c*(9/5)+32
		humidity = dhtDevice.humidity 
		strBuf = "Temp: {:.1f} F / {:.1F} C    Humidity:{}% ".format(temperature_f, temperature_c, humidity)
		print(strBuf)
		dhtFile.write(strBuf)
	except RuntimeError as error:  #DHT can be hard to read.
		print(error.args[0])
		time.sleep(2.0)
		continue
	except Exception as error:
		dhtDevice.exit()
		raise error
	time.sleep(2.0)
