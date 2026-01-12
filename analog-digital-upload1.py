import serial
import json
import time
import RPi.GPIO as GPIO
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

#Dette skriptet forsøker å kombinere forskjellige skript 

#Arduino

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

#GPIO

PIN = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)


#Google sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
    ]

#laster service konto credentials fra JSON key fil
#authentiserer Raspberry Pi med google
creds = Credentials.from_service_account_file(
    "zooia-1.json",
    scopes=scope
    )

client = gspread.authorize(creds) #autoriserer gspread til å bruke creds

#åpner Google sheet ved bruke av navn
#vær sikker på at regnearket er delt med service konto email
sheet = client.open("Pi Data Logger").sheet1


try:
    while True:
        #Les fra Arduino
        
        line = ser.readline().decode("utf-8", errors="ignore").strip() #les en linje fra arduino
        
        if not line.startswith("{"): # Ignorerer tomme eller feil formaterte linjer
            continue
        
        try:
            
            data = json.loads(line) #analyser JSON string til python ordbok
            
            #henter data
            adc = data["adc"]
            temp_c = data["temp_c"]
            
            #skriv ut resultat
            print(f"ADC: {adc}, Temperatur: {temp_c: .2f} *C")
            
        except (json.JSONDecodeError, KeyError) as e:
            #stopper dårligformatert data
            print(f"Bad data: {line}")
            continue
        
        # Leser fra GPIO
        pin_value = GPIO.input(PIN) #lager variabel pin-value
        
        if pin_value:
            status = "over"
            print("Temperatur over grense")
        
        else:
            status = "under"
            print("Temperatur under grense")
            
        #Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Genererer timestamp for når data blir lastet opp

        #Konsoll output
        print(
            f"{timestamp}, ADC: {adc}, Temperatur: {temp_c:.2f} *C "
            f"Pin: {pin_value}, Status: {status}"
            )
        
        #Last opp til Google sheet
        sheet.append_row([
            timestamp,
            adc,
            round(temp_c, 2),
            pin_value,
            status
            ])
        
        time.sleep(10) #antall sekunder til neste opplasting
        
except KeyboardInterrupt:
        print("Stopper")
        ser.close()
        GPIO.cleanup