from time import sleep
from ODrive_Ease_Lib import *
from pidev.Joystick import Joystick
from threading import Thread
from time import sleep

import pygame







def startup(od):
    assert od.config.enable_brake_resistor is True, dump_errors(od)

    # Selecting an axis to talk to, axis0 and axis1 correspond to M0 and M1 on the ODrive

    # Basic motor tuning, for more precise tuning follow this guide: https://docs.odriverobotics.com/control.html#tuning
    ax.set_gains()

    if not ax.is_calibrated():
        print("calibrating...")
        # ax.calibrate()
        ax.calibrate_with_current_lim(30)

    print("Current Limit: ", ax.get_current_limit())
    print("Velocity Limit: ", ax.get_vel_limit())

    print("Velocity Tolerance: ", ax.axis.controller.config.vel_limit_tolerance)
    print("Using Velocity Tolerance: ", ax.axis.controller.config.enable_overspeed_error)
    sleep(7)
    ax.set_vel(-3)
    while True:
        if od.get_gpio_states() & 0b00100 == 0:
            ax.set_vel(0)
            ax.set_home()
            print("yes")
            break
        sleep(.1)



def startJoyThread():

    Thread(target=joyMove, daemon=True).start()

def startButtonSense():

    Thread(target=ButtonSense, daemon=True).start()


# def ButtonSense():
#     while True:
#         if joy.get_button_state(5) == 1:
#             ax.set_relative_pos(-5)
#         if joy.get_button_state(6) == 1:
#             ax.set_relative_pos(5)
#         sleep(.1)
def joyMove():
    joy_x_val = 0.0
    joy_y_val = 0.0
    while True:
            joy_y_val = (joy.get_axis('y')*10)
            ax.set_vel(joy_y_val)
            if joy.get_axis('y') == 0:
                ax.set_vel(0)
            if joy.get_button_state(3) == 1:
                ax.set_relative_pos(5)
                sleep(.5)
            if joy.get_button_state(4) == 1:
                ax.set_relative_pos(-5)
                sleep(.5)
            if ax.get_pos() >= 12:
                ax.set_vel(0)
                ax.set_relative_pos(-1)
            if ax.get_pos() <= .5:
                ax.set_vel(0)
                ax.set_relative_pos(.5)
            sleep(.1)

    #def start_joy_thread(self):  # This should be inside the MainScreen Class
            #Thread(target=self.joyController).start()




if __name__ == "__main__":
    od = find_odrive()
    joy = Joystick(0, False)
    ax = ODrive_Axis(od.axis0)
    isJoy = False
    startup(od)
    startJoyThread()
    #startButtonSense()
    dump_errors(od)


