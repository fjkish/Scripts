import os 
import time
filename =r'c:\frank\go.txt'
filename1 =r'c:\frank\go1.txt'
filename2 =r'c:\frank\go2.txt'
listX=[filename,filename1,filename2]

while (True):
    existsList=[]
    for fileX in listX:            
        existsList.append(os.path.isfile(fileX))
    print existsList
    if (False in  existsList):
        print 'continue'
    else:
        break
    time.sleep(5)  
    
    
    
    
print 'done!!'