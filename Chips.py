"""
Contains all of the chips our computer will need.
Each chip is composed of Gates built in Gates.py
"""
from Gates import *

def HalfAdder(a,b):
    #computes the sum, least significant bit of a+b,
    #and carry, the most significant bit of a+b
    
    carry = And(a,b)
    sum = Xor(a,b)
    return sum,carry

def FullAdder(a,b,c,):
    #computes the sum, least significant bit of a+b+c,
    #and carry, the most significant bit of a+b+c
    sum_bc,carry_bc = HalfAdder(b,c)
    sum,carry_abc = HalfAdder(sum_bc,a)
    carry = Or(carry_bc,carry_abc)
    return sum,carry

def Add16(a,b):
    #add 16 bit values a,b
    out = [0]*16
    sum,carry = HalfAdder(a[-1],b[-1])
    out[-1] = sum
    for index in range(1,16):
        sum , carry = FullAdder(a[-index-1],b[-index-1],carry)
        out[-index-1] = sum
       
    return out

def Inc16(input):
    #16 bit incrementer
    #out =input+1 (16-bit addition
    #overflow not detected or handled
    base = [0]*16
    base[15] = 1
    return Add16(input,base)

class DFF:
    #data flip flop gate
    #out(t) = input(t-1)
    
    def __init__(self):
        self.out = 0
        
    def load(self,input):
        self.out = input
    
        
class Bit:
    #1-bit register
    #if load[t] == 1 then out[t+1]= in[t]
    #else out[t+1] = out[t] (no change)
    def __init__(self):
        self.flipFlop = DFF()
    def bit(self,input,load):
        toclock = Mux(self.flipFlop.out, input, load)
        temp = self.flipFlop.out
        self.flipFlop.load(toclock)
        return temp

class Register:
    #16 big register
    #if load[t] == 1 then out[t+1]= in[t]
    #else out[t+1] = out[t] (no change)
    
    def __init__(self):
        self.r = [Bit() for i in range(16)]
    
    def register(self,input,load):
        return [self.r[i].bit(input[i],load) for i in range(16)]

class RAM8:
# Memory of 8 registers, each 16-bit wide.  
# The chip facilitates read and write operations, as follows:
#     Read:  out(t) = RAM8[address(t)](t)
#     Write: If load(t-1) then RAM8[address(t-1)](t) = in(t-1)
# In words: the chip always outputs the value stored at the memory 
# location specified by address. If load == 1, the in value is loaded 
# into the memory location specified by address.  This value becomes 
# available through the out output starting from the next time step.

    def __init__(self):
        self.r = [Register() for i in range(8)]
    
    def access(self,input,load,address):
        toMemory = DMux8Way(load,address)
        out = [self.r[i].register(input,toMemory[i]) for i in range(8)]
        
        return Mux8Way16(*out,address) 


class PC:
    #16 bit counter with load and reset controls
    #if reset(t-1) then out(t) = 0
    #else if load(t-1) then out(t) = in(t-1)
    #else if inc(t-1) then out(t) = out(t-1)+1 (integer addition)
    #else out(t) = out(t-1)
    
    def __init__(self):
        self.reg = Register()
        pass
    def go(self,input,load,inc,reset):
        torecycle = self.reg.r
        recycled = Inc16(torecycle)
        addornot = Mux16(torecycle,recycled,inc)
        loadornot = Mux16(addornot,input,load)
        parsedIn = Mux16(loadornot,0,reset)
        out = Register(parsedIn,1)
        return out

input = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
pc = PC()
print(pc.go(input,0,1,0))
print(pc.go(input,0,1,0))
print(pc.go(input,0,1,0))
print(pc.go(input,0,1,0))
print(pc.go(input,0,1,0))
print(pc.go(input,0,1,0))