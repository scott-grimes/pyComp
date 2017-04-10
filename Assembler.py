
class Parser:
    
    def buildSymbolsFromLineNumbers(self,fileName):
        with open(fileName) as f:
            for line in f:
                #remove whitespace and newlines
                line = line.strip('\n').replace(' ','')
                
                #removes comments
                line = line.split('//')[0]
                
                #ignores blank lines 
                if line != '':
                    if line[0]=='(':
                        #if line is a label, adds our lineNumber
                        symbol = line[1:-1]
                        self.code.makeNewAddress(symbol,self.lineNumber)        
                    else:
                        self.lineNumber+=1    
                                
    def __init__(self,fileName):
        self.lineNumber = 0
        self.code = Code()
        self.buildSymbolsFromLineNumbers(fileName)
        print(self.code.symbolDict)
        with open(fileName) as f:
            for line in f:
                #remove whitespace and newlines
                line = line.strip('\n').replace(' ','')
                
                #removes comments
                line = line.split('//')[0]
                
                #ignores blank lines 
                if line != '' and line[0]!='(':
                    print(self.buildLine(line))
                            
                    
    def buildLine(self,line):
        c = self.commandType(line)
        if c=='A':
            return '0'+self.symbol(line)
        elif c=='C':
            return '111'+self.comp(line)+self.dest(line)+self.jump(line)
        else:
            self.symbol(line)
    
    
    def commandType(self,line):
        if line[0]=='@':
            return 'A'
        if line[0]=='(':
            return 'L'
        return 'C'
    
    def symbol(self,line):
        address = ''
        if line[1].isdigit():
            binary_number = bin(int(line[1:]))[2:]
            address+=binary_number
        else:
            address+=str(bin(self.code.getAddress(line[1:]))[2:])
        while(len(address)<15):
            address = '0'+address
        return address
    
    def dest(self,line):
        d = ''
        if '=' in line:
            d = line.split('=')[0]
        return self.code.dest(d)
    
    def comp(self,line):
        d = ''
        if '=' in line:
            d = line.split('=')[1]
        if ';' in line:
            d = line.split(';')[0]
        return self.code.comp(d)
        
    def jump(self,line):
        jump = ''
        if ';' in line:
            jump = line.split(';')[1]
        return self.code.jump(jump)
    
class Code:
    
    def __init__(self):
        self.numberOfNewVars = 0
        self.symbolDict = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576,
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15
        }
        
    def makeNewAddress(self,symbol,address):
        self.symbolDict[symbol] = address
        
    def getAddress(self,symbol):
        if symbol not in self.symbolDict:
            self.makeNewAddress(symbol,16+self.numberOfNewVars)
            self.numberOfNewVars+=1
        return self.symbolDict[symbol]
        
    def dest(self,mnemonic):
        d=''
        d+='1' if 'A' in mnemonic else '0'
        d+='1' if 'D' in mnemonic else '0'
        d+='1' if 'M' in mnemonic else '0'
        return d
    
    def comp(self,mnemonic):
        
        if (mnemonic=="0")     : return "0101010" 
        elif (mnemonic=="1")   : return "0111111" 
        elif (mnemonic=="-1")  : return "0111010" 
        elif (mnemonic=="D")   : return "0001100" 
        elif (mnemonic=="A")   : return "0110000" 
        elif (mnemonic=="!D")  : return "0001101" 
        elif (mnemonic=="!A")  : return "0110001" 
        elif (mnemonic=="-D")  : return "0001111" 
        elif (mnemonic=="-A")  : return "0110011" 
        elif (mnemonic=="D+1") : return "0011111" 
        elif (mnemonic=="A+1") : return "0110111" 
        elif (mnemonic=="D-1") : return "0001110" 
        elif (mnemonic=="A-1") : return "0110010" 
        elif (mnemonic=="D+A") : return "0000010" 
        elif (mnemonic=="D-A") : return "0010011" 
        elif (mnemonic=="A-D") : return "0000111" 
        elif (mnemonic=="D&A") : return "0000000" 
        elif (mnemonic=="D|A") : return "0010101" 
        elif (mnemonic=="M")   : return "1110000" 
        elif (mnemonic=="!M")  : return "1110001" 
        elif (mnemonic=="-M")  : return "1110011" 
        elif (mnemonic=="M+1") : return "1110111" 
        elif (mnemonic=="M-1") : return "1110010" 
        elif (mnemonic=="D+M") : return "1000010" 
        elif (mnemonic=="D-M") : return "1010011" 
        elif (mnemonic=="M-D") : return "1000111" 
        elif (mnemonic=="D&M") : return "1000000" 
        elif (mnemonic=="D|M") : return "1010101" 
        else:                    return "0000000"
        
    def jump(self,mnemonic):
        if(mnemonic=="JGT") : return "001"
        if(mnemonic=="JEQ") : return "010"
        if(mnemonic=="JGE") : return "011"
        if(mnemonic=="JLT") : return "100"
        if(mnemonic=="JNE") : return "101"
        if(mnemonic=="JLE") : return "110"
        if(mnemonic=="JMP") : return "111"
        return "000"
        
#Parser('testFiles/assemblerFiles/Max.asm')
#Parser('testFiles/assemblerFiles/add.asm')
#Parser('testFiles/assemblerFiles/MaxL.asm')
#Parser('testFiles/assemblerFiles/Rect.asm')
#Parser('testFiles/assemblerFiles/RectL.asm')
Parser('testFiles/assemblerFiles/PongL.asm')
