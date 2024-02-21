import time
import com.can as com

# import motors.rs_485_port as rs485_com
# import motors.rs_485 as com
# import log_msg.logger as log
from bitstring import BitArray
import math

header = [0xAA, 0xC8]  # The CAN message inside stays the same
trailer = [0x55]

global pre_angle
pre_angle = 0.0


def int_byte(int_data):
    return int_data & 0xFF


def ratio(mid, ang, velo):
    if mid == 1:
        ang *= 6.0
        velo *= 6.0
    elif mid == 2:
        ang *= 6.0
        velo *= 6.0
    elif mid == 3:
        ang *= 6.0
        velo *= 6.0
    elif mid == 4:
        ang *= 6.0
        velo *= 6.0
    elif mid == 5:
        ang *= 9.0
        velo *= 9.0
    elif mid == 6:
        ang *= 9.0
        velo *= 9.0
    else:
        ang *= 30.0
        velo *= 30.0
    return int(ang * 100), int(velo * 100)


def trans(data):
    try:
        if not com.ser.is_open:
            pass
            print("Interface: " + str(com.ser.is_open))
        else:
            com.ser.reset_output_buffer()
            com.ser.write(data)
    except Exception as error:
        com.ser.close()
        print(error)

    while (True):
        # print("wait")
        if (len(com.rx) > 0):
            # print("Hello5")
            if ((com.rx[0] == data[0])):
                break
    time.sleep(0.00296)

    # def write(data):
    # try:
    #     if not interface.is_open:
    #         pass
    #         print("Interface: " + str(interface.is_open))
    #     else:
    #         interface.reset_output_buffer()
    #         interface.write(data)
    # except Exception as error:
    #     interface.close()
    #     print(error)


# def trans_rs485(data):
#     rs485_com.ser.flushOutput()
#     rs485_com.ser.write(data)
#     print(data)

#     while True:
#         # print("wait")
#         if com.rx != None:
#             if len(com.rx) > 0:
#                 # print("Hello5")
#                 if com.rx[0] == data[0]:
#                     break
#         else:
#             print("null")
#             continue

#     # time.sleep(0.1)


# def reset_error(mid):
#     m_data = []
#     m_data.append(0x3E)
#     m_data.append(0x9B)
#     m_data.append(mid)
#     m_data.append(0x00)
#     m_data.append(int_byte(m_data[0] + m_data[1] + m_data[2] + m_data[3]))
#     trans_rs485(m_data)


# def stopmotor(mid):
#     m_data = []
#     m_data.append(0x3E)
#     m_data.append(0x81)
#     m_data.append(mid)
#     m_data.append(0x00)
#     m_data.append(int_byte(m_data[0] + m_data[1] + m_data[2] + m_data[3]))
#     trans_rs485(m_data)


def stopmotor1(mid):
    m_data = []
    m_data.append(0xAA)
    m_data.append(0xC8)
    m_data.append(0x40 + mid)
    m_data.append(0x01)
    # m_data.append(0x80)
    # m_data.append(0x02)
    m_data.append(0x81)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x55)
    trans(m_data)


# def runInc_speed_rs485(mid, ang, velo):
#     chsum = 0
#     degree, speed = ratio(mid, ang, velo)
#     m_data = []
#     m_data.append(0x3E)
#     m_data.append(0xA8)
#     m_data.append(mid)
#     m_data.append(0x08)
#     m_data.append(int_byte(m_data[0] + m_data[1] + m_data[2] + m_data[3]))
#     for i in range(5, 13):
#         if i in range(5, 9):
#             m_data.append(int_byte(degree >> 8 * (i - 5)))
#         if i in range(9, 13):
#             m_data.append(int_byte(speed >> 8 * (i - 9)))
#         chsum += m_data[i]
#     m_data.append(int_byte(chsum))
#     trans_rs485(m_data)


