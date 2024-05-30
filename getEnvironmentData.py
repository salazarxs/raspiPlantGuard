import board
import adafruit_dht
import RPi.GPIO as GPIO
import json

# Configurar el sensor de humedad de sustrato
sustrateSensorPin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(sustrateSensorPin, GPIO.IN)

def GetEnvironmentData():
    dhtDevice = adafruit_dht.DHT22(board.D4)
    sensor_soil_value = GPIO.input(sustrateSensorPin)
    
    temperature_c = dhtDevice.temperature
    humidity = dhtDevice.humidity
    sustrate_humidity = sensor_soil_value
    
    data = {
            "hum": humidity,
            "temp": temperature_c,
            "sustrate_humidity": sustrate_humidity
            }
    data_json = json.dumps(data)
    return data_json
