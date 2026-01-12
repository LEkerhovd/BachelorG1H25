import serial

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) #åpner serial kobling

try:
    while True:
        line = ser.readline().decode("utf-8").strip()
        
        if not line: #hopper over tomme linjer
            continue
        
        if "," not in line: # sikrer forventet CSV format
            print(f"Ignored line:{line}")
            continue
        
        parts = line.split(",")
        
        if len(parts) !=2:
            print(f"Malformed data: {line}")
            continue
        
        raw = int(parts[0])
        voltage = float(parts[1])
        #if line:
         #   raw, voltage = line.split(",")
            
            #raw = int(raw)
           # voltage = float(voltage)
        print(f"Raw ADC: {raw} | Voltage: {voltage: .2f} V")
            
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed")

