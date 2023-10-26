#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import BasicMFRC522

writer = BasicMFRC522()
sectors = [11, 15]

try:
        text = input('New data:')
        print("Now place your tag to write")
        writer.write_sectors(text, sectors)
        print("Written")
finally:
        GPIO.cleanup()
