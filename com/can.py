# import motor_handlers as motor
# from motors import movement as move
import serial

import time
from serial import Serial

# Open serial port

FILTER = 15
# counter = 0
ser = serial.Serial()
ser.port = '/dev/ttyUSB0'  # Port 485 for motor
# ser.port = '/dev/ttyUSB2'
ser.baudrate = 115200
ser.timeout = 0.0000001
ser.setDTR(False)
ser.open()
#############################################################
rx = bytes(0)
frame = bytearray()
i = 0
# channel = []
# data = [170, 200, 71, 1, 162, 0, 0, 0, 192, 198, 45, 0, 85]

# while True:
#     ser.write(data)

# def read_from_port(ss):
#     while True:
#         if ser.in_waiting > 0:
#             global rx
#             # global counter
#             rx = ss.read(100)
#             # data = ss.readline().decode().rstrip('\r\n')
#             # value = ser.readline().decode('utf-8').rstrip('\r\n')
#             # ss.flushInput()
#             # if value:
#             #     print(value)\
#             # counter = 0
#             # while counter < 16:
#             # while True:
#             #     value = ser.readline().decode(encoding='ascii', errors='ignore').rstrip('\r\n')
#             #     if value:
#             #         data = value.split(',')
#             #         channel.append(data[:15])
#             #     print(channel)
#         value = ser.readline().decode(encoding='ascii', errors='ignore').rstrip('\r\n')
#         if value
#         # test = int(value)
#         # print("test", x, ":", test)
#         # print("val: ", value)
#         # if value:
#         #     num = int(value)
#         #     print("val: ", value)
#         #     channel.append(num)
#         #     print(counter, ":", channel[counter])
#         #     counter = counter + 1
#             # channel.append(num)  # add data to array
#         # value = ser.readline().decode(encoding='utf-8', errors='ignore').rstrip('\n')
#             # num = int(value)
#             # print(num)
#         # if i % 14 == 0:
#         #     i = 0
#         # print(i, ":", num)
#         # i = i + 1
#         # output_string = str(rx, 'utf-8')
#         # print(output_string)


def read_from_port(ss):
    while True:
        global note1
        while ss.in_waiting > 0:
            global rx

            rx = ss.read(100)
            ss.flushInput()
            # print(*rx)


def frame_recieve(ss):
    # if not ss.open():
    #     print("Serial port not open")
    #     return -1

    
    frame_len = 0
    started = False
    while frame_len < 14:
        try:
            byte = ss.read(1)
            print(byte)
        except serial.serialutil.SerialException as e:
            print("Error reading from serial port: {e}")
        print(len(byte))
        if len(byte) > 0:
            if byte[0] == 0xaa:
                frame.append(byte[0])
                frame_len += 1
                started = True
        else:
            return -1
        
        if started:
            print(frame_len)
            frame.append(byte[0])
            print(frame)
            frame_len += 1

        if frame_len >= 32:
            break

    return frame

