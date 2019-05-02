import RPi.GPIO as GPIO
import time
import signal
import sys
import json

from RabbitMQMqttClient import RabbitMQMqttClient
GPIO.setwarnings(False)
# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
pinTrigger = 18
pinEcho = 24

rabbitMQMqttClient = RabbitMQMqttClient("cs616", "cs616", "192.168.0.103", 1883, None)

def close(signal, frame):
    print("\nTurning off ultrasonic distance detection...\n")
    GPIO.cleanup() 
    sys.exit(0)

signal.signal(signal.SIGINT, close)

# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)

while True:
    # set Trigger to HIGH
    GPIO.output(pinTrigger, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.0001)
    GPIO.output(pinTrigger, False)

    startTime = time.time()
    stopTime = time.time()

    # save start time
    while 0 == GPIO.input(pinEcho):
        startTime = time.time()

    # save time of arrival
    while 1 == GPIO.input(pinEcho):
        stopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = stopTime - startTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    print ("Distance: %.1f cm" % distance)
    
    msg = {
        "counter": 0,
        "micros": 0,
        "proximity": round(distance, 2),
    }
    
    rabbitMQMqttClient.publish("arduino/sensors/A4", json.dumps(msg))
    
    time.sleep(1)
    
    if not(rabbitMQMqttClient.isConnected):
        rabbitMQMqttClient.connect()
