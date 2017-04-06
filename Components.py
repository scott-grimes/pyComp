from Chips import *
class ROM():
    pass

class CPU:
    def __init__(self):
        self.ARegister = Register()
        self.PC = PC()
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
        
        #if "instruction" is a command set A to old outM, else set A to instruction
        #Mux1
        internalOutM = self.internalOutM[:]
        isZero = self.isZero
        isNegative = self.isNeg
        muxed1 = Mux16(instruction, internalOutM, instruction[0])
    
        #A Register
        #if instruction is a function and instruction5 is true, use A not M
        #if instruction is an address use A not M
        functionAndAWrite = And(instruction[0], instruction[10])#was instruction 5
        isConstant = Not(instruction[0])
        loadA = Or(functionAndAWrite, isConstant)
        aout = self.ARegister.register(muxed1, loadA)
        A = aout[:]
        addressM = aout[1::]
    
        #Mux AorM if we instruction is a function and if "a" ==1, use a
        useA = And (instruction[0], b=instruction[3]) #was 3
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
    
        pcout = self.PC.register(A, reset, noJump, jump)
        pc = pcout[1::] #was 0..14
    
        #D Register
        loadD = And(instruction[11],instruction[0]) #was 4,15
        D = self.DRegister.register(internalOutM, loadD)
     
        #ALU
        outM,zr,ng = ALU(D,AorM,instruction[4],
                                instruction[5], 
                                instruction[6], 
                                instruction[7],
                                instruction[8], 
                                instruction[9])
        internalOutM = outM[:]
    
        #if write to m ==1 and if instruction is a command writem=1
        writeM = And(instruction[12],instruction[0])
        self.internalOutM = internalOutM[:]
        self.isZero = zr
        self.isNeg = ng
        
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

