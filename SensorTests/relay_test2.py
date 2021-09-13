import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.OUT) 
   
GPIO.output(21, GPIO.HIGH)
time.sleep(2)
GPIO.output(21, GPIO.LOW)
time.sleep(2)


# Reset GPIO settings
GPIO.cleanup()