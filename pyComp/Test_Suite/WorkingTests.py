from ..Hardware.Chips import *
from ..Hardware.Gates import *
from ..Hardware.Components import *
import os


def generalTester(desired_outputs,my_outputs):
    badcount = 0
    for i,j in zip(desired_outputs,my_outputs):
        for a,b in zip(i,j):
            if(a!=b and not (a=="*******" or b=="*******")):
                badcount+=1
                print(i,j)
                
    print('Tested with '+str(badcount)+' incorrect answers out of '+str(len(desired_outputs)))
    

def decToBin(input):
    ans = []
    myInput = input
    if(input<0):
        input = -input
    while(input>0):
        ans.append(input%2)
        input = input//2
    while(len(ans)<16):
        ans.append(0)
    ans.reverse()
    #2's complement for neg values
    if(myInput<0):
        ans = Not16(ans)
        ans = Inc16(ans)
    return ans

def binToDec(input,IgnoreNeg = False):
    if(not IgnoreNeg):
        makeNeg = False
        if(input[0]==1):
            makeNeg = True
            #2's complement for neg values
            input = Not16(input)
            input = Inc16(input)
        ans = sum(c*(2**i) for i,c in enumerate(input[::-1]))
        if(makeNeg):
            return -ans
        return ans
    else:
        return sum(c*(2**i) for i,c in enumerate(input[::-1]))
    
def testALU(): 
    print('Testing ALU')
    
    fn = os.path.join(os.path.dirname(__file__), 'testFiles/chipFiles/alu.tst')
    with open(fn, "r") as ins: 
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
              
def testMemory():
    print('Testing Memory')
    mem = Memory()  
    desiredAnswers = []
    myAnswers = []
    fn = os.path.join(os.path.dirname(__file__), 'testFiles/chipFiles/memory.tst')
    with open(fn, "r") as ins:
        for line in ins:
            if line[0] != '#':
                parsed = line.strip('\n').replace(' ','').split('|')
                #print(parsed)
                input = decToBin(int(parsed[1]))
                load=int(parsed[2])
                address=decToBin(int(parsed[3]))[-15:]
                out = decToBin(int(parsed[4]))
                myout = mem.access(input,load,address)[:]
                myAnswers.append(myout)
                desiredAnswers.append(out)
    generalTester(desiredAnswers,myAnswers)
        
def testRegister():
    
    print('Testing Register')
    reg = Register()
    desiredAnswers = []
    myAnswers = []
    fn = os.path.join(os.path.dirname(__file__), 'testFiles/chipFiles/register.tst')
    with open(fn, "r") as ins: 
        
        for line in ins:
            if line[0] != '#':
                parsed = line.strip('\n').replace(' ','').split(',')[:-1]
                input = decToBin(int(parsed[1]))
                load = int(parsed[2])
                out = decToBin(int(parsed[3]))
                
                lineAnswer = [out]
                desiredAnswers.append(lineAnswer)
                
                myout = [reg.register(input,load)[:]]
                myAnswers.append(myout)
                
    generalTester(desiredAnswers,myAnswers)

def testRam8():
    print('Testing RAM8')
    ram8 = RAM8()
    desiredAnswers = []
    myAnswers = []
    fn = os.path.join(os.path.dirname(__file__), 'testFiles/chipFiles/ram8.tst')
    with open(fn, "r") as ins: 
        
        for line in ins:
            if line[0] != '#':
                parsed = line.strip('\n').replace(' ','').split(',')[:-1]
                input = decToBin(int(parsed[2]))
                load=int(parsed[3])
                address=decToBin(int(parsed[4]))[-3:]
                out=decToBin(int(parsed[5]))
                lineAnswer = [out]
                desiredAnswers.append(lineAnswer)
                myout = [ram8.access(input,load,address)[:]]
                myAnswers.append(myout)
    generalTester(myAnswers,desiredAnswers)

def testRam64():
    print('Testing Ram64')
    ram = RAM64()
    desiredAnswers = []
    myAnswers = []
    fn = os.path.join(os.path.dirname(__file__), 'testFiles/chipFiles/testRam64.tst')
    with open(fn, "r") as ins: 
        
        for line in ins:
            if line[0] != '#':
                parsed = line.strip('\n').replace(' ','').split('|')[:-1]
                input = decToBin(int(parsed[2]))
                load=int(parsed[3])
                address=decToBin(int(parsed[4]))[-6:]
                out=decToBin(int(parsed[5]))
                lineAnswer = [out]
                desiredAnswers.append(lineAnswer)
                myout = [ram.access(input,load,address)[:]]
                myAnswers.append(myout)
    generalTester(myAnswers,desiredAnswers)

