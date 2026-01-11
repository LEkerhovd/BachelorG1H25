# Denne virker, men krever gspread som jeg ikke får installert utenfor virtual environment
import RPi.GPIO as GPIO
import time
from datetime import datetime #bruk for å genrere timestamp for hver rad med data

import gspread
from oauth2client.service_account import ServiceAccountCredentials #importerer credentials handler for Google service konto

# GPIO setup

PIN = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)


#Google sheets setup
#Definer tillatelsene (scope) scriptet trenger
# - Tilgang til Google Sheets
# - Tilgang til Google Drive (kreves for å åpne regnearket)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
    ]

#laster service konto credentials fra JSON key fil
#authentiserer Raspberry Pi med google
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "zooia-1.json",
    scope
    )

client = gspread.authorize(creds) #autoriserer gspread til å bruke creds

#åpner Google sheet ved bruke av navn
#vær sikker på at regnearket er delt med service konto email
sheet = client.open("Pi Data Logger").sheet1

#main loop
try:
    while True:
        pin_value = GPIO.input(PIN) #lager variabel pin-value
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Genererer timestamp for når data blir lastet opp

        
        if pin_value:
            status = "over"
            print("Temperatur over grense")
        
        else:
            status = "under"
            print("Temperatur under grense")

        sheet.append_row([timestamp, pin_value, status]) #lager en ny rad i regnearket
        
        time.sleep(10) 
                
except KeyboardInterrupt:
    GPIO.cleanup()
                
                