import tkinter as tk
from constructs.linked_list import generate_linked_list, Node
from math   import sin, radians
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

        theta = 360/n
        r_middle = float(12 / sin(radians(theta/2))) if float(10 / sin(radians(theta/2)))>50 else 50
        frame_width = int(2*r_middle + 200)
        frame_height = frame_width 
        #set size
        window.geometry(f"{frame_width}x{frame_height}")
        #window.minsize(frame_width , frame_height)
        #window.maxsize(frame_width , frame_height)
        self.canvas = tk.Canvas(window, width=frame_width, height=frame_height-20)
        canvas = self.canvas
        canvas.pack(expand=True, fill=tk.BOTH)
        mid_position = (frame_width/2,frame_height/2)
        frame_data = {
            "mid_position": mid_position,
            "r_middle": r_middle,
            "theta": theta
        }
        self.current = generate_linked_list(n, canvas.create_circle, canvas.create_text, frame_data)
        canvas.itemconfig(self.current.data["component"], fill="blue")
        tk.Button(window,
            text= "Kill Next",
            command= self.kill_next
            ).pack()

    def kill_next(self)->Node:
        current = self.current
        canvas = self.canvas
        canvas.itemconfig(self.current.data["component"], fill="green")
        canvas.itemconfig(current.next.data["component"], fill="red")
        current.next = current.next.next
        self.current = current.next
        canvas.itemconfig(self.current.data["component"], fill="blue")
        if(current.next == current.next.next):
            popup = tk.Toplevel(self.window)
            popup.geometry("300x50")
            popup.minsize(300,50)
            popup.maxsize(300,50)
            label = tk.Label(popup, text = f"Number {int(self.current.data['num']/2)} survives!")
            close_button = tk.Button(popup, text="Ok", command=self.close_window)
            label.pack()
            close_button.pack()

    def close_window(self):
        self.window.destroy()