# def runMulti_Angle_speed_rs_485(mid, ang, velo):
#     chsum = 0
#     degree, speed = ratio(mid, ang, velo)
#     if speed == 0:
#         speed = 1
#     m_data = []
#     m_data.append(0x3E)
#     m_data.append(0xA4)
#     m_data.append(mid)
#     m_data.append(0x0C)
#     m_data.append(int_byte(m_data[0] + m_data[1] + m_data[2] + m_data[3]))
#     for i in range(5, 17):
#         if i in range(5, 13):
#             m_data.append(int_byte(degree >> 8 * (i - 5)))
#         if i in range(13, 17):
#             m_data.append(int_byte(speed >> 8 * (i - 13)))
#         chsum += m_data[i]
#     m_data.append(int_byte(chsum))
#     trans_rs485(m_data)


def runMulti_Angle_speed(mid, ang, velo):
    chsum = 0
    degree, speed = ratio(mid, ang, velo)
    if speed == 0:
        speed = 1
    m_data = []
    m_data.append(0xAA)
    m_data.append(0xC8)
    m_data.append(0x40 + mid)
    m_data.append(0x01)
    m_data.append(0xA4)
    m_data.append(0x00)
    # m_data.append(0xf4)
    # m_data.append(0x01)
    for i in range(8, 10):
        m_data.append(int_byte(speed >> 8 * (i - 8)))
    for i in range(10, 14):
        m_data.append(int_byte(degree >> 8 * (i - 10)))
    m_data.append(0x55)
    print(*m_data)
    trans(m_data)


# def incre_position(mid, speed, angle):
#     chsum = 0
#     m_data = []
#     m_data.append(0x3e)
#     m_data.append(0x00+mid)
#     m_data.append(0x08)
#     m_data.append(0xa8)
#     m_data.append(0x00)
#     for i in range (6, 12):
#         if i in range (6,8):
#             m_data.append(int_byte(speed >> 8 * (i - 6)))
#         if i in range(8, 12):
#             m_data.append(int_byte(angle >> 8 * (i - 8)))
#     for i in range(0, 11):
#         chsum += m_data[i]
#     m_data.append(int_byte(chsum))
#     m_data.append(int_byte(chsum >> 8))
#     print(m_data)
#     trans_rs485(m_data)

# def runInc_speed_can(mid, ang, velo):
#     degree, speed = ratio(mid, ang, velo)
#     m_data = []
#     m_data.append(0xaa)
#     m_data.append(0xc8)
#     m_data.append(0x40+mid)
#     m_data.append(0x01)
#     m_data.append(0xa8)
#     m_data.append(0x00)
#     for i in range (6, 12):
#         if i in range (6,8):
#             m_data.append(int_byte(speed >> 8 * (i - 6)))
#         if i in range(8, 12):
#             m_data.append(int_byte(degree >> 8 * (i - 8)))
#     m_data.append(0x55)
#     trans(m_data)


def runInc_speed(mid, velo, ang):
    chsum = 0
    degree, speed = ratio(mid, velo, ang)
    m_data = []
    m_data.append(0xAA)
    m_data.append(0xC8)
    m_data.append(0x40 + mid)
    m_data.append(0x01)
    m_data.append(0xA8)
    m_data.append(0x00)
    # for i in range(6, 13):
    #     if i in range(6, 8):
    #         m_data.append(int_byte(degree >> 8*(i-6)))
    #     if i in range(8, 12):
    #         m_data.append(int_byte(speed >> 8 * (i - 8)))
    for i in range(6, 13):
        if i in range(6, 8):
            m_data.append(int_byte(speed >> 8 * (i - 6)))
        if i in range(8, 12):
            m_data.append(int_byte(degree >> 8 * (i - 8)))
    m_data.append(0x55)
    trans(m_data)
    # speed *= 0.01
    # degree, speed = ratio(mid, ang, velo)
    # data = header + [0x40 + mid, 0x01, 0xa8, 0x00]
    # for i in range(0, 2):
    #     data.append((speed >> 8 * i) & 0xff)
    # for j in range(0, 4):
    #     data.append((degree >> 8 * j) & 0xff)
    # data += trailer
    # trans(data)


