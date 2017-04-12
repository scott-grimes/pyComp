#this does some shit 
import sys
from sympy.core.numbers import IntegerConstant
class syntaxAnalyzer:
    
    
    
    def __init__(self,file_with_path):
        self.keywords = ['class',
        'constructor',
        'function',
        'method',
        'field','static',
        'var',
        'int','char','boolean','void',
        'true','false','null',
        'this','let','do','if','else',
        'while','return'
        ] 
    
        self.symbols = ['(',')','{','}','[',']',
        '.',',',';','+','-','*','/','&','|',
        '<','>','=','~']
        
        self.lines = []
        
        fileName = file_with_path.split('\\')[-1]
        
        with open(file_with_path) as f:
            
            for line in f:
                #replaces tabs with single spaces
                line = line.replace('\t',' ')
                #removes comments with two slashes
                line = line.split('//')[0]
                #ignore blank lines
                if line != '':
                    self.lines.append(line)
        #joins the lines together into one big string
        inputStream = ''.join(self.lines)
        
        #number of comments remaining in the file
        numberOfComments = inputStream.count('/*')
        #removes remaining comments
        while(numberOfComments>0):
            before = inputStream.split('/*',1)[0]
            after = inputStream.split('*/',1)[1]
            inputStream = before+after
            numberOfComments-=1
        
        #removes newlines
        self.inputStream = inputStream.replace('\n',' ')
        
        #replaces all groups of whitespace with single whitespaces
        #inputStream = ' '.join(inputStream.split())
        while(self.hasMoreTokens()):
            token = self.advance()
            type = self.tokenType(token)
            print(type,':',token)
        pass
    
    def hasMoreTokens(self):
        return (len(self.inputStream.replace(' ',''))>0)
    
    def advance(self):
        #returns the next token
        
        #removes leading whitespace
        self.inputStream = self.inputStream.lstrip()
        
        #checks to see if we are looking at a string (leading char is \")
        if self.inputStream[0] == "\"":
            closing_index = self.inputStream.index("\"",1) 
            token = self.inputStream[:closing_index+1]
            self.inputStream = self.inputStream[len(token):]
            return token
        
        #checks to see if we are looking at a symbol
        if self.inputStream[0] in self.symbols:
            token = self.inputStream[0]
            self.inputStream=self.inputStream[1:]
            return token
        
        #gets a potential token, read up to the next whitespace character
        #this potential token requires further parsing as it might contain a symbol inside, which
        #should delimit the token instead of the whitespace
        
        potential_token= self.inputStream.split(' ',1)[0]
        foundInside = [i for i in self.symbols if i in potential_token]
        
        #if there is a symbol inside, use it to delimit our symbol
        if len(foundInside)>0:
            for i in foundInside:
                potential_token = potential_token.split(i,1)[0]
        
        #chops out the token from our input stream and returns it
        token = potential_token
        self.inputStream = self.inputStream[len(token):].lstrip()
        return token
        
            
    def tokenType(self,token):
        #returns the type of token we have obtained
        if token[0] == "\"":
            return 'StringConstant'
        
        if token in self.keywords:
            return 'keyword'
        if token in self.symbols:
            return 'symbol'
        if token[0].isdigit():
            return 'IntegerConstant'
        
        return 'identifier'
        
    
    def JackAnalyzer(self):
        pass
    
    def JackTokenizer(self):
        pass
    
    def CompilationEngine(self):
        pass
    
if __name__ == "__main__":
    try:
        if(len(sys.argv)<2):
            print('No input file specified!')
        else:
            syntaxAnalyzer(sys.argv[1])
    except Exception as e:
        print(e)
        input()
        sys.exit()