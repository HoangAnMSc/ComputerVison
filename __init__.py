from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Welcome to My Team")
        self.window.geometry('500x500')
        self.window.iconbitmap("ai.ico")
        self.Intro = Label(self.window, text="""An - Anh - Hằng 
                                        """)
        self.Intro.pack()
        self.Button1 = None
        self.my_label =None
    def files(self):
        self.window.filename = filedialog.askopenfilename(initialdir='image/',title="Select File: ",filetypes=(("jpeg files","*.jpg"),("all files","*.*")))
    def Action_B1(self):
        self.Button1 = Button(self.window, text="Select File",command=self.files)
        self.Button1.pack()
        self.my_label= Label(self.window, text="ALL DONE!")
        self.my_label.pack()
    def Action(self):
        self.window.mainloop()




A=App()
A.Action_B1()
A.Action()