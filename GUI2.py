from tkinter import * 

#enter this at the begining of code when working with tkinter
root = Tk()

# Creating a Label widget --> Define it.
name_of_widget_1 = Label(root, text ="hellow world!")
name_of_widget_2 = Label(root, text ="my name is tokyo dicks")

#inside () you tell the program where you want your widget
name_of_widget_1.grid(row=0, column=0)
name_of_widget_2.grid(row=1, column=0)

#Create an event loop <------
#creat our root widget and call it mainloop
root.mainloop()
