import tkinter as tk
from constructs.linked_list import generate_linked_list, Node
from math   import sin, cos, radians
#adding a custom method to Canvas class
def _create_circle(self, x, y, r = 9, **kwargs):
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
        root.mainloop()


    def visualize(self):
        try:
            n = int(self.entry.get())
        except:
            self.entry.delete(0, tk.END)
            #self.entry.insert(0,"")
            return
        if n<=0:
            self.entry.delete(0, tk.END)
            return
        #set window
        window = tk.Toplevel(self.root)
        self.window = window
        self.n = n
        self.drawLinkedList()
        #set size
        window.geometry(f"{self.frame_width}x{self.frame_height}")
        #window.minsize(frame_width , frame_height)
        #window.maxsize(frame_width , frame_height)
        tk.Button(window,
            text= "Kill Next",
            command= self.kill_next
            ).pack()

    def kill_next(self, k = 1)->Node:
        current = self.head
        canvas = self.canvas
        canvas.itemconfig(self.getCircleId(current.data), fill="green")
        canvas.itemconfig(self.getCircleId(current.next.data), fill="red")
        current.next = current.next.next
        self.head = current.next
        canvas.itemconfig(self.getCircleId(self.head.data), fill="blue")
        if(current.next == current.next.next):
            popup = tk.Toplevel(self.window)
            popup.geometry("300x50")
            popup.minsize(300,50)
            popup.maxsize(300,50)
            label = tk.Label(popup, text = f"Number {int(self.head.data)} survives!")
            close_button = tk.Button(popup, text="Ok", command=self.close_window)
            label.pack()
            close_button.pack()

    def close_window(self):
        self.window.destroy()

    def drawLinkedList(self):
        n = self.n
        self.theta = 360/n
        self.r_middle = float(12 / sin(radians(self.theta/2))) if float(10 / sin(radians(self.theta/2)))>50 else 50
        self.frame_width = int(2*self.r_middle + 200)
        self.frame_height = self.frame_width 
        self.canvas = tk.Canvas(self.window, width=self.frame_width, height=self.frame_height-20)
        canvas = self.canvas
        canvas.pack(expand=True, fill=tk.BOTH)
        self.mid_position = (self.frame_width/2 ,self.frame_height/2)
        self.head = generate_linked_list(n)
        self.drawNode(self.head)
        current = self.head.next
        while current != self.head:
            self.drawNode(current)
            current = current.next
        canvas.itemconfig(self.head.data, fill="blue")

    def drawNode(self, node: Node):
        x = self.r_middle * sin(radians((node.data-1) * (self.theta) + 180)) + self.mid_position[0]
        y = self.r_middle * cos(radians((node.data-1) * (self.theta) + 180)) + self.mid_position[1]
        self.canvas.create_circle(x,y, fill="green")
        self.canvas.create_text(x,y,text=node.data,fill="black")

    def getCircleId(self, number: int) -> int:
        return 2*number-1