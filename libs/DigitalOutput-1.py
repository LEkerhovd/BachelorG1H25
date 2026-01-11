import RPi.GPIO as GPIO #importerer GPIO Library for kontroll av Rasp Pi pins
import time #importerer tid, kan lage delays etc.

PIN = 7 #velger hvilken pin komponenten er koblet til

GPIO.setmode(GPIO.BCM) #Bruk BroadCom pin nummer
GPIO.setup(PIN, GPIO.IN) #Sett GPIO 7 som en input pin

try: #kjører evig til bruker stopper programn
    while True:
        
        sensor_state = GPIO.input(PIN) #leser digital output fra sensor
        
        if sensor_state ==GPIO.HIGH: #gir utslag om digital output er over grensen fra sensor
            print("ADVARSEL: Temperatur over grensen")
            
        else: 
            print("Temperatur under grensen")
        
        time.sleep(10) #venter 10 sekund før det leser igjen

except KeyboardInterrupt: #CTRL + C stopper programmet
    print("stoppet av bruker")
    
finally:
    GPIO.cleanup()