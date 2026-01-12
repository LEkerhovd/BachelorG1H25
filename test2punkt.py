import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        temp_c = float(line)
        print(f"Temperature: {temp_c: .2f} *C")
                 