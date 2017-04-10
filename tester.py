from WorkingTests import *



def testCPU():
    cpu = CPU()
    desiredAnswers = []
    myAnswers = []
    flipFlop = False
    with open("testFiles/chipFiles/cpu.tst", "r") as ins: 
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
                if(not flipFlop):
                    flipFlop = True
                else:
                    flipFlop = False
                    print()
                
                    
                
                desiredAnswers.append(correctanswers)
                myAnswers.append(myanswers)
    generalTester(desiredAnswers,myAnswers)
  
                
testPC()
testRegister()
testBit()
testCPU()
