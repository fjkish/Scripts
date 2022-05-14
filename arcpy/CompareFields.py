import arcpy
import argparse

def CreateDicOfFields(fc):
    result = {}    
    fields = arcpy.ListFields(fc)
    for field in fields:
        result[field.name]=field.type
    return result

def PrintCompareResult(added, removed, modified, same):
    print "\n"
    print "Added"
    print "======="
    for x in added:
        print x
    
    print "\n"
    print "Removed"
    print "======="
    for x in removed:
        print x

    print "\n"
    print "Modified"
    print "======="
    
    for key in modified:
        print key + ' : ' +  str(modified[key][0]) + ' -> ' +  str(modified[key][1])
    
def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])    
    PrintCompareResult(added, removed, modified, same)

parser = argparse.ArgumentParser()    
parser.add_argument('fc1', help='feature class 1')    
parser.add_argument('fc2', help='feature class 2')    
# Read the command line arguments.
args = parser.parse_args()

flds1 = CreateDicOfFields(args.fc1) 
flds2 = CreateDicOfFields(args.fc2) 
dict_compare(flds1,flds2)



