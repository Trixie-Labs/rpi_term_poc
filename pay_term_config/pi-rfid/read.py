#!/usr/bin/env python
import subprocess
import RPi.GPIO as GPIO
from mfrc522 import BasicMFRC522

reader = BasicMFRC522()
sectors = [11,15]

while True:
        try:
                print("start read...")
                id, text = reader.read_sectors(sectors)
                print(id)
                private_key = text.replace("\x00", "")
                subprocess.run(
                ["python3", "/home/vitor/pay_term_config/pi-rfid/transact.py", private_key]
)
        finally:
                GPIO.cleanup()
                print("end")

