import os

def GetFilesx(mydir):	
  dict={}	
  for root, dirs, files in os.walk(mydir):    
    for file in files:      
      print file 
      if file.endswith(".txt"):
        fullpath = os.path.join(root, file)
        filename = (os.path.splitext(fullpath)[0]).lower()
        filename =(os.path.splitext(os.path.basename(fullpath))[0]).lower()
        if filename in dict:
          print filename + " already in dict"
        else:
          print (fullpath)
          dict[filename]=fullpath
	return dict


def GetFiles(mydir):
    dict={}		
    for root, subdirs, files in os.walk(mydir):

        for name in files:
            if name.endswith(".txt"):            
                fullpath = os.path.join(root, name)
                ##full path with no ext
                #filename = (os.path.splitext(fullpath)[0]).lower()
                
                dirname1 = os.path.basename(os.path.dirname(fullpath)) 
                print "dirname1 --> " + dirname1
                filename =(os.path.splitext(os.path.basename(fullpath))[0]).lower()       
                
                if filename in dict:
                    print filename + " already in dict"
                else:
                    print filename
                    dict[filename]=fullpath
    return dict
dict = GetFiles(r'c:\frank\temp')	
print len(dict.keys())

'''
for path, subdirs, files in os.walk(r'c:\frank\temp'):
    for name in files:
        if name.endswith(".txt"):
            print os.path.join(path, name)
'''
