"""

Contains all of the chips our computer will need.
Each chip is composed of Gates built in Gates.py
All gates are based on a single Nand gate

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
    #overflow not handled
    out = [0]*16
    sum,carry = HalfAdder(a[-1],b[-1])
    out[-1] = sum
    for index in range(1,16):
        sum , carry = FullAdder(a[-index-1],b[-index-1],carry)
        out[-index-1] = sum
       
    return out

def Inc16(input):
    #16 bit incrementer
    #out =input+1 (16-bit addition)
    #overflow not handled
    base = [0]*16
    base[-1] = 1
    return Add16(input,base)

def ALU(x,y,zx,nx,zy,ny,f,no):
    #  IN  
    #    x[16], y[16],  // 16-bit inputs        
    #    zx, // zero the x input?
    #    nx, // negate the x input?
    #    zy, // zero the y input?
    #    ny, // negate the y input?
    #    f,  // compute  out = x + y (if f == 1) or out = x & y (if == 0)
    #    no; // negate the out output?

    #OUT 
    #    out[16], // 16-bit output
    #    zr, // 1 if (out == 0), 0 otherwise
    #    ng; // 1 if (out < 0),  0 otherwise
    x1 = Mux16(x,[0]*16,zx)
    notx1 = Not16(x1)
    x2 = Mux16(x1,notx1,nx)
    
    y1 = Mux16(y,[0]*16,zy)
    noty1 = Not16(y1)
    y2 = Mux16(y1,noty1,ny)
    
    xyadd = Add16(x2,y2)
    xyand = And16(x2,y2)
    almostOut = Mux16(xyand,xyadd,f)
    
    notAlmostOut = Not16(almostOut)
    out = Mux16(almostOut, notAlmostOut, no)
    outlow = out[0:8]
    outhigh = out[8:16]
    ng = out[0]
    
    zr1 = Or8Way(outlow)
    zr2 = Or8Way(outhigh)
    zralmost = Or(zr1,zr2)
    zr = Not(zralmost)
    
    return out,zr,ng
    
class DFF:
    #data flip flop gate
    #out(t) = input(t-1)
    
    def __init__(self):
        self.out = 0
        
    def load(self,input):
        temp = self.out
        self.out = input
        return temp
               
class Bit:
    #1-bit register
    #if load[t] == 1 then out[t+1]= in[t]
    #else out[t+1] = out[t] (no change)
    def __init__(self):
        self.flipFlop = DFF()
        self.out = self.flipFlop.out
        
    def register(self,input,load):
        self.out = self.flipFlop.out
        toclock = Mux(self.out, input, load)
        self.out = self.flipFlop.load(toclock)
        return self.out

class Register:
    #16 big register
    #if load[t] == 1 then out[t+1]= in[t]
    #else out[t+1] = out[t] (no change)
    
    def __init__(self):
        self.bits = [Bit() for i in range(16)]
        self.out = [0]*16
    
    def register(self,input,load):
        for i in range(16):
            self.out[i] = self.bits[i].register(input[i],load)
        return self.out
    
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
        

class RAM64:
    #memory of 64 registers, each 16bits wide
    def __init__(self):
        self.r = [RAM8() for i in range(8)]
    
    def access(self,input,load,address):
        
        toMemory = DMux8Way(load,address[3:6])
        out = [self.r[i].access(input,toMemory[i],address[0:3]) for i in range(8)]
        return Mux8Way16(*out,address[3:6])

class RAM512():   
    #memory of 512 registers, each 16bits wide

    def __init__(self):
        self.r = [RAM64() for i in range(8)]
    
    def access(self,input,load,address):
        toMemory = DMux8Way(load,address[6:9])       
        out = [self.r[i].access(input,toMemory[i],address[0:6]) for i in range(8)]
        return Mux8Way16(*out,address[6:9])
    
class RAM4K():
    #memory of 4096 registers, each 16bits wide

    def __init__(self):
        self.r = [RAM512() for i in range(8)]
    
    def access(self,input,load,address):
        toMemory = DMux8Way(load,address[9:12])       
        out = [self.r[i].access(input,toMemory[i],address[0:9]) for i in range(8)]
        return Mux8Way16(*out,address[9:12])

class RAM32K():
    #memory of 32768 registers, each 16 bits wide
    def __init__(self):
        self.r = [RAM4K() for i in range(8)]
    
    def access(self,input,load,address):
        toMemory = DMux8Way(load,address[12:15])       
        out = [self.r[i].access(input,toMemory[i],address[0:12]) for i in range(8)]
        return Mux8Way16(*out,address[12:15])
    
class FASTRAM():
    #faster implementation of RAM, instead of building ram from
    #chips just use an array (speeds up simulation)
    
    #memory of n 16-bit registers
    def __init__(self,n):
        self.ram = [[0]*16]*n
        
     
        
    def access(self,input,load,address):
        address_in_dec = sum(c*(2**i) for i,c in enumerate(address[::-1]))
        print(address_in_dec)
        if(load == 1):
            self.ram[address_in_dec] = input
        return self.ram[address_in_dec]

class PC:
    #16 bit counter with load and reset controls
    #if reset(t-1) then out(t) = 0
    #else if load(t-1) then out(t) = in(t-1)
    #else if inc(t-1) then out(t) = out(t-1)+1 (integer addition)
    #else out(t) = out(t-1)
    
    def __init__(self):
        self.reg = Register()
        self.last = self.reg.out[:]
        pass
    
   
    
    def register(self,input,load,inc,reset):
        
        incremented = Inc16(self.last)
        incOrNot = Mux16(self.last,incremented,inc)
        loadOrNot = Mux16(incOrNot,input,load)
        resetOrNot = Mux16(loadOrNot,[0]*16,reset)
        self.last = loadOrNot
        self.out = self.reg.register(resetOrNot,1)
        return self.out

