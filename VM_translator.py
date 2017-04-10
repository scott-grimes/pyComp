#reads in a VM file from stdin, outputs assembly code to stdout
import sys

class Parser:
    
    def __init__(self):
        self.lineNumber = 0
        self.fileName = 'fileName'
        #gets the line number of each user-defined symbol
        #and adds it to our symbol/address dictionary
        
        for read_line in sys.stdin:
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
        
   
    
    def commandType(self,line):
        if 'push' in line     : return 'push';
        if 'pop' in line      :  return 'pop';
        if 'label' in line    : return 'label';
        if 'goto' in line     : return 'goto';
        if 'function' in line : return 'function';
        if 'if' in line       : return 'if';
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
        
        if('("neg' in parsed):
            print("M=-D")
        
        if('eq' in parsed or 
            'gt' in parsed or 
            'lt' in parsed):
            #equal to, greater than, or less than by subtracting D and M
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M-D") #D has the stack subtraction
            print("@LogicWasTrue"+str(UniqueLabelID))
            writeLogicTest(parsed)
            print("@SP")
            print("A=M")
            print("M=0")
            print("@EndLogic"+str(UniqueLabelID))
            print("0JMP")
            print("(LogicWasTrue"+str(UniqueLabelID)+")")
            print("@SP")
            print("A=M")
            print("M=-1")
            print("(EndLogic"+str(UniqueLabelID)+")")
            UniqueLabelID+=1
       
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
            
            if(arg1 != "temp" or arg1 == "pointer"):
                print("A=M")
            for i in range(self.arg2(line)):
               print("A=A+1") #finds the index inside the segment needed
            
            print("M=D")
        return

if __name__ == "__main__":
        Parser()
