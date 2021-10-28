# Code/ inspiration taken from the following: 
# https://github.com/yusufcanb/flask-relay-control/blob/master/src/main.py 
# Many others


from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import RPi.GPIO as GPIO
import json
import io
import time
from os import path
from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)
import pymysql 

db = pymysql.connect(host="localhost", user="root",passwd="WinterGreen", db="sensor_database")
#cur = db.cursor() 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "config_sensors.json"))
with open(filepath) as json_file:
    data = json.load(json_file) 
for r in data["relays"]:
    GPIO.setup(r["pin"], GPIO.OUT) 
    GPIO.output(r["pin"], GPIO.LOW) 
    r["state"] = GPIO.input(r["pin"])
    r["status"] = "OFF"

# Retrieve LAST data from database
def getLastData():
    cur = db.cursor() 
    cur.execute("SELECT * FROM allSensorLog ORDER BY datetime DESC LIMIT 1")
    data = cur.fetchone()
    time = str(data[0]) 
    sensor_name = str(data[1])
    temp = data[2]
    hum = data[3]
    soil_sat = data[4] 
    cur.close()
    return time, sensor_name, temp, hum, soil_sat
def getHistData (numSamples):
    cur = db.cursor() 
    cur.execute("SELECT * FROM allSensorLog ORDER BY datetime DESC LIMIT "+str(numSamples)) #"SELECT * FROM allSensorLog LIMIT "+str(numSamples)
    data = cur.fetchall()
    dates = []
    sensor_names = []
    temps = []
    hums = [] 
    soil_sats = []
    for row in reversed(data):
        dates.append(row[0]) 
        sensor_names.append(row[1])
        temps.append(row[2])
        hums.append(row[3])
        soil_sats.append(row[4])
    cur.close()
    return dates, sensor_names, temps, hums, soil_sats
def maxRowsTable():
    cur = db.cursor() 
    cur.execute("SELECT COUNT(*) FROM allSensorLog")
    data = cur.fetchone()  
    maxNumberRows = data[0]
    #maxNumberRows = 0
    #for row in data: 
        #maxNumberRows = maxNumberRows + 1
	#for row in cur.execute("select COUNT(temperature) from allSensorLog"):
		#maxNumberRows=row[0]
    #maxNumberRows = cur.execute("SELECT COUNT(*) FROM allSensorLog")
    cur.close()
    return maxNumberRows
# define and initialize global variables
#global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
    numSamples = 100
# main route
@app.route("/")
def index():
    time, sensor_name, temp, hum, soil_sat = getLastData()
    for r in data["relays"]:
        r["state"] = GPIO.input(r["pin"])
    templateData = {   
        'time' : time, 
        'sensor_name' : sensor_name,
        'temp' : temp,
        'hum' : hum, 
        'soil_sat' : soil_sat, 
        'numSamples' : numSamples, 
        'pins': data["relays"]
	}
    return render_template('index.html', **templateData)
@app.route('/', methods=['POST'])
def my_form_post():
    #global numSamples, request.form['numSamples']
    numSamples = int (request.form['numSamples'])
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)
    time, sensor_name, temp, hum, soil_sat = getLastData()
    templateData = {
        'time' : time, 
        'sensor_name' : sensor_name,
		'temp' : temp,
        'hum' : hum, 
        'soil_sat' : soil_sat, 
        'numSamples' : numSamples
	}
    return render_template('index.html', **templateData)
@app.route("/<changePin>/<action>")
def action(changePin, action):
    # Convert the pin from the URL into an integer.
    changePin = int(changePin) 
    for r in data["relays"]:
        if r["pin"] == changePin: 
            deviceName = r["name"]
            if action == "on":
                # Set the pin high:
                GPIO.output(changePin, GPIO.HIGH)
                # Change the Status
                r["status"] = 'ON'
                # Save the status message to be passed into the template:
                message = "Turned " + deviceName + " on."
            if action == "off":
                GPIO.output(changePin, GPIO.LOW)
                r["status"] = 'OFF'
                message = "Turned " + deviceName + " off."
            if action == "toggle":
                # Read the pin and set it to whatever it isn't (that is, toggle it):
                GPIO.output(changePin, not GPIO.input(changePin))
                message = "Toggled " + deviceName + "."

    # For each pin, read the pin state and store it in the pins dictionary:
    for r in data["relays"]:
        r["state"] = GPIO.input(r["pin"])

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'message': message,
        'pins': data["relays"]
    }
    return render_template('index.html', **templateData)
@app.route('/plot/temp')
def plot_temp():
    times, sensor_names, temps, hums, soil_sats = getHistData(numSamples)
    ys = temps
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Temperature [°C]")
    axis.set_xlabel("Samples")
    axis.grid(True)
    xs = range(numSamples)
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png' 
    return response
@app.route('/plot/hum')
def plot_hum():
    time.sleep(20) #20 seconds
    times, sensor_names, temps, hums, soil_sats = getHistData(numSamples)
    ys = hums
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Humidity [%]")
    axis.set_xlabel("Samples")
    axis.grid(True)
    xs = range(numSamples)
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
@app.route('/plot/soil')
def plot_soil():
    time.sleep(40) #40 seconds
    times, sensor_names, temps, hums, soil_sats = getHistData(numSamples)
    ys = soil_sats
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Soil Saturation [%]")
    axis.set_xlabel("Samples")
    axis.grid(True)
    xs = range(numSamples)
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
if __name__ == "__main__":
   app.run(host='192.168.43.164', port=80, debug=False)
