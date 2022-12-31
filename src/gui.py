import tkinter as tk
from tkinter import messagebox
from constructs.linked_list import generate_linked_list, Node
from math   import sin, cos, radians
import threading
import time

_r = 12
#adding a custom method to Canvas class
def _create_circle(self, x, y, r = _r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

class GUI:
    def __init__(self):
        #set root
        root = tk.Tk()
        self.root = root
        #set title
        root.title("Josephos Problem")
        root.geometry("300x300")
        root.minsize(300,100)
        root.maxsize(300,100)
        #add labels
        self.label = tk.Label(text="Enter a number:")
        self.label.pack()
        #add entry
        self.entry = tk.Entry(justify="center")
        self.entry.pack()
        #add button
        self.button = tk.Button(text="Visualize", command=self.visualize)
        self.button.pack()
        #add state
        self.windowIsOpen = False
        self.isKilling = False
        self.thread_num = 0
        self.pause = False

        root.mainloop()


    def visualize(self):
        try:
            n = int(self.entry.get())
        except:
            self.showInvalidInputDialog(self.entry.get())
            self.entry.delete(0, tk.END)
            return
        if n<=0:
            self.showInputTooSmallDialog(n)
            self.entry.delete(0, tk.END)
            return
        if n> 500:
            self.showInputTooLargeDialog(n)
            self.entry.delete(0, tk.END)
            return
        self.button["state"] = "disable"
        #set window
        window = tk.Toplevel(self.root)
        self.window = window
        self.windowIsOpen = True
        window.protocol("WM_DELETE_WINDOW", self.onWindowClose)
        # bind keyboard event
        window.bind("<space>", self.kill_next)
        window.bind("<Return>", self.auto_kill)
        window.bind("p", self.pauseThreads )

        self.n = n
        self.drawLinkedList()
        #set size
        window.geometry(f"{self.frame_width}x{self.frame_height}")
        self.showCurrent()

    def kill_next(self, event = None)->Node:
        if(self.isKilling):
            return
        self.isKilling = True
        current = self.head
        canvas = self.canvas
        self.showCurrent()
        canvas.itemconfig(self.getCircleId(current.data), fill="green")
        canvas.itemconfig(self.getCircleId(current.next.data), fill="red")
        current.next = current.next.next
        self.head = current.next
        canvas.itemconfig(self.getCircleId(self.head.data), fill="blue")
        if(current.next == current.next.next):
            self.showSurvivor()
            return False
        self.isKilling = False
        return True

    def kill_all(self):
        keepKilling = True
        while keepKilling and self.windowIsOpen and not self.pause:
            keepKilling = self.kill_next()
            time.sleep(0.5)
        self.thread_num -= 1

    def auto_kill(self, event):
        self.pause = False
        if self.thread_num < 9:
            threading.Thread(target= self.kill_all).start()
            self.thread_num += 1

    def close_window(self):
        self.window.destroy()

    def drawLinkedList(self):

        n = self.n
        self.theta = 360/n
        '''
            r = sin(theta/2) * R => R = r/sin(theta/2)  
            The above formula is used to calculate r_middle value (r_middle is R in above formula)
            r_middle is the radius of the invisible circle, on which the center of the small circles are draw.
            theta is the angle between to circles
            r is the radius of small circles
        '''
        self.r_middle = float((_r+1) / sin(radians(self.theta/2))) if float((_r+1) / sin(radians(self.theta/2)))>50 else 50
        self.frame_width = int(2*self.r_middle + 200)
        self.frame_height = self.frame_width 
        #add canvas
        self.canvas = tk.Canvas(
            self.window,
            width=self.frame_width-10,
            height=self.frame_height-20,
            scrollregion=(0,0,self.frame_width-10, self.frame_height-20)
        )
        canvas = self.canvas
        # add horizontal scrollbar
        hbar=tk.Scrollbar(self.window, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.TOP,fill=tk.X)
        hbar.config(command=canvas.xview)
        # add verticall scrollbar
        vbar=tk.Scrollbar(self.window, orient=tk.VERTICAL)
        vbar.pack(side=tk.LEFT, fill=tk.Y)
        vbar.config(command=canvas.yview)
        # set scroll config for canvas
        canvas.config(xscrollcommand=hbar.set, yscrollcommand= vbar.set)
        canvas.pack(expand=True, fill=tk.BOTH)
        # mid position will be used to generate circle positions. 
        self.mid_position = (self.frame_width/2 ,self.frame_height/2)
        #generate linked list then draw all nodes
        self.head = generate_linked_list(n)
        self.drawNode(self.head)
        current = self.head.next
        while current != self.head:
            self.drawNode(current)
            current = current.next
        # change the current item color to blue
        canvas.itemconfig(self.head.data, fill="blue")

    def drawNode(self, node: Node):
        x = self.r_middle * sin(radians((node.data-1) * (self.theta) + 180)) + self.mid_position[0]
        y = self.r_middle * cos(radians((node.data-1) * (self.theta) + 180)) + self.mid_position[1]
        self.canvas.create_circle(x,y, fill="green")
        self.canvas.create_text(x,y,text=node.data,fill="black")

    def getCircleId(self, number: int) -> int:
        return 2*number-1

    def showSurvivor(self):
        messagebox.showinfo("Survivor", f"{self.head.data} survives!")
        self.close_window()
        self.button["state"] = "normal"
        self.isKilling = False
        self.windowIsOpen = False
        self.thread_num = 0

    def showInvalidInputDialog(self, input):
        messagebox.showerror('Input Error', f'Error: {input} is not a valid integer')

    def showInputTooLargeDialog(self, input):
        messagebox.showerror('Input Error', f'Error: {input} is too large!')
    
    def showInputTooSmallDialog(self, input):
        messagebox.showerror('Input Error', f'Error: input "{input}" cannot be negative!')

    def onWindowClose(self):
        self.windowIsOpen = False
        self.isKilling = False
        self.thread_num = 0
        self.button["state"] = "normal"
        self.window.destroy()

    def pauseThreads(self, event = None):
        self.pause = True

    def showCurrent(self):
        current = self.head
        canvas = self.canvas
        x = self.r_middle * sin(radians((current.next.data-1) * (self.theta) + 180)) + self.mid_position[0]
        y = self.r_middle * cos(radians((current.next.data-1) * (self.theta) + 180)) + self.mid_position[1]
        canvas.xview_moveto(x/(self.frame_width-10)- (1000/self.frame_width))
        canvas.yview_moveto(y/(self.frame_height-20)- (400/self.frame_height))