import arcpy
import os
import sys
import argparse


def listLyrsDs(baseDir,mxdName):

    _mxdPath = os.path.join(baseDir,mxdName)
    print _mxdPath
    mxd = arcpy.mapping.MapDocument(_mxdPath)
    for lyr in arcpy.mapping.ListLayers(mxd):
        if lyr.supports("DATASOURCE"):
            print('\t' + lyr.dataSource)

def remap(baseDir,origMxd,newMxd,origDS,newDS):    
    _origMxd = os.path.join(baseDir,origMxd)
    _origDS = os.path.join(baseDir,origDS)
    _newDS  = os.path.join(baseDir,newDS)
    _newMxd = os.path.join(baseDir,newMxd)

    mxd = arcpy.mapping.MapDocument(_origMxd)
    mxd.findAndReplaceWorkspacePaths(_origDS,_newDS)
    mxd.saveACopy(_newMxd)

    del mxd

'''
example:
remapds.py -BaseDir "D:\People\fxka\New folder\Fresno" -OrigMxdName "Fresno.mxd" -NewMxdName "FresnoNew.mxd" -OrigDSPath "C:\ProgramData\Esri\PGE\Electric\Distribution\Fresno" -NewDSPath "\\itgisappdev01\EcdArchive\ElectricalData_Latest"
'''    
parser = argparse.ArgumentParser(description='Remaps datasources')
parser.add_argument('-BaseDir', '--BaseDir', required=True)
parser.add_argument('-OrigMxdName', '--OrigMxdName', required=True)
parser.add_argument('-NewMxdName', '--NewMxdName', required=True)
parser.add_argument('-OrigDSPath', '--OrigDSPath', required=True)
parser.add_argument('-NewDSPath', '--NewDSPath', required=True)

args = parser.parse_args()

baseDir=args.BaseDir
origMxd = args.OrigMxdName
newMxd  = args.NewMxdName
origDS  = args.OrigDSPath
newDS   = args.NewDSPath

remap(baseDir,origMxd,newMxd,origDS,newDS)
listLyrsDs(baseDir,origMxd)
listLyrsDs(baseDir,newMxd)
