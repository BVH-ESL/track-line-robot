import serial
from time import sleep
speed = 100
command = "("+str(speed)+","+str(speed)+"):"
ser = serial.Serial('/dev/ttyACM0', 
					baudrate = 9600,
					bytesize=serial.EIGHTBITS,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					timeout=0.1)
sleep(1.0)
while ser.read():
	pass
sleep(1.0)

while True:
	ser.write(command)
	sleep(3)
	ser.write("(0,0):")
	sleep(2)
ser.close()
