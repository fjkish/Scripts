import zipfile
import os.path
import os
import arcpy

MAINDIR =r'C:\Frank\Temp'
GDBEXT = '.gdb'
ZIPEXT ='.gdb.zip'
FINALGDB = os.path.join(MAINDIR,'GemBnds.gdb')
SCALES=['SCALE_100']

def Unzipper(officeName):    
    zipFilePathIn = os.path.join(MAINDIR,officeName+ZIPEXT)
    zipFilePathOut = os.path.join(MAINDIR,officeName+GDBEXT)    
    zfile = zipfile.ZipFile(zipFilePathIn)    
    if not os.path.exists(zipFilePathOut):
        os.makedirs(zipFilePathOut)    
        zfile.extractall(zipFilePathOut)

def CopyBnds(officeName):
    for scale  in SCALES:    
        count = 0
        inMD = os.path.join(MAINDIR,officeName+GDBEXT,scale)          
        outFC=FINALGDB+'/'+officeName+'_'+scale
        result = arcpy.GetCount_management(inMD)
        count = int(result.getOutput(0))        
        if (count>0):
            arcpy.ExportMosaicDatasetGeometry_management(inMD,outFC, where_clause="", geometry_type="FOOTPRINT")    
            
            #fjk need to add OFFICE (office is full name not abbrev so need translation),MAP_NAME (presently name in the md data), and Scale (maybe)
            
def CopyToFinal(officeName):

    for scale  in SCALES:           
        outFC=FINALGDB+'/'+officeName+'_'+scale        
        if arcpy.Exists(outFC):
            

Unzipper('AUB')
CopyBnds('AUB')

CopyToFinal('AUB')
