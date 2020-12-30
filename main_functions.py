from api.ev3 import Ev3
import time
import random
from tkinter import *
from queue import Queue

test_unit = Ev3("192.168.0.115")

motor_a = test_unit.add_motor("A")
motor_b = test_unit.add_motor("B")
motor_c = test_unit.add_motor("C")

touch_sensor = test_unit.add_sensor(1, 'touch')
color_sensor = test_unit.add_sensor(4, 'color')
ir_sensor = test_unit.add_sensor(3,"IR")
prox_value = ir_sensor.get_prox()
ambient_value = color_sensor.get_ambient()
reflect_value = color_sensor.get_reflect()
rgb_values = color_sensor.get_rgb()
color_value = color_sensor.get_color()

def run_forward():
    """ Drives straight ahead and stops after two seconds """
    motor_b.run_forever(100, run=False)
    motor_c.run_forever(100, run=False)
    test_unit.start_motors(["B", "C"])
    time.sleep(2)
    test_unit.stop_all_motors()

def run_forward_slow():
        """ Drives straight ahead a bit slower than run_forward and stops after
         two seconds """
        motor_b.run_forever(20, run=False)
        motor_c.run_forever(20, run=False)
        test_unit.start_motors(["B", "C"])
        test_unit.stop_all_motors()

def run_backwards():
    """ Drives backwards and stops after two seconds """
    motor_b.run_forever(-100, run=False)
    motor_c.run_forever(-100, run=False)
    test_unit.start_motors(["B", "C"])
    time.sleep(1)
    test_unit.stop_all_motors()

def run_forever():
    """ Drives staright ahead """
    motor_b.run_forever(100, run=False)
    motor_c.run_forever(100, run=False)
    test_unit.start_motors(["B", "C"])

def turn_degree_one_track(degree):
    """ Turns given degrees using one motor """
    if degree<0:
        motor_b.run_position_limited(100, degree*8, brake="hold")
    else:
        motor_c.run_position_limited(100, degree*8, brake="hold")

def turn_degree_two_track(degree):
    """ Turns given degrees using two motors """
    motor_b.run_position_limited(80, degree*5, run=False, brake="hold")
    motor_c.run_position_limited(-80, degree*5, run=False, brake="hold")
    test_unit.start_motors(["B", "C"])

def peacefull_mode():
    """Starts moving forward until the sensor is pressed, then it makes a sound,
    turns in random direction and continues forward until it hits something else.
    If it sees a blue light (colur_value = 2), it will enter guard_mode"""

    motor_b.run_forever(70, run=False)
    motor_c.run_forever(70, run=False)
    test_unit.start_motors(["B", "C"])
    color_value = color_sensor.get_color()
    if touch_sensor.is_pressed():
        test_unit.stop_all_motors()
        time.sleep(2)
        test_unit.play_wav("hello_cutie")
        turn_degree_two_track(random.randint(0,360))
        time.sleep(2)


def run_guardmode():
    """ If the colour value is 2 Megatron will do a dance and then go into
        guardmode or else it will keep being in peacefull_mode"""
    while True:
        color_value = color_sensor.get_color()
        if color_value != 4:
            if color_value == 2:
                test_unit.stop_all_motors()
                happy_dance()
                time.sleep(2)
                guard_mode()
            else:
                peacefull_mode()
        else:
            break

def run_peaceful():
    """ If the colour value is 6 Megatron will do a dance and then go into
        peacefull_mode or else it will keep being in guardmode"""
    while True:
        color_value = color_sensor.get_color()
        if color_value != 4:
            if color_value == 6:
                moonwalk()
                time.sleep(1)
                peacefull_mode()
            else:
                guard_mode()
        else:
            break

def guard_mode():
    """ Drives slowly in a random direction in the square. If an enemy appears
    it calls the function attack()."""

    print("I am now in guardmode")
    motor_b.run_forever(30, run=False)
    motor_c.run_forever(30, run=False)
    test_unit.start_motors(["B", "C"])
    if color_value == 1:
        test_unit.stop_all_motors()
        time.sleep(2)
        run_backwards()
        time.sleep(2)
        turn_degree_two_track(random.randint(90,270))
        time.sleep(2)
    if ir_sensor.get_prox() <= 50:
        attack()


