#reads in a .jack file, compiles it into a .vm file, prints the results to stdout
import sys

class Analyzer:
    
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
        
        #redirects stdout to our file
        outputFile = file_with_path.replace('.jack','.vm')
        #sys.stdout=open(outputFile,"w")
       
    def hasMoreTokens(self):
        return (len(self.inputStream.replace(' ',''))>0)
    
    def advance(self):
        #returns the next token. If no tokens left,
        #returns None
        
        if(not self.hasMoreTokens()):
            return None
        
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
    
    def peek(self):
        #returns the next symbol without removing it from the stream
        if(not self.hasMoreTokens()):
            return None
        token = self.advance()
        self.inputStream = token+" "+self.inputStream
        return token
            
    def tokenType(self,token):
        #returns the type of token we have obtained
        
        if token[0] == "\"":
            return 'stringConstant'
        
        if token in self.keywords:
            return 'keyword'
        if token in self.symbols:
            return 'symbol'
        if token[0].isdigit():
            return 'integerConstant'
        
        
        return 'identifier'
        
    def keyWord(self,token):
        #returns the keyword of the current 
        #token
        return token

    def intVal(self,token):
        return int(token)
    
    def stringVal(self,token):
        return token[1:-1] #strips the quotes off of our token
        
class CompileJack:
    
    def __init__(self,file_with_path):
        self.fetch = Analyzer(file_with_path)
        self.indent = 0
        self.CompileClass()
        return
    
    def print_tag(self,tag): 
        for i in range(self.indent):
            print('  ',end='')
        print(tag)
        
        
    def xml_ify(self,token):
        #replaces the characters <,>,",and " with their xml equivalants
        token = token.replace("&",'&amp;')
        token = token.replace('<','&lt;')
        token = token.replace('>','&gt;')
        token = token.replace("\"",'&quot;')
        return token
    
    def out(self,token):
        #prints out the parsed XML line
        
        #indent for readability
        for i in range(self.indent):
            print('  ',end='')
            
        #check if we have an int
        if(isinstance( token, int )):
           type = self.fetch.tokenType(str(token))
           print("<"+type+"> "+str(token)+" </"+type+">")
        
        #we have a string
        else:
            type = self.fetch.tokenType(token)
            
            #remove quotes form string constants, otherwise just print the type and string
            if type == 'stringConstant':
                token = self.fetch.stringVal(token)
                
            #removes non-xml-compatable characters from our token
            token = self.xml_ify(token)
            print("<"+type+"> "+token+" </"+type+">")
        
    
    def CompileClass(self):
        self.print_tag('<class>')
        self.indent +=1
        f = self.fetch
        token = f.advance()
        self.out(token) #class keyword
        token = f.advance()
        self.out(token) #class name
        token = f.advance()
        self.out(token) #{
        
        peek = f.peek() #class Var Dec
        while(peek in ['static','field']):
            self.CompileClassVarDec()
            peek = f.peek()
        
        #class subroutine Dec
        while(peek in ['constructor','function',
                    'method','void']):
            self.CompileSubroutine()
            peek = f.peek()
            
        token = f.advance()
        self.out(token) #}
        self.indent-=1
        self.print_tag('</class>')
        
        return
    
    def CompileClassVarDec(self):
        self.print_tag('<classVarDec>')
        self.indent +=1
        f = self.fetch
        token = f.advance() #type
        self.out(token)
        token = f.advance() #varName
        self.out(token)
        token = f.advance() #varName or ','
        self.out(token)
        while token != ';':
            token = f.advance() #varName or ',' or ';'
            self.out(token)
        
        
        self.indent -=1
        self.print_tag('</classVarDec>')
        
    def CompileSubroutine(self):
        self.print_tag('<subroutineDec>')
        self.indent +=1
        f = self.fetch
        token = f.advance() #constructor/function/method
        self.out(token)
        token = f.advance() #return type or void
        self.out(token)
        token = f.advance() #subroutineName 
        self.out(token)
        token = f.advance() # '('
        self.out(token)
        
        self.CompileParameterList()
        
        token = f.advance() # ')'
        self.out(token)
        
        self.CompileSubroutineBody()
        
        self.indent -=1
        self.print_tag('</subroutineDec>')
        
        return
    
    def CompileParameterList(self):
        #((type varName)(','type varName)*)?
        self.print_tag('<parameterList>')
        
        self.indent +=1
        f= self.fetch
        peek = f.peek()
        while peek != ')':
            token = f.advance()
            self.out(token) # ',' or type or varName
            peek = f.peek()
        self.indent -=1
        self.print_tag('</parameterList>')
            
    def CompileSubroutineBody(self):
        self.print_tag('<subroutineBody>')
        self.indent +=1
        f = self.fetch
        token = f.advance() # '{'
        self.out(token)
        
        peek = f.peek()
        while(peek != '}'):
            while(peek == 'var'):
                self.CompileVarDec()
                peek = f.peek()
            if(peek != '}'):
                self.CompileStatements()
            peek = f.peek()
        token = f.advance()
        self.out(token)# '}'
        self.indent -=1
        self.print_tag('</subroutineBody>')

    def CompileVarDec(self):
        self.print_tag('<varDec>')
        self.indent +=1
        f = self.fetch
        token = f.advance() 
        self.out(token) #var
        token = f.advance() 
        self.out(token) #type
        token = f.advance() 
        self.out(token) #varName
        while token != ';':
            token = f.advance() #varName or ',' or ';'
            self.out(token)
        self.indent -=1
        self.print_tag('</varDec>')
            
    def CompileStatements(self):
        self.print_tag('<statements>')
        self.indent +=1
        f = self.fetch
        peek = f.peek()
        while(peek in ['let','if','while','do','return']):
            self.CompileStatement()
            peek = f.peek()
        
        self.indent -=1
        self.print_tag('</statements>')
        
    def CompileStatement(self):
        f = self.fetch
        peek = f.peek()
        if peek == 'let': self.CompileLet()
        if peek == 'if': self.CompileIf()
        if peek == 'while': self.CompileWhile()
        if peek == 'do': self.CompileDo()
        if peek == 'return': self.CompileReturn()
        
        
    def CompileDo(self):
        self.print_tag('<doStatement>')
        self.indent +=1
        f = self.fetch
        token = f.advance()
        self.out(token)# do
        peek = f.peek()
        while(peek != ';'):
            self.CompileSubroutineCall()
            peek = f.peek()
        token = f.advance()
        self.out(token)# ';'
        self.indent -=1
        self.print_tag('</doStatement>')
        
    def CompileLet(self):
        self.print_tag('<letStatement>')
        self.indent +=1
        f = self.fetch
        token = f.advance()
        self.out(token)# let
        token = f.advance()
        self.out(token)# varName
        peek = f.peek()
        if(peek == '['):
            token = f.advance()
            self.out(token)#'['
            peek = f.peek()
            if(peek !=']'):
                self.CompileExpression()
            token = f.advance()
            self.out(token)#']'
        
        token = f.advance()
        self.out(token)# '=' 
        
        self.CompileExpression()
        
        token = f.advance()
        self.out(token)# ';'
        self.indent -=1
        self.print_tag('</letStatement>')
        
    def CompileWhile(self):
        self.print_tag('<whileStatement>')
        self.indent +=1
        
        f = self.fetch
        
        token = f.advance()
        self.out(token)# while
        token = f.advance()
        self.out(token)#'('
        peek = f.peek()
        while(peek != ')'):
            self.CompileExpression()
            peek = f.peek()
        token = f.advance()
        self.out(token)# ')'
        token = f.advance()
        self.out(token)# '{'
        peek = f.peek()
        while(peek !='}'):
            self.CompileStatements()
            peek = f.peek()
        token = f.advance()
        self.out(token)# '}'
        self.indent -=1
        self.print_tag('</whileStatement>')
        
    def CompileReturn(self):
        self.print_tag('<returnStatement>')
        self.indent +=1
        f = self.fetch
        token = f.advance()
        self.out(token)# return
        peek = f.peek()
        while(peek != ';'):
            self.CompileExpression()
            peek = f.peek()
        token = f.advance()
        self.out(token)# ';'
        self.indent -=1
        self.print_tag('</returnStatement>')
        
    def CompileIf(self):
        self.print_tag('<ifStatement>')
        self.indent +=1
        f = self.fetch
        token = f.advance()
        self.out(token)# if
        token = f.advance()
        self.out(token) #'('
        peek = f.peek()
        while(peek != ')'):
            self.CompileExpression()
            peek = f.peek()
        token = f.advance()
        self.out(token)# ')'
        token = f.advance()
        self.out(token)# '{'
        peek = f.peek()
        while(peek!= '}'):
            self.CompileStatements()
            peek = f.peek()
        token = f.advance()
        self.out(token)# '}'
        
        self.indent -=1
        self.print_tag('</ifStatement>')
        
    def CompileExpression(self):
        self.print_tag('<expression>')
        self.indent +=1
        #term (op term)*
        f = self.fetch
        peek = f.peek()
        self.CompileTerm()
        peek = f.peek()
        while peek in ['+','-','*','/','&','|',
                    '<','>','=']:
            token = f.advance()
            self.out(token)# OP
            self.CompileTerm()
            peek = f.peek()
        
        self.indent -=1
        self.print_tag('</expression>')
        
    def CompileTerm(self):
        #term (op term)*
        #if term is identifier, distinguish between
        #[ ( or .
        self.print_tag('<term>')
        self.indent +=1
        f = self.fetch
        token = f.advance()
        type = f.tokenType(token)
        
        if type =='integerConstant':
            self.out(f.intVal(token))
        elif type == 'stringConstant':
            self.out(token)
        elif type =='keyword':
            self.out(token)
            
        #( expression )
        elif token == '(':
            self.out(token)#(
            self.CompileExpression()
            token = f.advance()
            self.out(token)#)
        elif token in ['-','~']:
            self.out(token)
            self.CompileTerm()
        elif type == 'identifier':
            self.out(token)
            peek = f.peek()
           
           #subroutine call
            if peek =='.':
                self.CompileSubroutineCall()
                
            #varName [ expression ]
            elif peek == '[':
                token = f.advance()
                self.out(token) #[
                self.CompileExpression()
                token = f.advance()
                self.out(token)# ]
            
            
            #variable
        
        self.indent -=1
        self.print_tag('</term>')
                
    def CompileExpressionList(self):
        self.print_tag('<expressionList>')
        self.indent+=1
        f = self.fetch
        peek = f.peek()
        while(peek != ')'):
            self.CompileExpression()
            peek = f.peek()
            if(peek == ','):
                token = f.advance()
                self.out(token)#','
                peek = f.peek()
                
        
        self.indent-=1
        self.print_tag('</expressionList>')
    
    def CompileSubroutineCall(self):
        f = self.fetch
        token = f.advance()
        while(token!= '('):
            self.out(token)
            token = f.advance()
        self.out(token)# (
        
        self.CompileExpressionList()
        token = f.advance()
        self.out(token)#')'
        return
        
    
if __name__ == "__main__":
    try:
        if(len(sys.argv)<2):
            print('No input file specified!')
        else:
            CompilationEngine(sys.argv[1])
    except Exception as e:
        print(e)
        input()
        sys.exit()