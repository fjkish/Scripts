import arcpy, os, time,sys,MyLogger

print time.strftime("%H:%M:%S")

##config inputs 
inputGrip_ws      =sys.argv[1]
geocodingLocator  =sys.argv[2]
templateFCInput_ws=sys.argv[3]
switchFC          =sys.argv[4]
cordsys           =sys.argv[5]
input_ws          =sys.argv[6]
stateName         =sys.argv[7]
logId             =sys.argv[8]
logPath           =sys.argv[9]
LOG = MyLogger.Logger(logPath,__file__,logId)
##remove 
sys.exit(1)


# Overwrite output
arcpy.env.overwriteOutput = 1

##input_ws = arcpy.GetParameterAsText(0)
input_ws = r"C:\Data\Projects\Verizon\Ouput\DC_PROCESS.gdb"
inputGrip_ws = r"C:\Data\Projects\Verizon\Ouput\Grip_Polygons.gdb"

ptFC = os.path.join(input_ws, "point")
txtptFC = os.path.join(input_ws, "text_point")
lineFC = os.path.join(input_ws, "lines")

stName = "DC"

#combinedPT = os.path.join(input_ws, "CombinedPT")
combinedPTSorted = os.path.join(input_ws, "CombinedPTSorted")
combinedPTSorted_StatTab = os.path.join(input_ws, "CombinedPTSorted_StatTab")

# Join fields
entnum_mslinkKey = "ENTNUM_MSLINK"
flag_field = "FLAG"

fcJurSetList = [ptFC,txtptFC,lineFC ]

arcpy.env.workspace = input_ws

# Check if tables exist
for fc in fcJurSetList:
    if not arcpy.Exists(fc):
        arcpy.AddError("Table: " + fc + " does not exist")
        # Exit script
        sys.exit()

def PrintGPResult(gpResult):
	if (gpResult.status==4):
		arcpy.AddMessage("Succeeded")
	else:
		arcpy.AddMessage("Did NOT Succeed,status code: " + gpResult.status)
	arcpy.AddMessage(gpResult.getMessages())

def GetGripFC(stName):
	gripFC=''
	if stName == "CA":
		gripFC = inputGrip_ws+"\\CA_GripWC"
	elif stName == "CT":
		gripFC = inputGrip_ws+"\\CT_GripWC"
	elif stName == "DC":
		gripFC = inputGrip_ws+"\\DC_GripWC"
	elif stName == "DE":
		gripFC = inputGrip_ws+"\\DE_GripWC"
	elif stName == "FL":
		gripFC = inputGrip_ws+"\\FL_GripWC"
	elif stName == "MA":
		gripFC = inputGrip_ws+"\\MA_GripWC"
	elif stName == "MD":
		gripFC = inputGrip_ws+"\\MD_GripWC"
	elif stName == "NJ":
		gripFC = inputGrip_ws+"\\NJ_GripWC"
	elif stName == "NY":
		gripFC = inputGrip_ws+"\\NY_GripWC"
	elif stName == "PA":
		gripFC = inputGrip_ws+"\\PA_GripWC"
	elif stName == "RI":
		gripFC = inputGrip_ws+"\\RI_GripWC"
	elif stName == "TX":
		gripFC = inputGrip_ws+"\\TX_GripWC"
	elif stName == "VA":
		gripFC = inputGrip_ws+"\\VA_GripWC"
	else:
		arcpy.AddMessage("stName not in if block")
	return gripFC
		
def SetJur(gripFC):	
	fld_found = arcpy.ListFields(gripFC, "ST_WC")
	if not fld_found:
		arcpy.AddField_management(gripFC, "ST_WC", "TEXT", "50")
	
	arcpy.CalculateField_management(gripFC, "ST_WC", "str(!ST!) + str(!WC!)", "PYTHON_9.3")
	
	index_found = arcpy.ListIndexes(gripFC, "ShortKey_index")
	
	if not index_found:
		arcpy.AddIndex_management(gripFC, "SHORTKEY", "ShortKey_index")
	arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        
## CALCULATING WC NAME and JUR
## WC NAME IS POPULATED USING THE DGN DIRECTORY PATH i.e the the value between the second last and last backlashes from the dgn directory path
## THE DGN DIRECTORY PATH IS STORED IN FME_DATASET_P field (ETL process)
for fc in fcJurSetList:
    print "procssing fc: "+fc
    with arcpy.da.UpdateCursor (fc, ["fme_dataset_p", "WC"]) as cursor:
        for row in cursor:
            wcName = row[0].split("\\")[-2]
            row[1] = wcName
            cursor.updateRow(row)
    fld_found = arcpy.ListFields(fc, "ST_WC")
    if not fld_found:
        print "fc name inside: "+fc
        arcpy.AddField_management(fc, "ST_WC", "TEXT", "50")
    arcpy.CalculateField_management(fc, "ST_WC", "str(!STATE!) + str(!WC!)", "PYTHON_9.3")
    
