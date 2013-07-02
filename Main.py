import re
from string import Template
from sympy import Symbol
from sympy import simplify
from sympy.solvers import solve
from CircuitGraph import *
from Components import *

STATELIST = ['DCSS','ACSS']
STATE = 'DCSS'
Unknowns = []
Equations = []
w = 0

def NodalAnalysis(Circuit):
    global Unknowns
    global Equations
    Voltages = {}
    Currents = {}
    Values = {}

    #Make a list of all Nodal Equations and Names
    for n in Circuit.NodeList:
        Equations.append(NodalEquation(n))
        if n._Value == None:
            Unknowns.append(n.Name)
    for c in Circuit.ComponentList:
        if c._Value == None:
            Unknowns.append(c.Name)

    #Print
    print('\nEquations: ' + str(Equations) + ' == 0')
    print('Unknowns: ' + str(Unknowns) + '\n')

    #Solve the Circuit
    temp = solve(Equations, Unknowns, manual=True, dict=True)[0]

    #Simplify the Answer
    solutions = {}
    for N, V in temp.items():
        solutions[N]=simplify(V)

    #Print the solutions
    print('Solutions: ' + str(solutions) + '\n')

    #Put solutions back into graph
    if len(Unknowns) > 0:
        for N, V in solutions.items():
            Circuit.Names[N].Value = V

    #Put all Voltages, Currents, and Values into seperate Dictionaries
    for c in Circuit.ComponentList:
        Currents[Symbol('I_'+str(c.Name))]=c.Current
        Values[c.Name]=c.Value
    for n in Circuit.NodeList:
        Voltages[n.Name]=n.Value


    return Voltages, Currents, Values

def NodalEquation(NodeA, ignore=None):
    Equ = 0
    #For this node, add up all the currents going to each component
    for c in NodeA.ComponentList:
        if c.Node2 is NodeA:        #Assume current in
            Equ += c.Current
        elif c.Node1 is NodeA:
            Equ -= c.Current

    return Equ
        

def ReadCircuit(location):
    #Read File
    f = open(location,'r')
    text = f.read()

    #Define Global Variables
    global Graph
    global STATE
    global Unknowns
    global Equations
    global w

    #Parse Text    
    lines = re.split('\n+',text) #turn text into a list of lines
    for line in lines:
        #Split line into a list of entries, and Print
        e = re.split(' ',line.replace(',',''))            
        print(e)

        #Set Variables
        t=e[0]
        Value = None

        #Check for state at the top, create a CircuitGraph
        if t=='DCSS':
            STATE = t
            Graph = CircuitGraph()
        elif t=='ACSS':
            STATE = t
            w = float(e[1])
            Graph = CircuitGraph(w)



        #Process Components
        if t in Graph.COMPLIST:
            #Add Component with Pre-defined Value
            if len(e)>=5:
                #Set the Value of the Component
                if STATE=='DCSS':
                    Value = float(e[4])
                elif STATE=='ACSS':
                    if len(e)==5:
                        Value = float(e[4])
                    else:
                        Value = complex(float(e[4]),float(e[5]))
                    
                #Add the Component
                Graph.addComponent(t,e[1],int(e[2]),int(e[3]),Value)
                
            #Add Component with no Value
            elif len(e)==4:
                Graph.addComponent(t,e[1],int(e[2]),int(e[3]))
            else:
                raise NumItemsError('Not a valid number of parameters for Component ' + str(Name) + '.')

        #Process Commands
        elif t in Graph.COMMLIST:
            #Set the Value to use in the Command
            if STATE=='DCSS':
                Value = float(e[2])
            elif STATE=='ACSS':
                Value = complex(float(e[2]),float(e[3]))

            #Execute Command
            if t=='VOL':
                Graph.NodeList[int(e[1])].Value = Value
            if t=='CUR':
                Comp = Equations.Names[Symbol(e[1])]
                Equations.append(Comp.Current-Value)

        #Process Errors
        elif t=='GND':
            print('\nERROR: GND is always set to node 0\n')
        elif not t in STATELIST:
            raise IncorrectLabel('Label does not exist.')
        

    return Graph


#Start Main
loc = input("Input file address: ")
Circuit = ReadCircuit(loc)

output = NodalAnalysis(Circuit)
print('All Values:')
print('Voltages: ' + str(output[0]) + ' (V)')
print('Currents: ' + str(output[1]) + ' (A)')
print('Other: ' + str(output[2]) + '\n')

input('\n+Press ENTER to exit')
