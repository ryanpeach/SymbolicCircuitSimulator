from sympy import Symbol
from Components import *

class CircuitGraph:
    COMPLIST = ['IMP', 'RES', 'IND', 'CAP', 'VSC', 'CSC']
    COMMLIST = ['VOL','CUR']
    
    def __init__(self,STATE='DCSS',w=0):
        self.NodeList = [Node('GND',0)]
        self.ComponentList = {}
        self.Names = {}
        self.STATE = STATE
        self.w = w

    #Adds all nodes between the last node on list to node number n
    #Adds the nodes to Names
    def addNodes(self, n):
        for i in range(len(self.NodeList),n+1):
            #Create Name
            Name = 'N'+str(i)

            #Check for DuplicateName Exception
            if Name in self.Names:
                raise DuplicateName(Name + ' already exists in Circuit. You can not use two items of the same name.')

            #Add Node
            newNode = Node(Name)
            self.NodeList.append(newNode)
            self.Names[newNode.Name]=newNode.Value

    #Done, not checked
    def addComponent(self, t, Name, Node1, Node2, Value=None, Init = 0):
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

        #Add to Graph
        self.ComponentList[newComponent.Name]=newComponent
        self.Names[newComponent.Name]=newComponent.Value

    def exeCommand():
        pass

    def NodalAnalysis(Circuit):
        Unknowns = []
        Equations = []

        #Make a list of all Nodal Equations and Names
        for n in self.NodeList:
            self.Equations.append(self._KCL(n))
            if n._Value == None:
                self.Unknowns.append(n.Name)
        for n, c in self.ComponentList.items():
            if c._Value == None:
                self.Unknowns.append(n)

        #Simplify the Equations List
        pass

        #Solve the Circuit
        sol = solve(Equations, Unknowns, manual=True, dict=True)[0]

        #Simplify the Answers
        Solutions = {}
        for N, V in sol.items():
            Solutions[N]=simplify(V)

        return Equations, Unknowns, Solutions

    def _KCL(NodeA, ignore=None):
        Equ = 0
        #For this node, add up all the currents going to each component
        for n, c in NodeA.ComponentList.items():
            if c.Node2 is NodeA:        #Assume current in
                Equ += c.Current
            elif c.Node1 is NodeA:
                Equ -= c.Current

        return Equ

#Here is the main Node class
class Node:
    def __init__(self, Name, Voltage=None):
        self.Name = Symbol(Name)
        self.ComponentList = {}
        self._Value=Voltage
    def __str__(self):
        return str(self.Name)
    def add(self, Component):
        self.ComponentList[Component.Name]=Component
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