# CALCULATE JUR NAME USING GRIP POLYGON DATA. THE RELATE KEY IS ST_WC BETWEEN DGN GRAPHICS AND GRIP POLY FC.
for fc in fcJurSetList:
	if arcpy.Exists(fc):
		print fc

		index_found = arcpy.ListIndexes(fc, "ST_WC_index")
		if not index_found:
			arcpy.AddIndex_management(fc, "ST_WC", "ST_WC_index")

		arcpy.MakeFeatureLayer_management(fc, fc+"_lyr")

		gripFC = GetGripFC(stName)
		arcpy.AddMessage("Using " + gripFC)
		SetJur(gripFC)

		arcpy.AddJoin_management(fc+"_lyr", "ST_WC", gripFC+"_lyr", "ST_WC", "KEEP_COMMON")
		arcpy.CalculateField_management(fc+"_lyr", "JUR", "!" + os.path.basename(gripFC) + ".JUR!", "PYTHON_9.3")
## END CALCULATING WC NAME and JUR


## Delete text points that has blank text strings
where_clause = "igds_text_string = ''"
arcpy.MakeFeatureLayer_management(txtptFC, "txtptFC_lyr", where_clause)
if int(arcpy.GetCount_management("txtptFC_lyr").getOutput(0)) > 0:
    print arcpy.GetCount_management ("txtptFC_lyr")
    arcpy.DeleteFeatures_management ("txtptFC_lyr")

print "Adding/calculating ENTNUM_MSLINK field in feature classes..."
fld_found = arcpy.ListFields(ptFC, entnum_mslinkKey)
if not fld_found:
    arcpy.AddField_management(ptFC, entnum_mslinkKey, "TEXT", "100")
arcpy.CalculateField_management(ptFC, entnum_mslinkKey, "str(!JUR!) + str(!WC!) + str(!entity_num!) + str(!mslink!)", "PYTHON_9.3")

fld_found = arcpy.ListFields(ptFC, flag_field)
if not fld_found:
    arcpy.AddField_management(ptFC, flag_field, "TEXT")

fld_found = arcpy.ListFields(txtptFC, entnum_mslinkKey)
if not fld_found:
    arcpy.AddField_management(txtptFC, entnum_mslinkKey, "TEXT", "100")
arcpy.CalculateField_management(txtptFC, entnum_mslinkKey, "str(!JUR!) + str(!WC!) + str(!entity_num!) + str(!mslink!)", "PYTHON_9.3")

# Index field
print "Adding Index..."
index_found = arcpy.ListIndexes(ptFC, "entmslink_index")
if not index_found:
    arcpy.AddIndex_management(ptFC, entnum_mslinkKey, "entmslink_index")

index_found = arcpy.ListIndexes(txtptFC, "entmslink_index")
if not index_found:
    arcpy.AddIndex_management(txtptFC, entnum_mslinkKey, "entmslink_index")

print "Join..."
arcpy.MakeFeatureLayer_management(ptFC, "ptFC_lyr")
arcpy.MakeFeatureLayer_management(txtptFC, "txtptFC_lyr")

print arcpy.GetCount_management (ptFC)
arcpy.AddJoin_management("ptFC_lyr", entnum_mslinkKey, "txtptFC_lyr", entnum_mslinkKey, "KEEP_COMMON")

if int(arcpy.GetCount_management("ptFC_lyr").getOutput(0)) > 0:
    print arcpy.GetCount_management ("ptFC_lyr")
    print "Calculate flag..."
    arcpy.CalculateField_management("ptFC_lyr", "FLAG", "\"YES\"",
                                    "PYTHON_9.3")
arcpy.RemoveJoin_management("ptFC_lyr")

flagfld = "FLAG"
flagcode = "YES"
whereclause = (flagfld + " = '" +flagcode + "'")
arcpy.MakeFeatureLayer_management(ptFC, "ptFC_lyr", whereclause)
print arcpy.GetCount_management ("ptFC_lyr")
arcpy.DeleteFeatures_management ("ptFC_lyr")
print arcpy.GetCount_management (ptFC)
if int(arcpy.GetCount_management(ptFC).getOutput(0)) > 0:
    arcpy.Append_management (ptFC,txtptFC, "NO_TEST")
    
arcpy.Sort_management(txtptFC, combinedPTSorted, "entity_num ASCENDING;mslink ASCENDING;LayerObjectType ASCENDING;str_length ASCENDING", "UR")
arcpy.Statistics_analysis(combinedPTSorted, combinedPTSorted_StatTab, "entity_num FIRST;mslink FIRST;LayerObjectType FIRST;str_length FIRST;OBJECTID FIRST", "mslink")

fld_found = arcpy.ListFields(combinedPTSorted, "KEEP_POINT")
if not fld_found:
    arcpy.AddField_management(combinedPTSorted, "KEEP_POINT", "TEXT")

if arcpy.Exists(combinedPTSorted_StatTab):
   arcpy.MakeTableView_management(combinedPTSorted_StatTab, "combinedPTSorted_StatTab_lyr")
   arcpy.MakeFeatureLayer_management(combinedPTSorted, "combinedPTSorted_lyr")

arcpy.AddJoin_management("combinedPTSorted_lyr", "OBJECTID", "combinedPTSorted_StatTab_lyr", "FIRST_OBJECTID", "KEEP_COMMON")
arcpy.CalculateField_management("combinedPTSorted_lyr", "KEEP_POINT", "\"YES\"",
                                    "PYTHON_9.3")
arcpy.RemoveJoin_management("combinedPTSorted_lyr")
arcpy.FeatureClassToFeatureClass_conversion(combinedPTSorted, input_ws, "FinalPoints", "KEEP_POINT = 'YES'")
        
print time.strftime("%H:%M:%S")
