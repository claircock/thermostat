from tkinter import * 

#enter this at the begining of code when working with tkinter
root = Tk()

# Creating a Label widget --> Define it.
name_of_widget = Label(root, text ="hellow world!")

#shoving it onto the screen ---> now pack it in
name_of_widget.pack()


#Create an event loop <------
#creat our root widget and call it mainloop
root.mainloop()
