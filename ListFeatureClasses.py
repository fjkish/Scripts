import arcpy,os,argparse


def listFcsInGDBx():
    ''' set your arcpy.env.workspace to a gdb before calling '''
    for fds in arcpy.ListDatasets('','feature') + ['']:
        for fc in arcpy.ListFeatureClasses('','',fds):
            yield os.path.join(arcpy.env.workspace, fds, fc)
            
def listFcsInGDB(gdb):
    ''' list all Feature Classes in a geodatabase, including inside Feature Datasets '''
    arcpy.env.workspace = gdb
    fcs = []
    for fds in arcpy.ListDatasets('','feature') + ['']:
        for fc in arcpy.ListFeatureClasses('','',fds):
            #yield os.path.join(fds, fc)
            fcs.append(os.path.join(fds, fc))
    return fcs

parser = argparse.ArgumentParser(description='GDB')
parser.add_argument('-GDB', '--GDB', required=True)
args = parser.parse_args()
print 'Processing ', arcpy.env.workspace
fcs = listFcsInGDB(args.GDB)
for fc in fcs:     
    result = arcpy.GetCount_management(fc)
    count = int(result.getOutput(0))
    print fc + ' = ' + str(count)
