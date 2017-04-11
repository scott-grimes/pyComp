from .Chips import *
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
    
class ROM():
    pass

class CPUOLD:
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
        aout = self.ARegister.register(muxed1, loadA)[:]
        
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
        D = self.DRegister.register(internalOutM, loadD)[:]
        
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
        print('A',binToDec(A),' D',binToDec(D),)
        return outM, writeM,addressM,pc

class Memory():
    #in in[16], load, address[15]
    #out out[16]
    def __init__(self,debug = True):
        if(debug):
            self.ram = FASTRAM(24577)
        else:
            #implement built in chip memory here
            pass
        
    def access(self,input,load,address):
        return self.ram.access(input,load,address)

