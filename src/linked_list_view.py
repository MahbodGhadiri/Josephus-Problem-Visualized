import tkinter as tk
from constructs.linked_list import generate_linked_list, Node
from math import sin, cos, radians
import threading
import time

_r = 12
class LinkedListView:
    def __init__(self, window: tk.Toplevel, n: int, onFinish):
        self.window = window
        self.onFinish = onFinish
        self.drawLinkedList(n)
        self.showCurrent()
        self.thread_num = 0
        self.windowIsOpen = True
        self.isKilling = False
        
    def drawLinkedList(self, n):
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
            width= self.frame_width-10,
            height= self.frame_height-20,
            scrollregion=(0,0,self.frame_width-10, self.frame_height-20),
            bg="#0ba7b3",
            borderwidth= 10
        )
        canvas = self.canvas
        # add horizontal scrollbar
        hbar=tk.Scrollbar(
            self.window, 
            orient=tk.HORIZONTAL,
            background= "#0ba7b3"
        )
        hbar.pack(side=tk.TOP,fill=tk.X)
        hbar.config(command=canvas.xview)
        # add verticall scrollbar
        vbar=tk.Scrollbar(
            self.window,
            orient= tk.VERTICAL,
            background ="#0ba7b3"
        )
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
        (x,y) = self.calculatePosition(node.data)
        self.canvas.create_circle(x,y, fill="green")
        self.canvas.create_text(x,y,text=node.data,fill="black")

    def auto_kill(self, event):
        self.stop = False
        if self.thread_num < 9:
            threading.Thread(target= self.kill_all).start()
            self.thread_num += 1

    def kill_all(self):
        '''
            keep killing until kill_next() return false marking the end of solution
            check if user has not close the window thus removing nodes
            check if user has not stopped the thread
        '''
        keepKilling = True
        while keepKilling and self.windowIsOpen and not self.stop:
            keepKilling = self.kill_next()
            time.sleep(0.5)
        self.thread_num -= 1
    
    def kill_next(self, event = None):
        # to avoid multiple thread to change shared resource, lock the resource
        if(self.isKilling):
            return
        self.isKilling = True

        # scroll to current node
        current = self.head
        canvas = self.canvas
        self.showCurrent()

        # mark current node green. mark the next node as red.
        canvas.itemconfig(self.getCircleId(current.data), fill="green")
        canvas.itemconfig(self.getCircleId(current.next.data), fill="red")

        # move to next next node and mark it blue
        current.next = current.next.next
        self.head = current.next
        canvas.itemconfig(self.getCircleId(self.head.data), fill="blue")

        # check if the problem is solved
        if(current.next == current.next.next):
            self.onFinish()
            return False
        
        # unlock shared resource
        self.isKilling = False

        return True

    def showCurrent(self):
        current = self.head
        canvas = self.canvas
        (x,y) = self.calculatePosition(current.next.next.data)
        canvas.xview_moveto(x/(self.frame_width-10)- (1000/self.frame_width))
        canvas.yview_moveto(y/(self.frame_height-20)- (400/self.frame_height))

    def calculatePosition(self, n):
        x = self.r_middle * sin(radians((n-1) * (self.theta) + 180)) + self.mid_position[0]
        y = self.r_middle * cos(radians((n-1) * (self.theta) + 180)) + self.mid_position[1]
        return (x,y)


    def getCircleId(self, number: int) -> int:
        return 2*number-1

    def stopThreads(self, event = None):
        self.stop = True

    def closeView(self):
        self.isKilling = False
        self.windowIsOpen = False