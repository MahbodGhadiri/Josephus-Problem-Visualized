from math import radians, sin, cos
class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
    
def generate_linked_list(n: int, create_circle, create_text, frame_data: dict) -> Node:
    #root is just a place holder
    root = Node(0)
    current = root
    mid_position = frame_data["mid_position"]
    r_middle = frame_data["r_middle"]
    theta = frame_data["theta"]
    for i in range(1,n+1):
        x = r_middle * sin(radians((i-1) * (theta) + 180)) + mid_position[0]
        y = r_middle * cos(radians((i-1) * (theta) + 180)) + mid_position[1]
        component = create_circle(x,y, fill="green")
        num = create_text(x,y,text=i,fill="black")
        data = {
            "num": num,
            "component": component
        }
        new_node = Node(data)
        current.next = new_node
        current = current.next
    current.next = root.next
    current = current.next
    return current



