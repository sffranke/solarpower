#!/usr/bin/python

#coding: utf8 
import time
import RPi.GPIO as GPIO
# Zaehlweise der Pins festlegen
GPIO.setmode(GPIO.BOARD)
# Pin 18 (GPIO 24) als Ausgang festlegen
GPIO.setup(18, GPIO.OUT)

GPIO.output(18, GPIO.LOW)
# zwei Sekunden warten
time.sleep(0.25)
# Ausgang ausschalten
GPIO.output(18, GPIO.HIGH)
# Ausgaenge wieder freigeben
GPIO.cleanup()


