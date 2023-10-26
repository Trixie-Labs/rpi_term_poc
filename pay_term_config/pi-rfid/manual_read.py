#!/usr/bin/env python
import subprocess
import RPi.GPIO as GPIO
from mfrc522 import BasicMFRC522

reader = BasicMFRC522()
sectors = [11,15]

try:
        id, text = reader.read_sectors(sectors)
        print(id)
        print(text)

finally:
        GPIO.cleanup()
        print("end")

