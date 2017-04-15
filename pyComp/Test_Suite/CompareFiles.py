class CompareFiles:
    
    def __init__(self,file1,file2):
        badCount = 0
        lines_1 = open(file1,'r').readlines()
        lines_2 = open(file2,'r').readlines()
        for line_1, line_2 in zip(lines_1, lines_2):
            if(line_1 != line_2):
                badCount+=1
                #print('ERROR',line_1,line_2)
                
        file1_trunkName = file1.split('/')[-1]
        file2_trunkName = file2.split('/')[-1]
        print(file1_trunkName,file2_trunkName,'had '+str(badCount)+' errors!')
        
if __name__ == "__main__":
    try:
        if(len(sys.argv)<3):
            print('No input files specified!')
        else:
            CompareFiles(sys.argv[1],sys.argv[2])
    except Exception as e:
        print(e)
        input()
        sys.exit()