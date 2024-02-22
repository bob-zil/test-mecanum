# # sbus_control.py
import serial
import numpy as np

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.0000001)

def read_sbus_data():
    data = []
    while True:
        byte = ser.read()
        if byte == b'\xAA':
            break
    for i in range(12):
        lowByte = ser.read()
        highByte = ser.read()
        if lowByte is None or highByte is None:
            break
        lowByte = int.from_bytes(lowByte, byteorder='little')
        highByte = int.from_bytes(highByte, byteorder='little')
        value = np.uint16(lowByte | (highByte << 8))
        data.append(value)
    if ser.read() == b'\x55':
        return data
    else:
        return None

# while True:
#     sbus_data = read_sbus_data()
#     if sbus_data is not None:
#         print(sbus_data)

# sbus_control.py
# import serial
# import numpy as np

# ser = serial.Serial('/dev/ttyACM0', 115200)

# def read_sbus_data():
#     data = []
#     while True:
#         byte = ser.read()
#         if byte == b'\xAA':
#             break
#     for i in range(12):
#         lowByte = ser.read()
#         highByte = ser.read()
#         if lowByte is None or highByte is None:
#             break
#         lowByte = int.from_bytes(lowByte, byteorder='little')
#         highByte = int.from_bytes(highByte, byteorder='little')
#         value = np.uint16(lowByte | (highByte << 8))
#         data.append(value)
#     if ser.read() == b'\x55':
#         return data
#     else:
#         return None
