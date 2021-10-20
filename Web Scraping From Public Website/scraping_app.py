import os
import tkinter
from subprocess import call
import threading

window = tkinter.Tk()
window.title("GUI")

def clicked():
    threading.Thread(target=call, args=("python Main.py" ,), ).start()

bt = tkinter.Button(window,text="Click Here to start Scraping",command=clicked).pack()

window.geometry('200x150')
window.configure(background='#1A5276')
window.mainloop()