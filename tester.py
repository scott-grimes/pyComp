from Chips import *
from Gates import *

def testBit():
    a = 1
    b = 0
    print('creating bit')
    bit = Bit()
    print('bit currently reads: ', end='')
    print(bit.out)
    
    print('loading a 1')
    bit.register(a,1)
    print('bit now reads',end='')
    print(bit.out)
    
    print('loading a 0')
    bit.register(b,1)
    print('bit now reads',end='')
    print(bit.out)
    
def testRegister():
    a = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    b = [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0]
    print('creating register')
    r=Register()
    print('register currently reads: ', end='')
    print(r.out)
    
    print('loading a')
    r.register(a,1)
    print('register currently reads: ', end='')
    print(r.out)
    
    print('loading b')
    r.register(b,1)
    print('register currently reads: ', end='')
    print(r.out)
    
    print('not loading a')
    r.register(a,0)
    print('register currently reads: ', end='')
    print(r.out)

def decToBin(input):
    ans = []
    while(input>0):
        ans.append(input%2)
        input = input//2
    while(len(ans)<16):
        ans.append(0)
    ans.reverse()
    return ans

def binToDec(input):
    return sum(c*(2**i) for i,c in enumerate(input[::-1]))
    
def testRam():
    
    memory = [decToBin(i)[-3::] for i in range(8)]
    a = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    
    ram = RAM8()
    for address in memory: 
        print(ram.access(a,0,address))
    print('loading')
    ram.access(a,1,memory[2])
    for address in memory: 
        print(ram.access(a,0,address))

def testPC():
    a = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    b = [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0]
    pc = PC()
    print(pc.register(b,1,0,0))
    print(pc.register(b,0,1,0))
    print(pc.register(b,0,1,0))
    print(pc.register(b,0,1,0))
    print(pc.register(b,0,1,0))
    print(pc.register(a,1,0,0))
    print(pc.register(a,1,0,1))
    print(pc.register(b,0,1,0))

def testALU():
    #x,y,zx,nx,zy,ny,f,no):
    #  IN  
    #    x[16], y[16],  // 16-bit inputs        
    #    zx, // zero the x input?
    #    nx, // negate the x input?
    #    zy, // zero the y input?
    #    ny, // negate the y input?
    #    f,  // compute  out = x + y (if f == 1) or out = x & y (if == 0)
    #    no; // negate the out output?
    #
    #OUT = answer
    #    zr, // 1 if (out == 0), 0 otherwise
    #    ng; // 1 if (out < 0),  0 otherwise
    x = decToBin(4)
    y = decToBin(4)
    args = [0,1,0,0,1,0] #0+y = 4
    print(ALU(x,y,*args))


def testRam64():
    a = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    memory = [decToBin(i)[-6::] for i in range(64)]
    ram = RAM64()
    for address in memory: 
        print(address)
        print(sum(ram.access(a,0,address)))
    print('loading')
    ram.access(a,1,memory[2])
    for address in memory: 
        if(sum(ram.access(a,0,address))>0):
            print(address)
def testRam512():
    a = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    memory = [decToBin(i)[-9::] for i in range(512)]
    ram = RAM512()
    for address in memory: 
        if(sum(ram.access(a,0,address)) != 0):
            print(address)
    print('loading')
    ram.access(a,1,memory[2])
    for address in memory: 
        if(sum(ram.access(a,0,address))>0):
            print(address)
def testRam4K():
    a = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    memory = [decToBin(i)[-9::] for i in range(4096)]
    ram = RAM4K()
    print('loading')
    ram.access(a,1,memory[4095])
    for address in memory: 
        if(sum(ram.access(a,0,address))>0):
            print(address)
testRam4K()
#testRam64()
