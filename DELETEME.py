#from WorkingTests import generalTester, decToBin, binToDec
#from Chips import PC
import pyComp,os,sys
from pyComp.Test_Suite.WorkingTests import decToBin,binToDec,generalTester
from pyComp.Hardware.Chips import *
from pyComp.Hardware.Components import *
from pyComp.Software.syntaxAnalyzer import *

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
    
class CPU:
    def __init__(self):
        self.PC = PC()
        self.ARegister = Register()
        self.DRegister = Register()
        self.internalOutM = [0]*16
        self.isZero = 0
        self.isNeg = 0
        
        
    def instruct(self,inM,instruction,reset):
        """
        IN  inM[16],         // M value input  (M = contents of RAM[A])
            instruction[16], // Instruction for execution
            reset;           // Signals whether to re-start the current program
                             // (reset == 1) or continue executing the current
                             // program (reset == 0).
    
        OUT outM[16],        // M value output
            writeM,          // Write into M? 
            addressM[15],    // RAM address (of M)
            pc[15];          // ROM address (of next instruction)
        """
       
        #fetch the last CPU executions values
        internalOutM = [i for i in self.internalOutM]
        isZero = self.isZero
        isNegative = self.isNeg
        
        #if bit[0] is 1 set A to old internalOutM, otherwise set A to instruction
        #Mux1
        muxed1 = Mux16(instruction, internalOutM, instruction[0])
    
        #A Register
        #if bit[0] is 1 and bit[5] is true, use A not M
        #if instruction is an address use A not M
        functionAndAWrite = And(instruction[0], instruction[10])#was instruction 5
        isConstant = Not(instruction[0])
        loadA = Or(functionAndAWrite, isConstant)
        aout = self.ARegister.register(muxed1, loadA)
        
        A = [i for i in aout]
        addressM = [i for i in aout][1:]
        #print('addressM',binToDec(addressM,True))
        #Mux AorM if we instruction is a function and if "a" ==1, use a
        useA = And (instruction[0], instruction[3]) #was 12
        AorM = Mux16(A, inM, useA)
        
        
        #PC
        #incriment if we're not jumping, load if we are jumping
        isNotPos = Or(isZero,isNegative)
        isPos = Not(isNotPos)
    
        jlt = And(isNegative, instruction[13]) #was 2
        jeq = And(isZero,instruction[14]) #was 1
        jgt = And(isPos, instruction[15]) #was 0
       
        oneOr = Or(jlt, jeq)
        hasJump = Or(oneOr, jgt)
        jump = And(instruction[0], hasJump) #was 15
        noJump = Not(jump)
                                #input,load,inc,reset
        pcout = self.PC.register(A, jump, noJump, reset)
        pc = [i for i in pcout][1:] #was 0..14
        
        
        
        #D Register
        loadD = And(instruction[11],instruction[0]) #was 4,15
        D = self.DRegister.register(internalOutM, loadD)
        
        #IN:X,Y,zx,nx,zy,ny,f,no
        #OUT: out,zr,ng
        #ALU
        outM,isZero,isNegative = ALU(D,AorM,instruction[4],
                                instruction[5], 
                                instruction[6], 
                                instruction[7],
                                instruction[8], 
                                instruction[9])
        
        self.internalOutM = [i for i in outM]
        self.isZero = isZero
        self.isNeg = isNegative
        
        
        #if write to m == 1 and if instruction is a command writem=1
        writeM = And(instruction[12],instruction[0])
        """
        print()
        print('internalOutM',binToDec(internalOutM))
        print('muxed1',binToDec(muxed1))
        print('functionAndAWrite',functionAndAWrite)
        print('isConstant',isConstant)
        print('loadA',loadA)
        print('A',binToDec(A))
        print('useA',useA)
        print('AorM',binToDec(AorM))
        print('isZero',isZero)
        print('isNegative',isNegative)
        print('isNotPos',isNotPos)
        print('jlt',jlt)
        print('jeq',jeq)
        print('jgt',jgt)
        print('oneOr',oneOr)
        print('hasJump',hasJump)
        print('noJump',noJump)
        print('loadD',loadD)
        print('D',binToDec(D))
        print()
        """
        print('A',binToDec(A),' D',binToDec(D))
        return outM, writeM,addressM,pc
    
def testCPU():
    cpu = CPU()
    desiredAnswers = []
    myAnswers = []
    fn = os.path.join(os.path.dirname(__file__), 'pyComp/Test_Suite/testFiles/chipFiles/cpu.tst')
    
    with open(fn, "r") as ins: 
        badCount = 0
        for line in ins:
            if line[0] != '#':
                parsed = line.strip('\n').replace(' ','').split(',')[:-1]
                #inM  ,  instruction   ,reset, outM  ,writeM ,addre, pc  ,DRegiste,
                inM = int(parsed[1])
                inM = decToBin(inM)
                
                instruction = [int(i) for i in parsed[2]]
                
                rest = int(parsed[3])
                
                outM = parsed[4]
                
                writeM = int(parsed[5])
                
                addre = int(parsed[6])
                
                pc  = int(parsed[7])
                
                DRegister = int(parsed[8])
                
                myoutM, myWriteM,myaddressM,Mypc = cpu.instruct(inM,instruction,rest) #
                MyD = cpu.DRegister.out
                myoutM = binToDec(myoutM)
                
                myaddressM = binToDec(myaddressM,True)
                
                MyD = binToDec(MyD)
                
                Mypc = binToDec(Mypc,True)
                if(outM!="*******"):
                    outM=int(outM)
                    
                correctanswers = [outM,writeM,addre,pc,DRegister]
                myanswers = [myoutM,myWriteM,myaddressM,Mypc,MyD]
                print(correctanswers,myanswers)
               
                
                    
                
                desiredAnswers.append(correctanswers)
                myAnswers.append(myanswers)
    generalTester(desiredAnswers,myAnswers)
        
"""
vm_names = ['BasicTest','PointerTest','SimpleAdd','StackTest','StaticTest']
for VMNAME in vm_names:
    pre = 'pyComp/Test_Suite/testFiles/vmFiles/'
    fn = os.path.join(os.path.dirname(__file__), pre+VMNAME+'.vm')
    
    sys.stdout=open(VMNAME+'.asm',"w")
    vm(fn,VMNAME)
    sys.stdout.close()
"""
"""
folderNames = ['1_BasicLoop','2_FibonacciSeries','3_SimpleFunction','4_FibonacciElement','5_StaticsTest']
prefix = 'pyComp/Test_Suite/testFiles/advancedVMFiles/'
for folder in folderNames:
    fn = os.path.join(os.path.dirname(__file__), prefix+folder)
    
    sys.stdout=open(folder[2:]+'.asm',"w")
    vm(fn)
    sys.stdout.close()
"""
prefix = 'pyComp/Test_Suite/testFiles/syntaxAnalyzerFiles/ArrayTest/'
fileName = 'Main.jack' 
CompileJack(prefix+fileName)

