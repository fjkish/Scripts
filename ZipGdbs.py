import arcserver
import arcpy
import csv
import sys
import argparse
import os
import sys
import string
import datetime
import time
import ConfigParser
import shutil
import traceback
import ntpath
import logging
import logging.handlers
import glob

def ZipGdb(initDir,officeCode):

    try:
        officePath = os.path.join(initDir,officeCode)    
        gdbFolder = os.path.join(initDir,officeCode,"GDB")
        gdb = os.path.join(gdbFolder,officeCode+'.gdb')   
        zip =  os.path.join(gdbFolder,officeCode+'.gdb.zip')   
        
        if (not os.path.exists(gdb)): 
            print ('GDB not found: ' + gdb)
            return None
            
        #delete existing local zip   
        if (os.path.isfile(zip)):
            print ("zip: " + zip + " exists")
            return None
        
        #make new zip, if previous was removed
        if (not os.path.isfile(zip) ):            
            ignore_pat = shutil.ignore_patterns('*.lock')
            tmpGdb = os.path.join(gdbFolder,'temp',officeCode+'.gdb')  
            shutil.copytree(gdb, tmpGdb,ignore=ignore_pat)
            print('Creating local:' + zip)
            shutil.make_archive(tmpGdb, format="zip", root_dir=tmpGdb)  
            zipTmp =  tmpGdb + '.zip'
            #move the  the zip 
            shutil.move(zipTmp,zip)
            #delete temp folder
            shutil.rmtree(os.path.join(gdbFolder,'temp'))            
            shutil.rmtree(gdb)
            return zip            
        else:
            print( 'Could not remove ' + zip)
            return None
            
        
    except:
        exeptionmsg = traceback.format_exc()                
        print(str(exeptionmsg))
        return None
    

initDir = r'D:\temp\Gas' 

ZipGdb(initDir,"AUB")
ZipGdb(initDir,"BKD")
ZipGdb(initDir,"CHI")
ZipGdb(initDir,"CMA")
ZipGdb(initDir,"CND")
ZipGdb(initDir,"CUO")
ZipGdb(initDir,"EUR")
ZipGdb(initDir,"FRE")
ZipGdb(initDir,"HAY")
ZipGdb(initDir,"MER")
ZipGdb(initDir,"MOD")
ZipGdb(initDir,"NAP")
ZipGdb(initDir,"OAK")
ZipGdb(initDir,"RCH")
ZipGdb(initDir,"RDG")
ZipGdb(initDir,"SAC")
ZipGdb(initDir,"SAL")
ZipGdb(initDir,"SCL")
ZipGdb(initDir,"SFO")
ZipGdb(initDir,"SJE")
ZipGdb(initDir,"SNR")
ZipGdb(initDir,"SRO")
ZipGdb(initDir,"STK")
ZipGdb(initDir,"UKI")
ZipGdb(initDir,"VJO")    
       

