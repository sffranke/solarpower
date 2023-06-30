#!/usr/bin/python

#coding: utf8 
import time
import RPi.GPIO as GPIO
# Zaehlweise der Pins festlegen
GPIO.setmode(GPIO.BOARD)
# Pin 22 (GPIO 25) als Ausgang festlegen
GPIO.setup(22, GPIO.OUT)

GPIO.output(22, GPIO.LOW)
# zwei Sekunden warten
time.sleep(0.25)
# Ausgang ausschalten
GPIO.output(22, GPIO.HIGH)
# Ausgaenge wieder freigeben
GPIO.cleanup()
