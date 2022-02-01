# THIS PROGRAM IS ALL YOU NEED TO TAKE INFO IN AND OUTPUT INFO

from tkinter import * 

#enter this at the begining of code when working with tkinter
root = Tk()


# to make an entry box for user use:
# to change size of entry box add with=50
# you again change the color by adding fg="white" or anything
# change border with  by adding borderwith=5 (KINDA DUMB)
# use:  e.insert(0, "Enter your name: ") to have a text in the box for user to see before typing
e = Entry(root)
e.insert(0, "Enter your name: ")
e.pack()

# make a function to run with a button
def my_click():
	#define the thing
	# now to get a useful entry from user use: text=e.get()
	my_function = Label(root, text="hellow " + e.get())
	# put the thing on the screeen
	my_function.pack()

#define the thing
# use state=DISABLED to make an unclickable button
# use padx=50  (or anything)  to make a wider button
# use pady=50 to make a taller button 
# use command=my_click to exicute that function after click
# WHEN using command=my_click DO NOT USE () like you normally would when calling a function it will not work, just leave it alone
# use fg="blue" to change color (fg means forground color)
# use bg="color" to change background color
myButton = Button(root, text="ehter your name:  ", command=my_click)



#now put it on the screen
# use myButton.pack() to force on screen
# use myButton.grid(row=0, column=0) to make it apper in a format you want 
myButton.pack()

#Create an event loop <------
#creat our root widget and call it mainloop
root.mainloop()

