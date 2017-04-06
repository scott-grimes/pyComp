from Chips import *
from Gates import *
from Components import *
from scipy.stats.morestats import ansari

def generalTester(desired_outputs,my_outputs):
    badcount = 0
    for i,j in zip(desired_outputs,my_outputs):
        for a,b in zip(i,j):
            if(a!=b):
                badcount+=1
                print(i,j)
                
    print('I had '+str(badcount)+' incorrect answers')
    

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

def binToDec(input):
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
    

def testALU():
    with open("testFiles/alu.tst", "r") as ins: 
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

def testCPU():
    cpu = CPU()
    desiredAnswers = []
    myAnswers = []
    with open("testFiles/cpu.tst", "r") as ins: 
        badCount = 0
        for line in ins:
            if line[0] != '#':
                parsed = line.strip('\n').replace(' ','').split(',')[:-1]
                inM = int(parsed[1])
                inM = decToBin(inM)
                instruction = [i for i in parsed[2]]
                rest = int(parsed[3])
                outM = parsed[4]
                writeM = parsed[5]
                addre = parsed[6]
                pc  = parsed[7]
                DRegister = parsed[8]
                myoutM, myWriteM,myaddressM,Mypc = cpu.instruct(inM,instruction,rest) #
                myoutM = binToDec(myoutM)
                myaddressM = binToDec(myaddressM)
                Mypc = binToDec(Mypc)
                correctanswers = [outM,writeM,addre,pc]
                myanswers = [myoutM,myWriteM,myaddressM,Mypc]
                desiredAnswers.append(correctanswers)
                myAnswers.append(myanswers)
    generalTester(desiredAnswers,myAnswers)
                
def testMemory():
    mem = Memory()  
    desiredAnswers = []
    myAnswers = []
    with open("testFiles/memory.tst", "r") as ins:
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
    print('testing register')
    reg = Register()
    desiredAnswers = []
    myAnswers = []
    with open("testFiles/register.tst", "r") as ins: 
        
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
    ram8 = RAM8()
    desiredAnswers = []
    myAnswers = []
    with open("testFiles/ram8.tst", "r") as ins: 
        
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
#testRegister()               

def testRam64():
    ram = RAM64()
    desiredAnswers = []
    myAnswers = []
    with open("testFiles/testRam64.tst", "r") as ins: 
        
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
    ram = RAM16K()
    desiredAnswers = []
    myAnswers = []
    with open("testFiles/testRam16k.tst", "r") as ins: 
        
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
    
    desiredAnswers = []
    myAnswers = []
    with open("testFiles/dmux8way.tst", "r") as ins: 
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
    desiredAnswers = []
    myAnswers = []
    with open("testFiles/mux8way16.tst", "r") as ins: 
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
                
    #generalTester(myAnswers,desiredAnswers)

