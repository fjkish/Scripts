

source = r'F:\Kish\Keep\Mocking\masterbkup\windows'
dest = r'F:\Kish\Keep\Mocking\na_online_test_mtr2\windows\data\rt_c_api\network_analyst\network_test_data\test_data'


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
    print (x)