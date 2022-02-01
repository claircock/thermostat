# CALCULATOR

from tkinter import * 

#enter this at the begining of code when working with tkinter
root = Tk()
root.title("simple calculator")

# DEFINE ENTRY BOX
e = Entry(root, width=35, borderwidth=5)

# PUT ENTRY BOX ON SCREEN
# use columnspan=3 to have this entry field to span over 3 columns
e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# here we are passing a parametor into a function
# create a varible (current) to make easier
# (number) is our varible name for the value that is passed intto this function
# use e.insert(0, number) to insert whatever number is stored in (number) onto the entry box
# use e.get() to use whatever is currently in the e entry box
# whenever you press a button it will call this function and bring whatever number is stored in (number). first it will assign the digit in the entrybox rightnow to (current), then delete that number in e (the entrybox) then add (current) number to our new number (number) as a string so the digits apper in order
def button_click(number):
	current = e.get()
	e.delete(0, END)
	e.insert(0, str(current) + str(number))

#clear previous number
def button_clear():
	e.delete(0, END)

# use global to pass information from one function to another function
# this function (button_add) will save a number stored in the entrybox and save it as f_num as an interger and make it global so it can be used in other functions THEN delete what you see in the entrybox.
def button_add():
	first_number = e.get()
	global f_num
	f_num = int(first_number)
	e.delete(0, END)


def button_equal():
	second_number = e.get() # save entrybox as second_number
	e.delete(0, END) #just to make sure it is empty now
	e.insert(0, f_num + int(second_number))


#define the button
# Nnormally to pass a parameter into a function we would use
# () but we cant using the Button so we need to use
# command= lambda: button_click() to asign value to button.
# Button() is the 'built in' function we are using,
# button_click (for ex) is just to call our own function
# we made and (4) (for ex) is the value we want to pass into
# function.
button_1 = Button(root, text="1", padx=40, pady=20, command=lambda: button_click(1))
button_2 = Button(root, text="2", padx=40, pady=20, command=lambda: button_click(2))
button_3 = Button(root, text="3", padx=40, pady=20, command=lambda: button_click(3))
button_4 = Button(root, text="4", padx=40, pady=20, command=lambda: button_click(4))
button_5 = Button(root, text="5", padx=40, pady=20, command=lambda: button_click(5))
button_6 = Button(root, text="6", padx=40, pady=20, command=lambda: button_click(6))
button_7 = Button(root, text="7", padx=40, pady=20, command=lambda: button_click(7))
button_8 = Button(root, text="8", padx=40, pady=20, command=lambda: button_click(8))
button_9 = Button(root, text="9", padx=40, pady=20, command=lambda: button_click(9))
button_0 = Button(root, text="0", padx=40, pady=20, command=lambda: button_click(0))
button_add = Button(root, text="+", padx=39, pady=20, command=button_add)
button_equal = Button(root, text="=", padx=91, pady=20, command=button_equal)
button_clear = Button(root, text="clear", padx=80, pady=20, command=button_clear)

# put the buttons on the screen
button_1.grid(row=3, column=0)
button_2.grid(row=3, column=1)
button_3.grid(row=3, column=2)

button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)

button_7.grid(row=1, column=0)
button_8.grid(row=1, column=1)
button_9.grid(row=1, column=2)

button_0.grid(row=4, column=0)
button_add.grid(row=5, column=0)
button_equal.grid(row=5, column=1, columnspan=2)
button_clear.grid(row=4, column=1, columnspan=2)



#Create an event loop <------
#creat our root widget and call it mainloop
root.mainloop()

