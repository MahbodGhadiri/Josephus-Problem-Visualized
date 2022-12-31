import tkinter as tk
from tkinter import messagebox
from dialogs import *
from linked_list_view import LinkedListView

# radius of circles
_r = 12

# adding a custom method to Canvas class
def _create_circle(self, x, y, r = _r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

class GUI:
    def __init__(self):
        # set root
        root = tk.Tk()
        self.root = root
        # set title
        root.title("Josephos Problem")
        # set size 
        root.geometry("300x100")
        root.minsize(300,100)
        root.maxsize(300,100)
        # add labels
        self.label = tk.Label(text= "Enter a number:")
        self.label.pack()
        # add entry
        self.entry = tk.Entry(justify= "center")
        self.entry.pack()
        # add button
        self.button = tk.Button(text= "Visualize", command= self.visualize)
        self.button.pack()

        root.mainloop()


    def visualize(self):
        if not self.validateInput():
            return
        # do not let user visualize another solution 
        self.button["state"] = "disable"

        # set window
        window = tk.Toplevel(self.root)
        self.window = window
        window.protocol("WM_DELETE_WINDOW", self.onWindowClose)

        # get input and draw its linked list view
        self.linkedListView = LinkedListView(window, int(self.entry.get()), self.showSurvivor)

        # bind keyboard event
        window.bind("<space>", self.linkedListView.kill_next)
        window.bind("<Return>", self.linkedListView.auto_kill)
        window.bind("s", self.linkedListView.stopThreads )

        #set size
        window.geometry(f"{self.linkedListView.frame_width}x{self.linkedListView.frame_height}")

    def validateInput(self):
        try:
            n = int(self.entry.get())
        except:
            showInvalidInputDialog(self.entry.get())
            self.entry.delete(0, tk.END)
            return False
        if n <=0:
            showInputTooSmallDialog(n)
            self.entry.delete(0, tk.END)
            return False
        if n > 500:
            showInputTooLargeDialog(n)
            self.entry.delete(0, tk.END)
            return False
        return True

    def showSurvivor(self):
        self.linkedListView.showCurrent()
        messagebox.showinfo("Survivor", f"{self.linkedListView.head.data} survives!")
        self.close_window()


    def onWindowClose(self):
        self.linkedListView.closeView()
        self.button["state"] = "normal"
        self.window.destroy()

    def close_window(self):
        self.onWindowClose()