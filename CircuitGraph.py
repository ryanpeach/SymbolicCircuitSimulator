from sympy import Symbol
from Components import *

class CircuitGraph:
    COMPLIST = ['IMP', 'RES', 'IND', 'CAP', 'VSC', 'CSC']
    COMMLIST = ['VOL','CUR']
    
    def __init__(self,w=0):
        self.NodeList = [Node('GND',0)]
        self.ComponentList = []
        self.Names = {}
        self.w = w

    #Adds all nodes between the last node on list to node number n
    #Adds the nodes to Names
    def addNodes(self, n):
        for i in range(len(self.NodeList),n+1):
            #Create Name
            Name = 'V'+str(i)

            #Check for DuplicateName Exception
            if Name in self.Names:
                raise DuplicateName(Name + ' already exists in Circuit. You can not use two items of the same name.')

            #Add Node
            newNode = Node(Name)
            self.NodeList.append(newNode)
            self.Names[newNode.Name]=newNode
    
    def addComponent(self, t, Name, Node1, Node2, Value=None):
        #Create Nodes if they don't already exist
        if Node1 >= len(self.NodeList):
            self.addNodes(Node1)
        if Node2 >= len(self.NodeList):
            self.addNodes(Node2)

        #Check for DuplicateName Exception
        if Name in self.Names:
            raise DuplicateName(Name + ' already exists in Circuit. You can not use two items of the same name.')

        #Add Components based on type (t)
        newComponent = None
        if t=='IMP':
            newComponent = Impedance(Name,self.NodeList[Node1],self.NodeList[Node2],Value)
        elif t=='RES':
            newComponent = Resistor(Name,self.NodeList[Node1],self.NodeList[Node2],Value)
        elif t=='IND':
            newComponent = Inductor(Name,self.NodeList[Node1],self.NodeList[Node2],Value,self.w)
        elif t=='CAP':
            newComponent = Capacitor(Name,self.NodeList[Node1],self.NodeList[Node2],Value,self.w)
        elif t=='VSC':
            newComponent = VSource(Name,self.NodeList[Node1],self.NodeList[Node2],Value)
        elif t=='CSC':
            newComponent = CSource(Name,self.NodeList[Node1],self.NodeList[Node2],Value)
        else:
            raise IncorrectLabel('This item is not a Component. Check that CircuitGraph has it listed.')                       #Just in case the programmer uses this wrong

        self.ComponentList.append(newComponent)
        self.Names[newComponent.Name]=newComponent

#Here are the main super classes
class Node:
    def __init__(self, Name, Voltage=None):
        self.Name = Symbol(Name)
        self.ComponentList = []
        self._Value=Voltage
    def __str__(self):
        return str(self.Name)
    def add(self, Component):
        self.ComponentList.append(Component)
    def set_Value(self, Value): self._Value = Value
    def get_Value(self):
        if self._Value == None:
            return self.Name
        else:
            return self._Value
    Value = property(get_Value, set_Value)

#Here are all the Errors
class NumItemsError(Exception):
    pass
class IncorrectLabel(Exception):
    pass
class DuplicateName(Exception):
    pass
