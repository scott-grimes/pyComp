#this does some shit 
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
        
        #replaces all groups of whitespace with single whitespaces
        #inputStream = ' '.join(inputStream.split())
        
        
    
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
            return 'string_const'
        
        if token in self.keywords:
            return 'keyword'
        if token in self.symbols:
            return 'symbol'
        if token[0].isdigit():
            return 'int_const'
        
        
        return 'identifier'
        
    def keyWord(self,token):
        #returns the keyword of the current 
        #token
        
        return token
    def intVal(self,token):
        return int(token)
    def stringVal(self,token):
        return token.replace("\"",'')
        
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
        
    def out(self,token):
        for i in range(self.indent):
            print('  ',end='')
        if(isinstance( token, int )):
           type = self.fetch.tokenType(str(token))
           print("<"+type+"> "+str(token)+" </"+type+">")
        
        else:
            type = self.fetch.tokenType(token)
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
            print('peek: '+peek)
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
        token = f.advance() #type
        self.out(token)
        token = f.advance() #returns
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
        if(not peek):
            return
        if(peek == 'readInt'):
            sys.exit()
        if peek == 'let': self.CompileLet()
        if peek == 'if': self.CompileIf()
        if peek == 'while': self.CompileWhile()
        if peek == 'do': self.CompileDo()
        if peek == 'return': self.CompileReturn()
        
        
        self.indent -=1
        self.print_tag('</statements>')
        
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
            while(peek !=']'):
                self.CompileExpression()
                peek = f.peek()
            token = f.advance()
            self.out(token)#']'
        
        token = f.advance()
        self.out(token)# '='
        
        peek = f.peek()
        while(peek != ';'):
            self.CompileExpression()
            peek = f.peek()
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
        f = self.fetch
        token = f.advance()
        self.out(token)# return
        peek = f.peek()
        while(peek != ';'):
            self.CompileExpression()
            peek = f.peek()
        token = f.advance()
        self.out(token)# ';'
        
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
        token = f.advance()
        self.out(token)# '}'
        
        self.indent -=1
        self.print_tag('</ifStatement>')
        
    def CompileExpression(self):
        self.print_tag('<expression>')
        self.indent +=1
        #term (op term)*
        f = self.fetch
        
        self.CompileTerm()
        peek = f.peek()
        while(peek in ['+','-','*','/','&','|','<',
                       '>','=']):
            token = f.advance()
            self.out(token)# op 
            self.CompileTerm()
            peek = f.peek()
        
        self.indent -=1
        self.print_tag('</expression>')
        
    def CompileTerm(self):
        
        self.print_tag('<term>')
        self.indent +=1
        f = self.fetch
        
        token = f.advance() #some term
        type = f.tokenType(token)
        
        if type == 'string_const':
             self.out(f.stringVal(token)) #prints a string
        elif type == 'keyword':
            self.out(f.keyWord(token))
        elif type == 'symbol':
            if(token == '('):
                #I have an (expression)
                self.out(token)#'('
                peek = f.peek()
                while(peek != ')'):
                    self.CompileExpression()
                    peek = f.peek()
                token = self.out(token)
                self.out(token)#')'
            else:
                self.out(token)
        elif type == 'int_const':
            self.out(f.intVal(token))
        elif type == 'identifier':
            #an identifier may be either a 
            # subroutine
            # varName
            # varName [ expression ]
            
            #checking for a subroutine
            subroutine = False
            peek = f.peek()
            while(peek == '.'):
                #we have a subroutine call!
                subroutine = True
                self.out(token)
                token=f.advance() # pulls the '.' from our subroutine call
                self.out(token) #'.'
                peek = f.peek()
                
            if(subroutine):
                token = f.advance()
                self.out(token)# '('
                self.CompileSubroutineCall()
                token = f.advance()
                self.out(token)# ')'
            else:
                #our identifier is either
                #varName or
                #varName [expression]
                self.out(token)# varName
                peek = f.peek()
                if(peek == '['):
                    token = f.advance()
                    self.out(token)#'['
                    self.CompileExpression()
                    token = f.advance()
                    self.out(token)#']'
        self.indent -=1
        self.print_tag('</term>')
                
    def CompileExpressionList(self):
        f = self.fetch
        peek = f.peek()
        while(peek!= ')'):
            print(peek)
            print()
            self.CompileExpression()
            peek = f.peek()
            if(peek == ','):
                token = f.advance()
                self.out(token)#','
                peek = f.peek()
            pass

    
    def CompileSubroutineCall(self):
        f = self.fetch
        token = f.advance()
        self.out(token)# subroutineName or className
        token = f.advance()
        self.out(token)# '(' or '.'
        self.CompileExpressionList()
        token = f.advance()
        self.out(token)#')'
        return
        
        
        pass
    
    
    
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