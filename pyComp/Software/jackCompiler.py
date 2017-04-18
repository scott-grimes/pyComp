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
    
    def symbolOperator(self,token):
        if token == '+':
            return 'add'
        elif  token == '-':
            return 'sub'
        elif  token == '*':
            return 'call Math.multiply 2'
        elif  token == '/':
            return 'call Math.divide 2'
        elif  token == '&':
            return 'and'
        elif  token == '|':
            return 'or'
        elif  token == '<':
            return 'lt'
        elif  token == '>':
            return 'gt'
        elif  token == '=':
            return 'eq'
        
        
        return None
        
class CompileJack:
    
    def __init__(self,file_with_path):
        self.fetch = Analyzer(file_with_path)
        self.symbol = SymbolTable()
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
        self.indent +=1
        f = self.fetch
        class_keyword = f.advance() #encountered a class
        
        self.class_name = f.advance() 
        
        open_brace = f.advance() #opens the class
        
        
        peek = f.peek() #class Var Dec
        while(peek in ['static','field']):
            self.CompileClassVarDec()
            peek = f.peek()
        
        #class subroutine Dec
        while(peek in ['constructor','function',
                    'method','void']):
            self.CompileSubroutine()
            peek = f.peek()
            
        close_curl = f.advance() #ends the class
        
        self.indent-=1
        
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
        self.indent +=1
        f = self.fetch
        sub_type = f.advance() #constructor/function/method
        
        return_type = f.advance() #return type or void
        if(return_type == 'void'):
            self.voidReturn = True
        else:
            self.voidReturn = False
        sub_name = f.advance() #subroutineName 
       
        open_parenth = f.advance() # '('
        
        parameter_count = self.CompileParameterList()
        
        close_parenth = f.advance() # ')'
        
        open_brace = f.advance() # '{' starts the body
        
        num_of_method_vars = 0
        peek = f.peek()
        while(peek == 'var'):
                num_of_method_vars+=self.CompileVarDec()
                peek = f.peek()
        
        
        #find num of variables declared!
        print('function '+self.class_name+'.'+sub_name+' '+str(parameter_count+num_of_method_vars))
        
        self.CompileSubroutineBody()
        
        self.indent -=1
        
        return
    
    def CompileParameterList(self):
        #((type varName)(','type varName)*)?
        parameter_count = 0
        self.indent +=1
        f= self.fetch
        peek = f.peek()
        while peek != ')':
            parameter_count+=1
            type = f.advance()# type or varName
            varName = f.advance()
            self.symbol.define(varName,type,'arg')
            peek = f.peek()
            if peek == ',':
                f.advance()
        self.indent -=1
        return parameter_count
            
    def CompileSubroutineBody(self):
        self.indent +=1
        f = self.fetch
        num_of_vars = 0
        peek = f.peek()
        while(peek != '}'):
            self.CompileStatements()
            peek = f.peek()
        close_brace = f.advance() #'}' end of our function
        #print('i had '+str(num_of_vars)+ ' variables')
        self.indent -=1

    def CompileVarDec(self):
        self.indent +=1
        f = self.fetch
        num_of_vars = 1
        token = f.advance()  
        var = token
        token = f.advance()  
        type = token
        token = f.advance() 
        varName = token
        self.symbol.define(varName,type,'var')
        peek = f.peek()
        while peek == ',':
            token = f.advance() #','
            varName = f.advance()#varName
            self.symbol.define(varName,type,'var')
            peek = f.peek()
            num_of_vars+=1
        f.advance() #';' ends declaration
        print(self.symbol.subroutineTable)
        self.indent -=1
        return num_of_vars
            
    def CompileStatements(self):
        self.indent +=1
        f = self.fetch
        peek = f.peek()
        while(peek in ['let','if','while','do','return']):
            self.CompileStatement()
            peek = f.peek()
        
        self.indent -=1
        
    def CompileStatement(self):
        f = self.fetch
        peek = f.peek()
        if peek == 'let': self.CompileLet()
        if peek == 'if': self.CompileIf()
        if peek == 'while': self.CompileWhile()
        if peek == 'do': self.CompileDo()
        if peek == 'return': self.CompileReturn()
        
        
    def CompileDo(self):
        self.indent +=1
        f = self.fetch
        token = f.advance() #do command
        peek = f.peek()
        while(peek != ';'):
            self.CompileSubroutineCall()
            peek = f.peek()
        token = f.advance()# ';' end of do command
        
        self.indent -=1
        
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
        self.indent +=1
        f = self.fetch
        token = f.advance()# return
        peek = f.peek()
        while(peek != ';'):
            self.CompileExpression()
            peek = f.peek()
        semi_colon = f.advance()# ';' end of return statement
        if(self.voidReturn):
            print('pop temp 0')
            print('push constant 0')
        
            
        
        print('return')
        
        self.indent -=1
        
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
        self.indent +=1
        #term (op term)*
        f = self.fetch
        peek = f.peek()
        self.CompileTerm()
        peek = f.peek()
        while peek in ['+','-','*','/','&','|',
                    '<','>','=']:
            token = f.advance()
            operator_statement = f.symbolOperator(token)# operator symbol
            self.CompileTerm()
            print(operator_statement)
            peek = f.peek()
        
        self.indent -=1
        
    def CompileTerm(self):
        #term (op term)*
        #if term is identifier, distinguish between
        #[ ( or .
        self.indent +=1
        f = self.fetch
        token = f.advance()
        type = f.tokenType(token)
        
        if type =='integerConstant':
            print('push constant '+token)
            
        elif type == 'stringConstant':
            self.out(token)
        elif type =='keyword':
            self.out(token)
            
        #( expression )
        elif token == '(':
            
            self.CompileExpression()
            token = f.advance()#) end of parenthisis
            
        elif token in ['-','~']:
            self.CompileTerm()
            if token == '-':
                print('neg')
            if token == '~':
                print('not')
            
            
       
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
                
    def CompileExpressionList(self):
        
        self.indent+=1
        f = self.fetch
        peek = f.peek()
        num_of_expressions = 0
        while(peek != ')'):
            num_of_expressions += 1
            self.CompileExpression()
            peek = f.peek()
            if(peek == ','):
                token = f.advance()# ',' seperates another expression
                peek = f.peek()
                
        
        self.indent-=1
        return str(num_of_expressions)
    
    def CompileSubroutineCall(self):
        f = self.fetch
        token = f.advance()
        subroutine_name = token
        while(token!= '('):
            token = f.advance()
            if(token!='('):
                subroutine_name += token
        
        num_subroutine_arguments = self.CompileExpressionList()
        token = f.advance() #')' end of subroutine call's arguments
        print('call '+subroutine_name+' '+num_subroutine_arguments)
        return
    