def run_speed(mid, velo):
    result = 0
    # chsum = 0
    degree, speed = ratio(mid, 0, velo)
    m_data = []
    m_data.append(0xAA)
    m_data.append(0xC8)
    m_data.append(0x40 + mid)
    m_data.append(0x01)
    m_data.append(0xA2)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    for i in range(8, 12):
        m_data.append(int_byte(speed >> 8 * (i - 8)))
    m_data.append(0x55)
    # print("moving")
    trans(m_data)

# def readAngle(mid):
#     global pre_angle
#     _result = 0
#     result = 0
#     m_data = []
#     m_data.append(0x3E)
#     m_data.append(0x92)
#     m_data.append(mid)
#     m_data.append(0x00)
#     m_data.append(int_byte(m_data[0] + m_data[1] + m_data[2] + m_data[3]))
#     trans_rs485(m_data)
#     if len(com.rx) >= 14:
#         if (com.rx[0] == 0x3E) and (com.rx[1] == 0x92) and (com.rx[2] == mid):
#             for i in range(5, 13):
#                 _result |= com.rx[i] << (8 * (i - 5))
#         s = "{:016b}".format(_result & 0xFFFFFFFF)
#         _resulttemp = BitArray(bin=s).int
#         # print(_resulttemp)
#         result = _resulttemp / 100.0
#         if mid == 1:
#             result /= 9.0
#         elif mid == 2:
#             result /= 9.0
#         elif mid == 3:
#             result /= 9.0
#         else:
#             result /= 30.0
#         pre_angle = result
#         return result
#     else:
#         return pre_angle


def readAngle_can(mid):
    global pre_angle
    _result = 0
    result = 0
    m_data = []
    m_data.append(0xAA)
    m_data.append(0xC8)
    m_data.append(0x40 + mid)
    m_data.append(0x01)
    m_data.append(0x92)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x55)
    trans(m_data)
    if len(com.rx) >= 14:
        if (com.rx[0] == 0xAA) and (com.rx[1] == 0xC8) and (com.rx[2] == 0x40 + mid):
            for i in range(5, 13):
                _result |= com.rx[i] << (8 * (i - 5))
        s = "{:016b}".format(_result & 0xFFFFFFFF)
        _resulttemp = BitArray(bin=s).int
        # print(_resulttemp)
        result = _resulttemp / 100.0
        if mid == 1:
            result /= 9.0
        elif mid == 2:
            result /= 9.0
        elif mid == 3:
            result /= 9.0
        else:
            result /= 30.0
        pre_angle = result
        return result
    else:
        return pre_angle


def readSpeed_can(mid):
    result = 0
    m_data = []
    m_data.append(0xAA)
    m_data.append(0xC8)
    m_data.append(0x40 + mid)
    m_data.append(0x01)
    m_data.append(0x9C)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x55)
    trans(m_data)
    # print(com.rx)
    # print(len(com.rx))
    while (len(com.rx) ==13):
        if com.rx[2] == 0x40+mid:
            result = (com.rx[9] << 8) | (com.rx[8])
            # print(com.rx)
            # print(result/6)
            result /= 6
            result = math.radians(result)
            round_result = round(result, 4)
            # print("result")
            break
        # if ((com.rx[0] == 0xaa) and (com.rx[1] == 0xc8a) and (com.rx[2] == 0x40+mid)):
        #     # print(com.rx)
        #     result = (com.rx[9] << 8) | (com.rx[8])
        #     # print(result)
        #     result /= 6.0

    return round_result


def read_speed_all():
    
    result = []
    for i in range(0, 4):
        result.append(readSpeed_can(i+1))
    return result


def readEncoder_can(mid):
    result = 0
    m_data = []
    m_data.append(0xAA)
    m_data.append(0xC8)
    m_data.append(0x40 + mid)
    m_data.append(0x01)
    m_data.append(0x90)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x55)
    trans(m_data)
    while len(com.rx) == 0:
        print("wait")
        if (com.rx[0] == 0xAA) and (com.rx[1] == 0xC8) and (com.rx[2] == 0x40 + mid):
            result = (com.rx[9] << 8) | (com.rx[8])
    return result