def testRAM16K():
    print('Testing RAM16K')
    ram = RAM16K()
    desiredAnswers = []
    myAnswers = []
    fn = os.path.join(os.path.dirname(__file__), 'testFiles/chipFiles/testRam16k.tst')
    with open(fn, "r") as ins: 
        
        for line in ins:
            if line[0] != '#':
                parsed = line.strip('\n').replace(' ','').split('|')[:-1]
                input = decToBin(int(parsed[2]))
                load=int(parsed[3])
                address=decToBin(int(parsed[4]))[-14:]
                out=decToBin(int(parsed[5]))
                lineAnswer = [out]
                desiredAnswers.append(lineAnswer)
                myout = [ram.access(input,load,address)[:]]
                myAnswers.append(myout)
    generalTester(myAnswers,desiredAnswers)
#testRegister()            

def testDemux8way():
    print('Test Demux8way')
    desiredAnswers = []
    myAnswers = []
    fn = os.path.join(os.path.dirname(__file__), 'testFiles/chipFiles/dmux8way.tst')
    with open(fn, "r") as ins: 
        for line in ins:
            if line[0] != '#':
                parsed = line.strip('\n').replace(' ','').split('|')[:-1]
                input = int(parsed[1])
                select = parsed[2]
                select = [int(i) for i in select]
                answers = [int(i) for i in parsed[3:]]
                output = [i for i in DMux8Way(input,select[::-1])]
                desiredAnswers.append(answers)
                myAnswers.append(output)
    generalTester(myAnswers,desiredAnswers)

def testmux8way16():
    print("Testing Mux8way16")
    desiredAnswers = []
    myAnswers = []
    fn = os.path.join(os.path.dirname(__file__), 'testFiles/chipFiles/mux8way16.tst')
    with open(fn, "r") as ins: 
        for line in ins:
            if line[0] != '#':
                parsed = line.strip('\n').replace(' ','').split('|')[:-1]
                
                inputs = parsed[1:9]
                select = parsed[9]
                actualOut = parsed[10]
                inputs = [[int(i) for i in j]for j in inputs]
                select = [int(i) for i in select]
                actualOut = [int(i) for i in actualOut]
                myOut = Mux8Way16(*inputs,select[::-1])
                desiredAnswers.append(actualOut)
                myAnswers.append(myOut)
                
        generalTester(desiredAnswers,myAnswers)
def testPC():
    print('Testing PC')
    desiredAnswers = []
    myAnswers = []
    pc = PC()
    fn = os.path.join(os.path.dirname(__file__), 'testFiles/chipFiles/testPC.tst')
    with open(fn, "r") as ins: 
        for line in ins:
            if line[0] != '#':
                parsed = line.strip('\n').replace(' ','').split('|')[2:-1]
                
                input = int(parsed[0])
                reset = int(parsed[1])
                load = int(parsed[2])
                inc = int(parsed[3])
                out = int(parsed[4])
                myout = pc.register(decToBin(input),load,inc,reset)
                
                desiredAnswers.append([out])
                myAnswers.append([binToDec(myout)])
    generalTester(desiredAnswers,myAnswers)
    
def testBit():
    print("Testing Bit")
    bit = Bit()
    desiredAnswers = []
    myAnswers = []
    flipFlop = False
    fn = os.path.join(os.path.dirname(__file__), 'testFiles/chipFiles/bit.tst')
    with open(fn, "r") as ins: 
        badCount = 0
        for line in ins:
            if line[0] != '#':
                parsed = line.strip('\n').replace(' ','').split('|')
                input = int(parsed[2]) 
                load = int(parsed[3])
                out = int(parsed[4])
                myout = bit.register(input,load)
                desiredAnswers.append([out])
                myAnswers.append([myout])

    generalTester(desiredAnswers,myAnswers)

def testAll():
    
    testPC()
    testALU()
    testRegister()
    testMemory()
    testRam8()
    testMemory()
    testmux8way16()
    testDemux8way()
    testRam64()
    testBit()
    print('All Chips Tested')
