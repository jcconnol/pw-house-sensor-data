import board
import RPi.GPIO as GPIO
import time
import board
import adafruit_dht
import psutil
from facialRec import runFacialRec
import boto3
import os
import json

light_sensor_pin = 26
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(light_sensor_pin, GPIO.IN)

for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(board.D23)

def sendSensorData():
    data_obj = {}
    is_it_dark = isItDark()
    data_obj = getHumidityTemp()
    data_obj["is_dark"] = is_it_dark
    upload_to_s3(data_obj)
    
def upload_to_s3(data_obj):
    session = boto3.Session(
        aws_access_key_id=os.getenv('aws_access_key_id'),
        aws_secret_access_key=os.getenv('aws_secret_access_key')
    )
    
    s3 = session.resource('s3')

    txt_data = json.dumps(data_obj, indent=2).encode('utf-8')

    object = s3.Object('house_data', 'house_data.txt')

    object.put(Body=txt_data)
    
def getHumidityTemp():
    temp = None
    humidity = None
    
    for x in range(10):
        try:
            temp = sensor.temperature
            humidity = sensor.humidity
            return {
                "temp": temp,
                "humidity":humidity
            }
        except RuntimeError as error:
            print("error")
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            sensor.exit()
            raise error
        time.sleep(2.0)
        
    return None
    
def isItDark():
    print(GPIO.input(light_sensor_pin))
    return GPIO.input(light_sensor_pin)

if __name__=='__main__':
    sendSensorData()


