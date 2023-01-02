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
        root.geometry("300x130")
        root.minsize(300,130)
        root.maxsize(300,130)
        # add labels
        self.label = tk.Label(text= "Enter number of people in the circle:")
        self.label.grid(row = 0, column=0, sticky= tk.W)
        self.label = tk.Label(text= "Enter number of k:")
        self.label.grid(row = 3, column=0, sticky= tk.W)
        # add entry
        self.nEntry = tk.Entry(justify= "center")
        self.nEntry.grid(row= 2, column=0)
        self.kEntry = tk.Entry(justify= "center")
        self.kEntry.grid(row= 4, column=0)
        # add button
        self.button = tk.Button(text= "Visualize", command= self.visualize)
        self.button.grid(row= 5, column=0 )

        root.mainloop()


    def visualize(self):
        if not self.validateInput(self.nEntry):
            return
        if not self.validateInput(self.kEntry):
            return
        # do not let user visualize another solution 
        self.button["state"] = "disable"

        # set window
        window = tk.Toplevel(
            self.root,
            bg="#0ba7b3",
        )
        self.window = window
        window.protocol("WM_DELETE_WINDOW", self.onWindowClose)

        # get input and draw its linked list view
        self.linkedListView = LinkedListView(window, int(self.nEntry.get()), int(self.kEntry.get()), self.showSurvivor)

        # bind keyboard event
        window.bind("<space>", self.linkedListView.kill_next)
        window.bind("<Return>", self.linkedListView.auto_kill)
        window.bind("s", self.linkedListView.stopThreads )

        #set size
        window.geometry(f"{self.linkedListView.frame_width}x{self.linkedListView.frame_height}")

    def validateInput(self, entry: tk.Entry):
        try:
            n = int(entry.get())
        except:
            showInvalidInputDialog(entry.get())
            entry.delete(0, tk.END)
            return False
        if n <=0:
            showInputTooSmallDialog(n)
            entry.delete(0, tk.END)
            return False
        if n > 500:
            showInputTooLargeDialog(n)
            entry.delete(0, tk.END)
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