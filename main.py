import threading
import motors.motor_handlers as motor
import time
from utils import map_range
import com.can as can
from sbus_control import read_sbus_data

M = [0, 0, 0, 0]
controller = None

def read_controller():
    global controller
    while True:
        controller = read_sbus_data()
        time.sleep(0.01)

def mainprog():
    global controller
    while True:
        if controller is not None:
            print(controller)
        lx = 29
        ly = 21.05
        r = 7.5

        if controller is not None and len(controller) == 12:
            Vx = map_range(controller[1], 282, 1722, 10000, -10000)
            Vy = map_range(controller[0], 282, 1722, -10000, 10000)
            omega = map_range(controller[3], 282, 1722, -10000, 10000)

            M[0] = (Vx - Vy - (lx + ly) * omega) * 1 / r
            M[1] = (Vx + Vy + (lx + ly) * omega) * 1 / r
            M[2] = (Vx + Vy - (lx + ly) * omega) * 1 / r
            M[3] = (Vx - Vy + (lx + ly) * omega) * 1 / r

            if abs(Vx) == abs(Vy):  # 45-degree movement
                motor.run_speed(1, M[0])
                motor.run_speed(2, -M[1])
                motor.run_speed(3, -M[2])
                motor.run_speed(4, M[3])
            elif Vy < 0:
                motor.run_speed(1, -M[0])  # Reverse direction
                motor.run_speed(2, M[1])  # Reverse direction
                motor.run_speed(3, M[2])  # Reverse direction
                motor.run_speed(4, -M[3])  # Reverse direction
            elif Vy > 0:
                motor.run_speed(1, -M[0])  # Reverse direction
                motor.run_speed(2, M[1])  # Reverse direction
                motor.run_speed(3, M[2])  # Reverse direction
                motor.run_speed(4, -M[3])  # Reverse direction
            elif Vx < 0:
                motor.run_speed(1, -M[0])  # Reverse direction
                motor.run_speed(2, M[1])  # Reverse direction
                motor.run_speed(3, M[2])  # Reverse direction
                motor.run_speed(4, -M[3])  # Reverse direction
            elif Vx > 0:
                motor.run_speed(1, -M[0])  # Reverse direction
                motor.run_speed(2, M[1])  # Reverse direction
                motor.run_speed(3, M[2])  # Reverse direction
                motor.run_speed(4, -M[3])  # Reverse direction
            elif omega >0:
                motor.run_speed(1, -M[0])  # Reverse direction
                motor.run_speed(2, M[1])  # Reverse direction
                motor.run_speed(3, M[2])  # Reverse direction
                motor.run_speed(4, -M[3])  # Reverse direction
            elif omega <0 :
                motor.run_speed(1, -M[0])  # Reverse direction
                motor.run_speed(2, M[1])  # Reverse direction
                motor.run_speed(3, M[2])  # Reverse direction
                motor.run_speed(4, -M[3])  # Reverse direction
            else:
                motor.run_speed(1, 0)
                motor.run_speed(2, 0)
                motor.run_speed(3, 0)
                motor.run_speed(4, 0)

if __name__ == "__main__":
    thread1 = threading.Thread(target=mainprog)
    thread1.start()

    thread2 = threading.Thread(target=read_controller)
    thread2.start()

    thread3 = threading.Thread(target=can.read_from_port, args=(can.ser,))
    thread3.start()
