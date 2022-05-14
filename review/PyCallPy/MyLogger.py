import os, sys, string, datetime, time,  shutil, traceback, arcpy
from time import strftime
from datetime import date, timedelta




class Logger:
	def __init__(self, logPath,filePath,logid):		
		try:        
			fileprefix = strftime("%Y-%m-%d-%H-%M-%S")			
			name = os.path.basename(filePath)
			##logfilename =logid +'_'+ str(name) + '_' + str(fileprefix)+".log"			
			logfilename =logid +'_'+ str(name)+".log"			
			logFullPath = os.path.abspath(logPath + '\\' +logfilename)			
			logFile=open (logFullPath, 'a')
			logFile.write (str(fileprefix) + ": Start\n")					
			self.logFile=logFile
			self.logFullPath=logFullPath
			self.logfilename=logfilename			
			self.__myPrint("Created:" + logFullPath) 
			self.errList=list()
			
		except:			
			arcpy.AddError("CreateScriptLogFile Error")
			arcpy.AddError(traceback.format_exc())     

	def __myPrint(self,msg):
		arcpy.AddMessage(msg) 
		
		
	def Msg(self, msg):
		msg = str(msg)
		self.__myPrint(msg)
		timeStamp = strftime("%Y-%m-%d-%H-%M-%S");
		self.logFile.write (str(timeStamp) + ": ")		
		self.logFile.write (msg+"\n")	    
	
	
	
	def Close(self):
		self.logFile.close()