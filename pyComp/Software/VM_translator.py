#reads in all VM files in a given directory (the first argument passed),
#outputs assembly code to STDOUT
import sys
from os import listdir
from os.path import isfile, join

class Parser:
    
    def __init__(self,folderPath):
        
        self.UniqueLabelID = 0
        #list of files in the given directory
        fileNames = [f for f in listdir(folderPath) if (isfile(join(folderPath, f)) and f.endswith('.vm'))]
        
        #if Sys is in our file folder, bootstrap Sys.init call
        if 'Sys.vm' in fileNames:
            self.writeInit()
        
        #a file was specified, open it and write our assembly code
        for fileName in fileNames:
            self.fileName = fileName
            with open(join(folderPath, fileName)) as f:
                for read_line in f:
                    #remove newlines
                    line = read_line.strip('\n')
                    
                    #removes comments
                    line = line.split('//')[0]
                    
                    #ignores blank lines 
                    if line != '':
                        
                        self.buildLine(line)
       
                
                
                
    def arg1(self,line):
        parts = line.split(' ')
        if(self.commandType(line) == 'arithmetic'):
            return parts[0]
        else:
            return parts[1]
    
    def arg2(self,line):
        parts = line.split(' ')
        return int(parts[2])
                            
                    
    def buildLine(self,line):
        c = self.commandType(line)
        if(c == 'push' or
            c == 'pop'):
            self.writePushPop(line)
            
        if c == 'arithmetic':
            self.writeArithmetic(line)
        
        if c == 'label':
            self.writeLabel(self.arg1(line))
        if c == 'goto':
            self.writeGoto(self.arg1(line))
        
        if c == 'function':
            self.writeFunction(self.arg1(line),self.arg2(line))
        if c == 'if':
            self.writeIf(self.arg1(line))
        if c == 'return':
            self.writeReturn()
        if c == 'call':
            self.writeCall(self.arg1(line),self.arg2(line))
        
    
    def commandType(self,line):
        if 'push' in line     : return 'push';
        if 'pop' in line      :  return 'pop';
        if 'label' in line    : return 'label';
        if 'if' in line       : return 'if';
        if 'goto' in line     : return 'goto';
        if 'function' in line : return 'function';
        if 'return' in line   : return 'return';
        if 'call' in line     : return 'call';
        
        return 'arithmetic';
    
    def writeArithmetic(self,line):
        #add, sub, neg, eq, gt, lt, and, or not
        print("@SP")
        print("M=M-1")
        print("A=M")
        print("D=M")
        print("M=0")
        parsed = line.replace(' ','')
        #D is now the top number in stack. sp points to blank "top of stack"
        if('add' in parsed):
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("M=M+D")
        
        if('sub' in parsed):
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("M=M-D")
        
        if('neg' in parsed):
            print("M=-D")
        
        if('eq' in parsed or 
            'gt' in parsed or 
            'lt' in parsed):
            #equal to, greater than, or less than by subtracting D and M
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M-D") #D has the stack subtraction
            print("@LogicWasTrue"+str(self.UniqueLabelID))
            self.writeLogicTest(parsed)
            print("@SP")
            print("A=M")
            print("M=0")
            print("@EndLogic"+str(self.UniqueLabelID))
            print("0;JMP")
            print("(LogicWasTrue"+str(self.UniqueLabelID)+")")
            print("@SP")
            print("A=M")
            print("M=-1")
            print("(EndLogic"+str(self.UniqueLabelID)+")")
            self.UniqueLabelID+=1
       
        if('and' in parsed):
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("M=M&D")
        
        if('or' in parsed):
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("M=M|D")
        
        if('not' in parsed):
          print("M =!D")
        
        #increments SP, to tpoint to blank part of top of stack
        print("@SP")
        print("M=M+1")
        print("A=M")
    
    def writeLogicTest(self,logic):
        if logic == 'eq':
            print("D;JEQ")
        elif logic =='gt':
            print("D;JGT")
        elif logic == 'lt':
            print("D;JLT")
            
    def writePushPop(self,line):
        if self.commandType(line) == 'push':
            #pushes a variable onto the stack
            if(self.arg1(line) == "constant"):
                #if pushing a constant...
                print("@"+str(self.arg2(line)))
                print("D=A")
                print("@SP")
                print("M=M+1")
                print("A=M-1")
                print("M=D")
                return
            
            if(self.arg1(line) == 'static'):
                print("@"+self.fileName+"."+str(self.arg2(line)))
                print("D=M")
                print("@SP")
                print("M=M+1")
                print("A=M-1")
                print("M=D")
                return
        
            
            #pushing some value in a location onto the stack
            print("@"+str(self.arg2(line))) #A = index of segment
            print("D=A")
            arg1 = self.arg1(line)
            
            if(arg1 == "argument") : print("@ARG")
            if(arg1 == "local")    : print("@LCL")
            if(arg1 == "this")     : print("@THIS")
            if(arg1 == "that")     : print("@THAT")
            if(arg1 == "pointer")  : print("@THIS")
            if(arg1 == "temp")     : print("@5")
            
            if(arg1 == "temp" or arg1 == "pointer"):
                print("A=A+D")
            else:
                print("A=M+D")
            
            print("D=M")
            print("@SP")
            print("A=M")
            print("M=D")
            
            #pushed onto stack, now increment sp
            print("@SP")
            print("M=M+1")
            print("A=M")
            
            return
        else:
            #command was a pop command
            
            #pops the current value into D
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M")
            print("M=0")
            
            # find the storage location and store D into it
            arg1 = self.arg1(line)
            if(arg1 == "argument") : print("@ARG")
            if(arg1 == "local")    : print("@LCL")
            if(arg1 == "this")     : print("@THIS")
            if(arg1 == "that")     : print("@THAT")
            if(arg1 == "pointer")  : print("@THIS")
            if(arg1 == "temp")     : print("@5")
            if(arg1 == "static"):
                print("@"+self.fileName+"."+str(self.arg2(line)))
                print("M=D")
                return
            
            if(not (arg1 == "temp" or arg1 == "pointer")):
                print("A=M")
            for i in range(self.arg2(line)):
               print("A=A+1") #finds the index inside the segment needed
            
            print("M=D")
        return
    
    def writeLabel(self,label):
        print('('+self.fileName+"$"+label+')')

    def writeInit(self):
        print('@256')
        print('D=A')
        print('@SP')
        print('M=D')
        self.writeCall('Sys.init',0)
        
    def writeGoto(self,label):
        print('@'+self.fileName+'$'+label)
        print("0;JMP")
    
    def writeIf(self,label):
        print("@SP")
        print("M=M-1")
        print("A=M")
        print("D=M")
        print("M=0")
        #if D==0 continue on, otherwise jump to the requesteddestination
        print("@gotoif."+str(self.UniqueLabelID))
        print("D;JEQ")
        print("@"+self.fileName+"$"+label)
        print("0;JMP")
        print("(gotoif."+str(self.UniqueLabelID)+")")
        self.UniqueLabelID+=1
        
    def writeCall(self,functionName,numArgs):
        # before this is called n arguments should have been pushed onto stack
        #
        #push a return address using label declared at bottom 
        print("@returnNum"+str(self.UniqueLabelID))
        print("D=A")
        print("@SP")
        print("M=M+1")
        print("A=M-1")
        print("M=D")
        #push lcl
        print("@LCL")
        self.pushM()
        #push arg
        print("@ARG")
        self.pushM()
        #push this
        print("@THIS")
        self.pushM()
        #push that
        print("@THAT")
        self.pushM()
        #arg = SP-n-5 (n is the number of arguments for the new function
        print("@SP")
        print("D=M")
        print("@"+str(5+numArgs))
        print("D=D-A")
        print("@ARG")
        print("M=D")
        #lcl = sp
        print("@SP")
        print("D=M")
        print("@LCL")
        print("M=D")
        #goto f (the function)
        print("@"+functionName)
        print("0;JMP")
        #(return address label)
        print("(returnNum"+str(self.UniqueLabelID)+")")
        self.UniqueLabelID+=1
        
    def pushM(self):
        print("D=M")
        print("@SP")
        print("M=M+1")
        print("A=M-1")
        print("M=D")
    
    def writeReturn(self):
        #FRAME = LCL
        print("@LCL")
        print("D=M")
        print("@FRAME")
        print("M=D")
        
        # RET = *(Frame-5)
        print("@5")
        print("D=A")
        print("@FRAME")
        print("A=M-D")
        print("D=M") #D not has the return address saved
        print("@RET")
        print("M=D")
        
        #*ARG = pop()
        print("@SP")
        print("A=M-1")
        print("D=M") #d is the return value now
        print("M=0")
        print("@ARG")
        print("A=M")
        print("M=D")
        
        #SP = ARG+1
        print("@ARG")
        print("D=M+1")
        print("@SP")
        print("M=D")
        
        #that = *(frame-1)
        print("@1")
        print("D=A")
        print("@FRAME")
        print("A=M-D")
        print("D=M") 
        print("@THAT")
        print("M=D")
        
        #this = *(frame-2)
        print("@2")
        print("D=A")
        print("@FRAME")
        print("A=M-D")
        print("D=M") 
        print("@THIS")
        print("M=D")
        
        #arg = *(frame-3)
        print("@3")
        print("D=A")
        print("@FRAME")
        print("A=M-D")
        print("D=M") 
        print("@ARG")
        print("M=D")
        
        #lcl = *(frame-4)
        print("@4")
        print("D=A")
        print("@FRAME")
        print("A=M-D")
        print("D=M") 
        print("@LCL")
        print("M=D")
        
        #go to RET
        print("@RET")
        print("A=M")
        print("0;JMP")
        
    def writeFunction(self,functionName,numLocals):
        #label f (the function)
        print('('+functionName+')')
        for i in range(numLocals):
            print('@SP')
            print('M=M+1')
            print('A=M-1')
            print('M=0')
        
if __name__ == "__main__":
    if(len(sys.argv)<2):
        print('no folder path given!')
    else:
        Parser(sys.argv[1])
