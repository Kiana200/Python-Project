from api.ev3 import Ev3
from tkinter import *
from queue import *
from main_functions import *


""" Opens the main window with different buttons"""

base = Tk()

menubar = Menu(base)
menubar.add_command(label="Talk with Intruder", command=talk)
menubar.add_command(label="Choose modes", command=modes)
menubar.add_command(label="Live state", command=live_state)
menubar.add_command(label="Quit!", command=base.destroy)
menubar.add_command(label="Build state", command=build_state)


base.config(menu=menubar)
