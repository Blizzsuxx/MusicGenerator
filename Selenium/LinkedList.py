


class Node:
    def __init__(self, key, value) -> None:
        self._next = None
        self.key = key
        self.value = value
    

    def next(self):
        return self._next
        



class LinkedList:

    def __init__(self) -> None:
        self.head = None
        self.tail = self.head
    
    def pop(self) -> None:
        if not self.head is None:
            returnValue = self.head
            self.head = self.head._next
            if self.head is None:
                self.tail = None
            return returnValue
    
    def add(self, node):
        if not self.tail is None:
            self.tail._next = node
            self.tail = node
        else:
            self.head = node
            self.tail = node
    
    def add2(self, key, value):
        self.add(Node(key, value))
    

    def isEmpty(self):
        return self.head is None
    
