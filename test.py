from part2 import *
from tkinter import *

main = Tk()
root = Tk()

main.title("Öppnat fönster")
main.geometry("700x700")


def leftKey(event):
    print("Left key pressed")
    command=turn_degree_two_track(20)

def rightKey(event):
    print("Right key pressed")
    command=turn_degree_two_track(-20)

def upKey(event):
    print("Up key pressed")
    command=run_forward()

def downKey(event):
    print("downKey pressed")
    command=run_backwards()

def create_window():
    window = Toplevel(root)

frame = Frame(main, width=100, height=100)
main.bind('<Left>', leftKey)
main.bind('<Right>', rightKey)
main.bind("<Up>", upKey)
main.bind("<Down>", downKey)
b = Button(root, text="Start manual control", command=create_window())
b.pack()
frame.pack()

main.mainloop()
root.mainloop()

# from tkinter import *
# import queue
# q = queue.Queue()
#
# for i in range(5):
#     q.put(i)
#
# while not q.empty():
#     print(q.get())