def happy_dance():
    """Does a happy little dance"""
    turn_degree_one_track(180)
    turn_degree_one_track(-180)

def attack():
    """ When the distance is smaller than 50 it will ask the enemy to go away
    and then start a countdown. If the enemy goes away the countdown stops and
    Megatron resumes guard_mode. If the eneemy doesnt move it fires 2 balls
    against it."""
    distance = ir_sensor.get_prox()
    if distance <= 50:
        test_unit.stop_all_motors()
        test_unit.speak("Please go away")
        time.sleep(1)
        distance = ir_sensor.get_prox()
        if distance <= 50:
            test_unit.speak("Three")
            time.sleep(1)
            distance = ir_sensor.get_prox()
            if distance <= 50:
                test_unit.speak("Two")
                time.sleep(1)
                distance = ir_sensor.get_prox()
            if distance <= 50:
                test_unit.speak("One")
                time.sleep(1)
                distance = ir_sensor.get_prox()
            if distance <= 50:
                test_unit.stop_all_motors()
                time.sleep(1)
                test_unit.speak("Attack!")
                weapon()
                distance = ir_sensor.get_prox()
            if distance <= 50:
                turn_degree_two_track(180)
                time.sleep(1)
                hide()
            else:
                guard_mode()

def hide():
    """ Activated when the intruder doesnt go away after it has been attacked.
    It flees towards a wall, then runs along it until it finds a corner and
    stays there """
    motor_b.run_forever(100, run=False)
    motor_c.run_forever(100, run=False)
    test_unit.start_motors(["B", "C"])
    distance = ir_sensor.get_prox()
    print(distance)
    if distance < 30:
        distance = ir_sensor.get_prox()
        while distance < 40:
            turn_degree_two_track(10)
            time.sleep(0.2)
            distance = ir_sensor.get_prox()
            print(distance)
        else:
            while not touch_sensor.is_pressed():
                motor_b.run_forever(80, run=False)
                motor_c.run_forever(80, run=False)
                test_unit.start_motors(["B", "C"])
            else:
                test_unit.stop_all_motors()
    else:
        hide()

def weapon():
    """ Pulls back a lever and then pushes it forward making a ball shoot
    straight forward"""
    motor_a.run_forever(100)
    time.sleep(2)
    test_unit.stop_all_motors()

def moonwalk():
    """ A dance thats a little different than happy_dance"""
    for i in range(5):
        motor_b.run_position_limited(-40, 100)
        motor_c.run_position_limited(-60,100)
        time.sleep(0.5)
        motor_b.run_position_limited(-60, 100)
        motor_c.run_position_limited(-40,100)

    turn_degree_two_track(360)

def talk():
    """ Takes and entry from user and sends a command to make the robot
    say the input"""
    root2 = Tk()

    def speak():
        message = entry_1.get()
        label_2 = Label(root2)
        test_unit.speak(message)

    label_1 = Label(root2, text='Message to intruder: ')
    entry_1 = Entry(root2)
    button_1 = Button(root2, text='Send message to intruder!',  command=speak)
    button_2 = Button(root2, text="QUIT", fg="red", command=root2.destroy)
    label_1.grid(row=0, column=0)
    entry_1.grid(row=0, column=1)
    button_1.grid(row=1, column=0)
    button_2.grid(row=1,column=1)

    root2.mainloop()

def modes():
    """ Opens up a GUI with buttons where one can select prefered mode"""

    root = Tk()

    w = Label(root, text="Hello, world!")
    w.pack()
    root.geometry("500x500")
    t = Text(root)

    def change_color():
        root.configure(background='green')
        root.update()
        run_peaceful()
        if color_sensor.get_color() == 2:
            root.configure(background="red")
            root.update()
            run_guardmode()

    def change_color2():
        root.configure(background="red")
        root.update()
        run_guardmode()

    button_peacefull = Button(root, text="Peacefull mode", command= change_color)
    button_peacefull.pack()

    button_guard = Button(root, text="Guard Mode", command=change_color2)
    button_guard.pack()

    button_attack = Button(root, text="Attack", command=attack)
    button_attack.pack()

    button_quit = Button(root, text="Quit", command=root.destroy)
    button_quit.pack()

    root.mainloop()

