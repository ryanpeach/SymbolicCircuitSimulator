import re
from string import Template
from sympy import Solve, simplify
from sympy import simplify
from sympy.solvers import solve
from CircuitGraph import *
from Components import *

STATELIST = ['DCSS','ACSS','Laplace']
STATE = 'DCSS'
Unknowns = []
Equations = []
w = 0
        
#Done, not checked
def ReadCircuit(location):
    #Read File
    f = open(location,'r')
    text = f.read()

    #Define Global Variables
    global Graph

    #Parse Text
    lines = re.split('\n+',text) #turn text into a list of lines
    for line in lines:
        #Split line into a list of entries, and Print
        e = re.split(',',line.replace(' ',''),5)            
        print(e)

        #Set Variables
        t=e[0]

        #Check for state at the top, create a CircuitGraph
        if t in STATELIST:
            if t=='DCSS':
                Graph = CircuitGraph(t)
            elif t=='ACSS':
                if len(e)>1:
                    Graph = CircuitGraph(t,float(e[1]))
                else:
                    Graph = CircuitGraph(t,Symbol('w'))
            elif t=='Laplace':
                Graph = CircuitGraph(t,Symbol('w'))


        #Process Components
        if t in Graph.COMPLIST:
            #Add Component with Pre-defined Value and Initial Value
            if len(e)==6:
                Graph.addComponent(str(t),Symbol(e[1]),int(e[2]),int(e[3]),S(e[4]),float(e[5]))
                
            #Add Component with Pre-defined Value
            elif len(e)==5:
                Graph.addComponent(str(t),Symbol(e[1]),int(e[2]),int(e[3]),S(e[4]))

            #Add Component with no Value
            elif len(e)==4:
                Graph.addComponent(str(t),Symbol(e[1]),int(e[2]),int(e[3]))

            #Return Error if not enough parameters
            else:
                raise NumItemsError('Not a valid number of parameters for Component ' + str(Name) + '.')

        #Process Commands
        elif t in Graph.COMMLIST:
            #Set a Parameter of a component
            if len(e)==4:
                Graph.exeCommand(str(t),int(e[1]),int(e[2]),S(e[3]))
                
            #Set the Value of one node
            if len(e)==2:
                Graph.exeCommand(str(t),int(e[1]))

            #Return Error if wrong number of parameters
            else:
                raise NumItemsError('Not a valid number of parameters for Command ' + str(t) + '.')

        #Process Errors
        elif t=='GND':
            print('\nERROR: GND is always set to node 0\n')
        elif not t in STATELIST:
            raise IncorrectLabel('Label does not exist.')
        

    return Graph

#Start Main
#Done, not checked
loc = input("Input file address: ")
Circuit = ReadCircuit(loc)

Equations, Unknowns, Solutions = Circuit.NodalAnalysis()

#Print
print('\nEquations: ' + str(Equations) + ' == 0')
print('Unknowns: ' + str(Unknowns) + '\n')

#Print the solutions
print('Solutions: ' + str(Solutions) + '\n')

#Put all Voltages, Currents, and Values into seperate Dictionaries
for n, c in Circuit.ComponentList.items():
    Currents[Symbol('I_'+str(n))]=c.Current
    Values[n]=c.Value
for n in Circuit.NodeList:
    Voltages[n.Name]=n.Value

print('All Values:')
print('Voltages: ' + str(output[0]) + ' (V)')
print('Currents: ' + str(output[1]) + ' (A)')
print('Other: ' + str(output[2]) + '\n')

input('\n+Press ENTER to exit')
