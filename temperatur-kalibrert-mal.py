import serial
import json

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

try:
    while True:
        
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
            
except KeyboardInterrupt:
    ser.close()
    print("Tilkobling avbrutt")