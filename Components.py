from sympy import Symbol
from sympy import oo

def cincout(me):
    total = 0
    for c in me.Node1.ComponentList:
        if c is not me:
            if me.Node1 is c.Node2:           #Convert to Passive
                total += c.Current
            elif me.Node1 is c.Node1:
                total -= c.Current

    return total

class Component:    
    def __init__(self, Name, Node1, Node2, Value=None, w=0):
        self.Node1=Node1
        self.Node2=Node2
        Node1.add(self)
        Node2.add(self)
        self.w = w
        self.Name=Symbol(Name)
        self.Value = Value
    def __str__(self): return str(self.Name)

    #Value will be used for the main attribute of the class
    def set_Value(self, Value): self._Value = Value
    def get_Value(self):
        if self._Value == None:
            return self.Name
        else:
            return self._Value

    #Current and Voltage are by default derived, but will later be defined as values in other subclasses
    def get_Current(self):
        return self.Voltage/self.Value             #Assume Passive
    def get_Voltage(self):
        return (self.Node1.Value-self.Node2.Value) #Assume Passive
        

    Value = property(get_Value, set_Value)
    Voltage = property(get_Voltage)
    Current = property(get_Current)

#Here are all the Impedance Components
class Impedance(Component):
    pass
class Resistor(Impedance):
    pass
class Inductor(Impedance):
    def set_Value(self,ind):
        if self.w == 0:
            self._Value = 0
            self.Node1.Value = self.Node2.Value
        else:
            self._Value = complex(0,self.w*ind)
            
    def get_Current(self):
        if self.w == 0:            
            #Current in = Current out
            return cincout(self)
            
        else:
            return self.Voltage/self.Value             #Assume Passive
                    
    Value = property(Component.get_Value, set_Value)
    Current = property(get_Current)
    
class Capacitor(Impedance):
    def set_Value(self,c):
        if self.w == 0:
            self._Value = complex(0,-oo)
        else:
            self._Value = complex(0,-1/(self.w*c))
    def get_Current(self):
        if self.w == 0:
            return 0
        else:
            return self.Voltage/self.Value

    Value = property(Component.get_Value, set_Value)
    Current = property(get_Current)

#Here are all the Source Components
class Source(Component):
    pass
class VSource(Source):
    def set_Value(self, Voltage):
        self._Value=Voltage
        self.Node1.Value = self.Node2.Value+Voltage
    def get_Voltage(self):
        return self.Value
    def get_Current(self):
        return cincout(self)

    Value = property(Component.get_Value,set_Value)
    Voltage = property(get_Voltage,set_Value)
    Current = property(get_Current)

class CSource(Source):
    def get_Current(self):
        if self.Value==None:
            return self.Name
        else:
            return -self.Value                                 #Convert to Passive
        
    Current = property(get_Current,Component.set_Value)
