import machine
import urequests 
from machine import Pin, I2C
import network
from dht import DHT22

import socket
from time import sleep
import gc
gc.collect()
from bmp085 import BMP180


HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = '2JMJKEHA60T7CBD4'  
 
ssid = 'Realme 1'
password = '123456789'
 
# Configure Pico W as Station
sta_if=network.WLAN(network.STA_IF)
sta_if.active(True)
 
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
     pass
print('network config:', sta_if.ifconfig()) 
 
while True:
    sleep(5)
    
    #DHT22
    pin = Pin(5, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT22(pin)
    sensor.measure()
    t  = sensor.temperature()
    h = sensor.humidity()
    #t  = (sensor.temperature())
    #h = (sensor.humidity())
    
    print( "DHT")
    print("Temperature: {}".format(t))
    print("Humidity: {}".format(h))
    
    
    #BMP180
    led_onboard = Pin(2, Pin.OUT)
    i2c = I2C(0, sda = Pin(21), scl = Pin(22), freq = 1000000)
    bmp = BMP180(i2c)
    bmp.oversample = 2
    bmp.sealevel = 101325
    #temp = bmp.temperature
    press = bmp.pressure
    altitude = bmp.altitude
    #temp_f= (temp * (9/5) + 32)
    print( "BMP")
    print( "The Pressure Value {:.2f}".format(press))
    print("The Altitude Value{:.2f}".format(altitude))
    #print("The Temperature Value{:.2f}".format(temp))
    
    
    
    dht_readings = {'field1':t, 'field2':h, 'field3':press, 'field4':altitude} 
    request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = dht_readings, headers = HTTP_HEADERS )  
    request.close() 
    print(dht_readings) 

