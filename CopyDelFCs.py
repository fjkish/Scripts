import arcpy,os

def DeleteFc(dstGdbName,folder):
    fcList = ['PadmountStructure','SubsurfaceStructure','SupportStructure']    
    for fcName in fcList:        
		dstFc = os.path.join(folder,dstGdbName,fcName)       
		if (arcpy.Exists(dstFc)):
			gpResult = arcpy.Delete_management(dstFc)
			if (gpResult.status == 4 ):
				arcpy.AddMessage("Deleted " + dstFc)
			else:
				arcpy.AddMessage(gpResult.getMessages())	


def CopyFc(sourceGdbName,dstGdbName,folder):
    fcList = ['PadmountStructure','SubsurfaceStructure','SupportStructure']    
    for fcName in fcList:        
		
		srcFc = os.path.join(folder,sourceGdbName,fcName)
		dstGdb = os.path.join(folder,dstGdbName)       
		dstFc = os.path.join(folder,dstGdbName,fcName)       
		if (arcpy.Exists(dstFc)):
			gpResult = arcpy.Delete_management(dstFc)
			if (gpResult.status == 4 ):
				arcpy.AddMessage("Deleted " + dstFc)
			else:
				arcpy.AddMessage(gpResult.getMessages())		
		if (arcpy.Exists(dstFc) == False):		
			gpResult = arcpy.FeatureClassToFeatureClass_conversion(srcFc,dstGdb,fcName)	
			if (gpResult.status == 4 ):
				arcpy.AddMessage("Copied " + srcFc + " to " + dstGdb + " as " + fcName)
			else:
				arcpy.AddMessage(gpResult.getMessages())
		else:
			arcpy.AddMessage(gpResult.getMessages())
#

divList = ['KERN','FRESNO','STOCKTON','YOSEMITE']  
folder  = r'C:\fxka\Data\ECExtract\EcExtracted2015-01-06'                  
for divName in divList:        
	dstGdbName = divName + '.gdb'
	sourceGdbName = divName + 'Structures.gdb'
	#DeleteFc(dstGdbName,folder)
	CopyFc(sourceGdbName,dstGdbName,folder)

print ' done like dinner'