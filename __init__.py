from tkinter import *
from tkinter import filedialog
from HangScanner.main import * 
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
        self.pathname1 =None
        self.webcamFeed=False
        self.Button2=None
    def files(self):
        self.window.filename = filedialog.askopenfilename(initialdir='image/',title="Select File: ",filetypes=(("jpeg files","*.jpg"),("all files","*.*")))
        self.pathname1=self.window.filename
        print(self.pathname1)
        if self.pathname1:
            self.webcamFeed=False
            RUNNNNNNN(self.webcamFeed,self.pathname1)
    def file2(self):
        RUNNNNNNN(True,self.pathname1)

    def Action_B1(self):
        self.Button1 = Button(self.window, text="Select File",command=self.files)
        self.Button1.pack()
    def Action_B2(self):
        self.Button2 = Button(self.window, text="Bật camera",command=self.file2)
        self.Button2.pack()
        
    def Action(self):
        self.window.mainloop()




A=App()
A.Action_B1()
A.Action_B2()
A.Action()