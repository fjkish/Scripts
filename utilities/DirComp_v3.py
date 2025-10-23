import os

##C:\Users\fran2604\Documents\ArcGIS\Projects\CR325745\Unzipped\NavWithUpdate\p12\northamerica.tn

dir1 = r'E:\Frank\Temp\MapOpsBM\p12\northamerica.cdf_db'
dir2 = r'E:\Frank\Temp\origMapOpsBM\p12\northamerica.cdf_db'


def printSet(setX,msg):
    
    print ('++++++++++++++++++++++++++++++++++++')
    print ('Files in: ' + msg)
    print ('++++++++++++++++++++++++++++++++++++')
    for v in setX:
        print v

def listfiles(path):
    files = []
    for dirName, subdirList, fileList in os.walk(path):
        dir = dirName.replace(path, '')
        for fname in fileList:
            files.append(os.path.join(dir, fname))
    return files

dir1List = listfiles(dir1)
dir2List = listfiles(dir2)

files_only_in_dir1 = set(dir1List) - set(dir2List) 
files_only_in_dir2 = set(dir2List) - set(dir1List)
files_only_in_either = set(dir1List) ^ set(dir2List)
files_in_both = set(dir1List) & set(dir2List)
all_files = set(dir1List) | set(dir2List)



print ('dir1 = ' + dir1)
print ('dir2 = ' + dir2)

printSet( files_only_in_dir1,"files_only_in_dir1")
printSet( files_only_in_dir2,"files_only_in_dir2")
