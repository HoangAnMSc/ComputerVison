from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
class App:
    def __init__(self, RunFunction):
        self.window = Tk()
        self.window.title("Welcome to My Team")
        self.window.geometry('500x500')
        self.window.iconbitmap("ai.ico")

        #Add logo
        self.logo = Image.open('logo.png')
        self.logo = ImageTk.PhotoImage(self.logo)
        self.Intro = Label(image = self.logo)
        self.Intro.image = self.logo
        self.Intro.grid(column=1, row=0)

        self.Intro.pack()
        self.Button1 = None
        self.my_label =None
        self.pathname1 =None
        self.webcamFeed=False
        self.Button2=None
        self.RUNN = RunFunction

    def files(self):
        self.window.filename = filedialog.askopenfilename(initialdir='Image/',title="Select File: ",filetypes=(("jpeg files","*.jpg"),("all files","*.*")))
        self.pathname1=self.window.filename
        print(self.pathname1)
        if self.pathname1:
            self.webcamFeed=False
            self.RUNN(self.webcamFeed,self.pathname1)

    def file2(self):
        self.RUNN(True,self.pathname1)

    def Action_B1(self):
        self.Button1 = Button(self.window, text="Select File",command=self.files, font='Raleway', bg = '#00c2cb', fg='white', height= 1, width= 10)
        self.Button1.pack(pady=10)

    def Action_B2(self):
        self.Button2 = Button(self.window, text="Turn on Camera",command=self.file2, font='Raleway', bg = '#00c2cb', fg='white', height= 1, width= 10)
        self.Button2.pack()
        
    def Action(self):
        self.window.mainloop()




