import threading
import motors.motor_handlers as motor
import time
from utils import map_range
#from utils import map_range
import com.can as can
from sbus_control import read_sbus_data  # import the function

global reload
M = [0, 0, 0, 0]
pwm_ = [0, 0, 0, 0]
v = [0, 0, 0, 0]
deltaT = 0.02

controller = None

def read_controller():
    global controller
    while True:
        controller = read_sbus_data()  # read data from sbus_control.py
        time.sleep(0.01)  # sleep for 10ms

def mainprog():
    global reload
    global controller
    while True:
        if controller is not None:
            print(controller)
        lx = 29
        ly = 21.05
        r = 7.5


        if controller is not None and len(controller) == 12:
            #print(controller[0])
            Vx = map_range(controller[1], 282, 1722, -10000, 10000)
            Vy = map_range(controller[0], 282, 1722, -10000, 10000)
            omega = map_range(controller[3], 282, 1722, -10000, 10000)
            print("Vx: ", Vx)
            print("Vy: ", Vy)
            print("omega: ", omega)

            M[0] = (Vx - Vy - (lx + ly) * omega) * 1 / r
            M[1] = (Vx + Vy + (lx + ly) * omega) * 1 / r
            M[2] = (Vx + Vy - (lx + ly) * omega) * 1 / r
            M[3] = (Vx - Vy + (lx + ly) * omega) * 1 / r
            print("M0: ", M[0])
            print("M1: ", M[1])
            print("M2: ", M[2])
            print("M3: ", M[3])

            if Vy < 0:
                motor.run_speed(1, M[0])
                motor.run_speed(2, -M[1])
                motor.run_speed(3, -M[2])
                motor.run_speed(4, M[3])
            elif Vy > 0:
                motor.run_speed(1, M[0])
                motor.run_speed(2, -M[1])
                motor.run_speed(3, -M[2])
                motor.run_speed(4, M[3])
            elif Vx < 0:
                motor.run_speed(1, M[0])
                motor.run_speed(2, -M[1])
                motor.run_speed(3, -M[2])
                motor.run_speed(4, M[3])
            elif Vx > 0:
                motor.run_speed(1, M[0])
                motor.run_speed(2, -M[1])
                motor.run_speed(3, -M[2])
                motor.run_speed(4, M[3])
            elif omega >0:
                motor.run_speed(1, M[0])
                motor.run_speed(2, -M[1])
                motor.run_speed(3, -M[2])
                motor.run_speed(4, M[3])
            elif omega <0 :
                motor.run_speed(1, M[0])
                motor.run_speed(2, -M[1])
                motor.run_speed(3, -M[2])
                motor.run_speed(4, M[3])

            else:
                motor.run_speed(1, 0)
                motor.run_speed(2, 0)
                motor.run_speed(3, 0)
                motor.run_speed(4, 0)

# def test():
#     motor.run_speed(3,0)


if name == "main":
    thread1 = threading.Thread(target=mainprog)
    thread1.start()

    thread2 = threading.Thread(target=read_controller)
    thread2.start()

    thread3 = threading.Thread(target=can.read_from_port, args=(can.ser,))
    thread3.start()
