import os, sys, string, datetime, time, ConfigParser, shutil, traceback, MyLogger,MyConfigReader, subprocess
import random
from time import strftime
from datetime import date, timedelta

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def CallScript(scriptName,inputGrip_ws,geocodingLocator,templateFCInput_ws,switchFC,cordsys,input_ws,stateName):			
	scriptX = '{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}'.format(scriptName,inputGrip_ws,geocodingLocator,templateFCInput_ws,switchFC,cordsys,input_ws,stateName,LOGID,LOGPATH)
	LOG.Msg( scriptX)
	result = os.system(scriptX)
	
	if (result!=0):
		LOG.Msg (scriptName + " FAILED!")
		LOG.Msg(scriptName + ' result = ' + str(result))		
		sys.exit()
	else:
		LOG.Msg (scriptName + " SUCCEEDED!")
		LOG.Msg(scriptName + ' result = ' + str(result))

def MAIN(cvCommon,cvState,stateName):
    try:	
		inputGrip_ws      = cvCommon['inputGrip_ws']
		geocodingLocator  = cvCommon['geocodingLocator']
		templateFCInput_ws= cvCommon['templateFCInput_ws']
		switchFC          = cvCommon['switchFC'] 
		cordsys           = cvState['cordsys']
		input_ws          = cvState['input_ws']
		
		CallScript("AB2_Step3_Combine_TextPoint_and_Point_Process.py",inputGrip_ws,geocodingLocator,templateFCInput_ws,switchFC,cordsys,input_ws,stateName)
		CallScript("AB2_Step4_Points_Processing.py",inputGrip_ws,geocodingLocator,templateFCInput_ws,switchFC,cordsys,input_ws,stateName)
		
		
    except:
        LOG.Msg("++++MAIN Exception++++\n")
        LOG.Msg(traceback.format_exc())        
        LOG.Msg("++++++++++++++++++++++\n")                
        
####################################################################################
## START
####################################################################################

##Globals############################################
##Change if you want config and logs some where else
CONFIGPARAFILEPATH = ".\Config"
LOGPATH = r".\Logs"
############################################
start = time.mktime(time.localtime())

##for logging
LOGID             = id_generator()
thisfile = os.path.basename(__file__)
LOG = MyLogger.Logger(LOGPATH,thisfile,LOGID)
LOG.Msg("Running: " + sys.argv[0] )

##argument check, one extra than we use ... extra is for the py script name
argLen = 3
if len(sys.argv) != argLen:
    LOG.Msg("Number of arguments expected: " + str(argLen-1))
    LOG.Msg("Number of arguments input: " + str(len(sys.argv)-1))
    LOG.Msg("--> Usage: <CONFIGPARAFILENAME> <STATENAME> e.g. ConfigurationParameters.txt DC")
    LOG.Close()
    sys.exit()

##get args to vars as needed
configFileName = sys.argv[1]	
stateName=sys.argv[2]

##validate
if (MyConfigReader.ValidateConfigExists(CONFIGPARAFILEPATH,configFileName,LOG) == True):               
	configValuesCommon=MyConfigReader.ReadConfigFileCommon(CONFIGPARAFILEPATH,configFileName)
	configValuesState=MyConfigReader.ReadConfigFileState(CONFIGPARAFILEPATH,configFileName,stateName)
	MAIN(configValuesCommon,configValuesState,stateName)	

LOG.Msg("Total Time = %0.1f minutes" % ((time.mktime(time.localtime()) - start)/60.0))
LOG.Msg("Done")
LOG.Close()

print "Done Done"	
	
	
