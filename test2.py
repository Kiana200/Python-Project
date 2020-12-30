from main_functions import *
from tkinter import *

main = Tk()


main.title("Öppnat fönster")
main.geometry("700x700")
t = Text(main)
lista1 = []

def print_list():
    """ Prints the list. """
    for x in lista1:
        t.insert(END, x  + ' ')
    t.pack()

def que_forward():
    lista1.append("Run forward")

def que_backwards():
    lista1.append("Run backwards")

def que_if():
    lista1.append("If distance < 50")

def if_function_forward():
    print(ir_sensor.get_prox())
    if ir_sensor.get_prox() < 50:
        run_forward()
    else:
        print("Distance is larger than 50")

def if_function_backwards():
    print(ir_sensor.get_prox())
    if ir_sensor.get_prox() < 50:
        run_backwards()
    else:
        print("Distance is larger than 50")




def get_list():
    if lista1[0] == "If distance < 50" and lista1[1] == "Run forward":
        print("yez")
        if_function_forward()
    elif lista1[0] == "If distance < 50" and lista1[1] == "Run backwards":
        if_function_backwards()


lala = Button(main, text="If distance < 50", command=que_if)
lala.pack()

# button_if = Button(main, text="If", command=que_if)
# button_if.pack()

run_forward_button = Button(main, text="Run forward", command = que_forward)
run_forward_button.pack()

run_backwards_button = Button(main, text="Run backwards", command = que_backwards)
run_backwards_button.pack()


button_print = Button(main, text="Print", command=print_list)
button_print.pack()

button_go = Button(main, text="Go", command=get_list)
button_go.pack()
main.mainloop()
