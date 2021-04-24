# Uses a deprecated library, but allegedly works.

import Adafruit_DHT

sensor = Adafruit_DHT.DHT11

pin = 4
i = 0

dhtFile = open("dht11_results.txt", "w")

while (i<11):
	humidity, temp = Adafruit_DHT.read_retry(sensor, pin)

	if humidity is not None and temp is not None:
		L = "Temp={0:0.1f}*C   Humidity={1:0.1f}%".format(temp, humidity)
		print(L)
		i = i+1
		dhtFile.write(L)
	else:
		print("Failed to get reading. Try again.")
dhtFile.close()
