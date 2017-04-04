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
    memory = [decToBin(i)[-12::] for i in range(4096)]
    ram = RAM4K()
    print('loading')
    ram.access(a,1,memory[4095])
    count = 0
    for address in memory: 
        if(count%100==0):
            print(count)
        if(sum(ram.access(a,0,address))>0):
            print(address)
        count+=1
def testRam32K():
    a = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    memory = [decToBin(i)[-15::] for i in range(4096*8)]
    ram = RAM32K()
    print('loading')
    ram.access(a,1,memory[3])
    count = 0
    for address in memory: 
        if(count%100==0):
            print(count)
        if(sum(ram.access(a,0,address))>0):
            print(address)
        count+=1


def testALU():
    with open("alu.tst", "r") as ins: 
        badCount = 0
        for line in ins:
            if line[0] != '#':
                parsed = line.split(',')
                x = parsed[0]
                y = parsed[1]
                zx = int(parsed[2])
                nx = int(parsed[3]) 
                zy  = int(parsed[4])
                ny  = int(parsed[5])
                f  = int(parsed[6])
                no = int(parsed[7])
                out = parsed[8]
                out = [int(i) for i in out]
                zr = int(parsed[9])
                ng =  int(parsed[10][0])
                x = [int(i) for i in x]
                y = [int(i) for i in y]
                
                myout,myzr,myng = ALU(x,y,zx,nx,zy,ny,f,no)
                if(myout != out or
                   ng != myng or
                   zr != myzr):
                    badCount+=1
                    print('my out: ',end='')
                    print(out)
                    print('act ot: ',end='')
                    print(myout)
                    print(zr,myzr)
                    print(ng,myng)
        print('I got '+str(badCount)+' incorrect')

