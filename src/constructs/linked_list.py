from math import radians, sin, cos
class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
    
def generate_linked_list(n: int) -> Node:
    #root is just a place holder
    root = Node(0)
    current = root
    for i in range(1,n+1):
        new_node = Node(i)
        current.next = new_node
        current = current.next
    current.next = root.next
    current = current.next
    return current
