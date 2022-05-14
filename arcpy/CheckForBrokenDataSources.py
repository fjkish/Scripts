import arcpy, os

def CheckDS(divName):
	path = r'C:\ProgramData\ESRI\PGE\Electric\Distribution\\' + divName
	fileName=divName + '.mxd'
	fullPath = os.path.join(path, fileName)

	mxd = arcpy.mapping.MapDocument(fullPath)
	print "MXD: " + fileName
	brknList = arcpy.mapping.ListBrokenDataSources(mxd)
	cnt = 0
	for brknItem in brknList:
		cnt+=1
		print "\t" + brknItem.name

	print 'Done,  Broken Data Sources ' + str(cnt)
	
divList = ['KERN','FRESNO','STOCKTON','YOSEMITE']  

for divName in divList:        
	CheckDS(divName)