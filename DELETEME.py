#from WorkingTests import generalTester, decToBin, binToDec
#from Chips import PC
import pyComp,os
from pyComp.Test_Suite.WorkingTests import decToBin,binToDec,generalTester
class TEMPPC:
    #16 bit counter with load and reset controls
    #if reset(t) then out(t+1) = 0
    #else if load(t) then out(t+1) = in(t)
    #else if inc(t) then out(t+1) = out(t)+1 (integer addition)
    #else out(t+1) = out(t)
    def __init__(self):
        self.stored = [0]*16
        self.skip = False
        
    def register(self,input,load,inc,reset):
        stored_value = self.stored[:]
        if(not self.skip):
            self.skip = True
            value_to_store = self.stored[:]
            
            if(reset is 1):
                value_to_store = [0]*16
            elif(load is 1):
                value_to_store = input
            elif(inc is 1):
                value_to_store = decToBin(binToDec(value_to_store)+1)
            
            self.stored = value_to_store
        else:
            self.skip = False
        return stored_value
    
    
def testPC():
    print('testPC')
    desiredAnswers = []
    myAnswers = []
    pc = TEMPPC()
    #pc = PC()
    fn = os.path.join(os.path.dirname(__file__), 'pyComp/Test_Suite/testFiles/chipFiles/testPC.tst')
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
                print('input:',input,'reset:',reset,'load:',load,'inc:',inc,'out:',out,'myOut:',binToDec(myout))
                desiredAnswers.append([out])
                myAnswers.append([binToDec(myout)])
    generalTester(desiredAnswers,myAnswers)
