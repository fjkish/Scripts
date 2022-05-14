import arcpy, os, sys, string, ConfigParser, shutil, traceback
from time import strftime
from datetime import date, timedelta

def ValidateConfigExists(configParaFilePath,configParaFileName,LOG):	    
    configPath = configParaFilePath+"\\"+configParaFileName
    if not os.path.exists (configPath):        
        logMsg="Configuration parameters file does not exist or is not accessible in path below\n" + configPath +"\nExiting. Make sure the configuration file exist before running this script again\n"        
        LOG.Msg(logMsg)
        return False
    else:                        
        LOG.Msg("Found config file:"+ configPath)
        return True
		
def ValidateConfigValues (configParaFilePath,configParaFileName,LOG):
	
	configValues = ReadConfigFile(configParaFilePath,configParaFileName) 
	
	LOG.Msg("Validating config contains required sections and items.")
	##if reading fails configValues is none, so missing section or item
	if (configValues==None):
		return False
	LOG.Msg("OK - config contains required sections and items.")
	
	LOG.Msg("Validating config item values")	
	isOk=0
	#sections and item seem ok so now check the values, have values and values are 'correct'
	for k in configValues:
		if (configValues[k] == '' or configValues==None):
			print (k + ' is empty')	
			##do more checking based on what each value represent, folder , gdb, etc
			
	#fix based on above checks
	if (isOk==0):
		LOG.Msg("Passed - config item values are ok.")	
		return True
	else:
		LOG.Msg("Failed - config item values are not correct.")	
		return False

def ReadConfigFileCommon(configParaFilePath,configParaFileName):
	try:	          
		cvCommon = dict()
		cvCommon['inputGrip_ws']=''
		cvCommon['geocodingLocator']=''
		cvCommon['templateFCInput_ws']=''
		cvCommon['switchFC']=''		
	
		config = ConfigParser.ConfigParser()
		config.read(configParaFilePath+"\\"+configParaFileName)      
		
		for k in cvCommon:
			print 'Looking for ' + k
			##this can fail if missing so in try catch
			cvCommon[k] = config.get("COMMON", k)   
		
		
		return cvCommon
	except:
		#print(traceback.format_exc())
		arcpy.AddError("!!Error reading config file, perhaps a missing section or item.")
		return None

def ReadConfigFileState(configParaFilePath,configParaFileName,stateName):
	try:	
		cvState = dict()
		cvState['cordsys']=''
		cvState['input_ws']=''
		
		config = ConfigParser.ConfigParser()
		config.read(configParaFilePath+"\\"+configParaFileName)      
		
		for k in cvState:
			print 'Looking for ' + k
			##this can fail if missing so in try catch
			cvState[k] = config.get(stateName, k)   
		
		
		return cvState
	except:
		#print(traceback.format_exc())
		arcpy.AddError("!!Error reading config file, perhaps a missing section or item.")
		return None
