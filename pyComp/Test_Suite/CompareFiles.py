class CompareFiles:
    
    def __init__(self,file1,file2):
        badCount = 0
        with open(file1) as f1:
            with open(file2) as f2:
                file1_line = f1.readline()
                file2_line = f2.readline()
                if(file1_line != file2_line):
                    badCount+=1
                    print('ERROR',file1_line,file2_line)
                else:
                    pass
                
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