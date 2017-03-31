"""
This file contains all of the basic gates our
computer will need. We start with a Nand gate,
and all other gates are composed of Nand gates

Gates:
Nand
Not
And
Or
Xor
Multiplexor
Demultiplexor
and 16-bit versions and multi-way versions of
each gate
"""


def Nand(a,b):
    #Elementary Gate upon which the entire computer
    #is built!
    if a==1 and b==1:
        return 0
    return 1

def Not(a):
   return Nand(a,a)
def And(a,b):
    c = Nand(a,b)
    return Not(c)

def Or(a,b):
    not_a = Not(a)
    not_b = Not(b)
    return Nand(not_a,not_b)

def Xor(a,b):
    not_a = Not(a)
    not_b = Not(b)
    w1 = And(a,not_b)
    w2 = And(not_a,b)
    return Or(w1,w2)
            
def Mux(a,b,sel):
    #if sel is 1, return b, otherwise return a
    not_sel = Not(sel)
    w1 = And(a,not_sel)
    w2 = And(b,sel)
    return Or(w1,w2)
        
def DMux(w,sel):
    #if sel is 0 returns (w,0), else return (0,w)
    not_sel = Not(sel)
    a = And(not_sel,w)
    b = And(sel,w)
    return a,b

def Not16(input):
    #16 bit not gate
    return [Not(i) for i in input]

def And16(a,b):
    #16 bit and gate
    return [And(i,j) for i,j in zip(a,b)]

def Or16(a,b):
    #16 bit or gate
    return [Or(i,j) for i,j in zip(a,b)]

def Mux16(a,b,sel):
    #16 bit Mux16 gate
    return [Mux(i,j,k) for i,j,k in zip(a,b,sel)]
    
def Or8Way(input):
    #8way input, returns true if any value is true
    z1 = Or(input[0],input[1])
    z2 = Or(input[2],input[3])
    z3 = Or(input[4],input[5])
    z4 = Or(input[6],input[7])
    z5 = Or(z1,z2)
    z6 = Or(z3,z4)
    return Or(z5,z6)


def Mux4Way16(a,b,c,d,sel):
    #4-way 16-bit multiplexor.  
    #returns a if sel == 00
    #        b if sel == 01
    #        c if sel == 10
    #        d if sel == 11
     z1 = Mux16(a,b,sel[0])
     z2 = Mux16(c,d,sel[0])
     return Mux16(z1,z2,sel[1])
 
def Mux8Way16(a,b,c,d,e,f,g,h,sel):
    #8-way 16-bit multiplexor.  
    #returns a if sel == 000
    #        b if sel == 001
    #        etc
    #        h if sel == 111
    z1 = Mux4Way16(a,b,c,d,sel[0:2])
    z2 = Mux4Way16(e,f,g,h,sel[0:2])
    return Mux16(z1,z2,sel[2])

def DMux4Way(input,sel):
    # given input array {a,b,c,d}
    # output = {in,0,0,0} if sel == 00
    #          {0,in,0,0} if sel == 01
    #          {0,0,in,0} if sel == 10
    #          {0,0,0,in} if sel == 11
    
    out1, out2 = DMux(input, sel[1])
    a,b = DMux(out1,sel[0])
    c,d = DMux(out2,sel[0])
    return (a,b,c,d)

def DMux8Way(input,sel):
    # 8-way demultiplexor
    # given 16bit input array {a,b,c,d,e,f,g,h}
    # output = {in,0,0,0,0,0,0,0} if sel == 000
    #          {0,in,0,0,0,0,0,0} if sel == 001
    #          etc.
    #          {0,0,0,0,0,0,0,in} if sel == 111
    w1,w2,w3,w4 = DMux4Way(input,sel[1:3])
    a,b = DMux(w1,sel[0])
    c,d = DMux(w2,sel[0])
    e,f = DMux(w3,sel[0])
    g,h = DMux(w4,sel[0])
    
    return(a,b,c,d,e,f,g,h)
