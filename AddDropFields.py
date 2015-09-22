import arcpy
import argparse 

##Update to correct connection file and fc name
fc =r"D:\Frank\Temp\junk.gdb\test"

##Update ad needed

FIELDSTOADD = {'CASHONLYSCORE':'LONG','DAYSAGING':'LONG','CUMULATIVE_MINUTES':'DOUBLE','EXTRACTDATETIME':'DATE','LASTACTIONDATE':'DATE','LASTMETERREADDATETIME':'DATE','LASTACTIONCODE':'TEXT','LASTACTIONCOMMENT':'TEXT','LASTACTIONREMARKCODE':'TEXT','LASTREGREADING ':'TEXT'}
FIEDLSTODROP = "FILTERSEQUENCE;LASTMETERREADDATE;LASTMETERREADING;PHONE"

def AddFields():
	print 'started adding fields'
	for key in FIELDSTOADD:
		print 'Adding: ' + key + ' as ' + FIELDSTOADD[key]
		gpresult = arcpy.AddField_management(fc,key,FIELDSTOADD[key])
        ##,"#","#","#","#","NULLABLE","NON_REQUIRED","#")
        if (gpresult.status == 4):
            print '\tAdded'
        else:
            print gpresult.getMessages()
	print 'done adding fields'
	
def DropFields():
	print 'started dropping fields'
	gpresult = arcpy.DeleteField_management(fc,FIEDLSTODROP)
	print gpresult.status
	print gpresult.getMessages()
	print 'done dropping fields'

parser = argparse.ArgumentParser(description='ADD | DROP ... Adds or Drops fields based in hard coded array')
parser.add_argument('-ADDORDROP', '--AddorDrop', required=True)
#parser.add_argument('-AddDrop', required=True)

args = parser.parse_args()
if (args.AddorDrop.upper() == 'DROP'):
    print('Dropping fields...')
    DropFields()
elif (args.AddorDrop.upper() == 'ADD'):
    print('Adding fields...')
    AddFields()
else:
    print('Use ADD or DROP')
    

