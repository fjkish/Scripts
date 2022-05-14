source = r"C:\Users\fran2604\Downloads\pv\Debug"
dest = r"C:\Users\fran2604\Downloads\pv\Bin43"


from os import walk

f = []
for (dirpath, dirnames, filenames) in walk(source):
    f.extend(filenames)
    break
    



f1 = []
for (dirpath, dirnames, filenames) in walk(dest):
    f1.extend(filenames)
    break
    

diffs = [a for a in f+f1 if (a not in f) or (a not in f1)]

for x in diffs:
    print x