class Symbol:
    def __init__(self,name,type,kind):
        self.name = name
        self.type = type
        self.kind = kind
        
    def __repr__(self):
        return '['+self.name+','+self.type+','+self.kind+']'
        
class SymbolTable:
    def __init__(self):
        self.classTable = []
        self.subroutineTable = []
    
    def startSubroutine(self):
        self.subroutineTable = []
    
    def define(self,name,type,kind):
        newSymbol = Symbol(name,type,kind)
        if kind in ['arg','var']:
            self.subroutineTable.append(newSymbol)
        if kind in ['static','field']:
            self.classTable.append(newSymbol)
        
    def varCount(self,kind):
        num = 0
        if kind in ['arg','var']:
            table = self.subroutineTable
        if kind in ['static','field']:
            table = self.classTable
        for i in table:
            if i.kind == kind:
                num+=1
        return num
            
            
    def kindOf(self,name):
        #what kind of variable is name
        table = self.getTableOf(name)
        if table != None:
            names = [i.name for i in table]
            if name in names:
                return table[table.index(name)].kind
        return None
        
        
    def typeOf(self,name):
       #what type of variable is name
        table = self.getTableOf(name)
        if table != None:
            names = [i.type for i in table]
            if name in names:
                return table[table.index(name)].type
        return None
    
    def getTableOf(self,name):
        #returns the table which contains our variable
        #is our name in the subroutine
        names = [i.name for i in self.subroutineTable]
        if name in names:
            return self.subroutineTable
        
        #is our name a class var?
        names = [i.name for i in self.classTable]
        if name in names:
            return self.classTable
    
    def indexOf(self,name):
        #what is the index of name
        table = self.getTableOf(name)
        if table != None:
            names = [i.name for i in table]
            if name in names:
                return table.index(name)
        return None
    
class VMWriter:
   def __init__(self):
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