def live_state():
    """ Opens up a GUI with different control buttons for live control"""
    root = Tk()

    root.geometry("500x500")

    button_happy = Button(root, text="Happy Dance", command=happy_dance)
    button_happy.pack()

    button_left = Button(root, text="Turn Left",\
                    command= lambda degree = 90: turn_degree_two_track(degree))
    button_left.pack()

    button_right = Button(root, text="Turn Right",\
                    command= lambda degree = -90: turn_degree_two_track(degree))
    button_right.pack()

    button_forward = Button(root, text="Forward", command=run_forward)
    button_forward.pack()

    button_backward= Button(root, text="Backwards", command=run_backwards)
    button_backward.pack()

    button_quit = Button(root, text="Quit", command=root.destroy)
    button_quit.pack()

    root.mainloop()

def build_state():
    """ Opens up a GUI where the user can put functions into a que and when
    desired execute all functions from the cue. It can also show what is
    currently in the que."""
    root = Tk()

    root.geometry("500x500")

    l = []
    t = Text(root)

    def run():
        """ Goes thru the list with given arguments and calls the right
        function for that argument"""

        for i in l:
            if i == 'Turn left':
                turn_degree_two_track(90)
            elif i == 'Turn right':
                turn_degree_two_track(-90)
            elif i == 'Run forward':
                run_forward()
            elif i == 'Run backwards':
                run_backwards()
        l.clear()
        t.delete(1.0, END)

    def print_list():
        """ Prints the list. """
        for x in l:
            t.insert(END, x  + ' ')
        t.pack()

    def que_forward():
        """ Adds 'Run forward to the list' """
        l.append('Run forward')

    def que_backwards():
        """ Adds 'Run backwards to the list' """
        l.append('Run backwards')

    def que_left():
        """ Adds 'Turn left to the list' """
        l.append('Turn left')

    def que_right():
        """ Adds 'Turn right to the list' """
        l.append('Turn right')

    button_left = Button(root, text="Turn Left", command= que_left)
    button_left.pack()

    button_right = Button(root, text="Turn Right", command= que_right)
    button_right.pack()

    button_forward = Button(root, text="Forward", command=que_forward)
    button_forward.pack()

    button_backward= Button(root, text="Backwards", command = que_backwards)
    button_backward.pack()

    button_run = Button(root, text="Run", command=run)
    button_run.pack()

    button_print = Button(root, text="Print", command=print_list)
    button_print.pack()

    button_quit = Button(root, text="Quit", command=root.destroy)
    button_quit.pack()

    root.mainloop()

def line_follow():
    """ Follows the line and adjusts depending on the color value """
    while True:
        if color_sensor.get_rgb()[0] > 20 and color_sensor.get_rgb()[0] < 70:
            run_forward_slow()
        elif color_sensor.get_rgb()[0] >= 70:
            turn_degree_two_track(10)
        elif color_sensor.get_rgb()[0]<= 20:
            turn_degree_two_track(-10)

def line_spin():
    """ Turns around after a while and calls line_follow """
    a = 0
    while a < 100:
        if a == 10:
            turn_degree_two_track(-100)
            time.sleep(2)
            while color_sensor.get_rgb()[0] > 20:
                motor_b.run_forever(25)
            line_follow()
        elif color_sensor.get_rgb()[0] > 20 and color_sensor.get_rgb()[0] < 70:
            run_forward_slow()
        elif color_sensor.get_rgb()[0] >= 70:
            turn_degree_two_track(-10)
        elif color_sensor.get_rgb()[0]<= 20:
            turn_degree_two_track(10)

        a += 1
