from tkinter import *
from manager import AppManager
from adventure import TextAdventure

root = Tk()
root.resizable(width=False, height=False)


def start_manager(root: Tk):
    manager = AppManager(root)
    manager.add_application(text="Text Adventure", app=TextAdventure)
   

start_manager(root)
root.mainloop()