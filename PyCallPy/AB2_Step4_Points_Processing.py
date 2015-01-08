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
stName = "DC"

# Geocoding Locator
GeocodingLocator = r"G:\Locators\USA_StreetAddress"


ptFC_SP = os.path.join(input_ws, "FinalPoints")
lnFC_SP = os.path.join(input_ws, "Lines")

ptFC = os.path.join(input_ws, "FinalPoints_Project")
lnFC = os.path.join(input_ws, "Lines_Project")

## Tables
FDHSplitter = os.path.join(input_ws, "FDHSplitter")
VirtualMdu = os.path.join(input_ws, "VirtualMdu")
FDH = os.path.join(input_ws, "FDH")
FDT = os.path.join(input_ws, "FDT")
FDTServRange = os.path.join(input_ws, "FDTServRange")
FDTAddressRange = os.path.join(input_ws, "FDTAddressRange")
FDTAddress = os.path.join(input_ws, "FDTAddress")



fcList = [ptFC,lnFC]

# Projecting State Plane Coordiante System Feature classes to WGC Coordiante System before processing them with ICGS text file data
if arcpy.Exists(ptFC):
    arcpy.Delete_management (ptFC)
arcpy.Project_management(ptFC_SP, ptFC, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", "WGS_1984_(ITRF00)_To_NAD_1983", "PROJCS['NAD_1983_StatePlane_Maryland_FIPS_1900_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1312333.333333333],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-77.0],PARAMETER['Standard_Parallel_1',38.3],PARAMETER['Standard_Parallel_2',39.45],PARAMETER['Latitude_Of_Origin',37.66666666666666],UNIT['Foot_US',0.3048006096012192]]")

if arcpy.Exists(lnFC):
    arcpy.Delete_management (lnFC)
arcpy.Project_management(lnFC_SP, lnFC, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", "WGS_1984_(ITRF00)_To_NAD_1983", "PROJCS['NAD_1983_StatePlane_Maryland_FIPS_1900_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1312333.333333333],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-77.0],PARAMETER['Standard_Parallel_1',38.3],PARAMETER['Standard_Parallel_2',39.45],PARAMETER['Latitude_Of_Origin',37.66666666666666],UNIT['Foot_US',0.3048006096012192]]")

# Join fields
dgnKey = "DGN_KEY"
txtKey = "TEXT_KEY"
txtIPIDKey = "IPIDKEY"

cablekey_fld = "CABLE_KEY"
ipidkey_fld = "IPIDKEY"
cableid_fld = "CABLE_ID"
graphic_fld = "GraphicSource"
flag_field = "FLAG"

# Check if tables exist
for fc in fcList:
    if not arcpy.Exists(fc):
        arcpy.AddError("Table: " + fc + " does not exist")
        # Exit script
        sys.exit()

# Add/Calculate X and Y fields for FinalPoints projected feature class.
arcpy.AddXY_management(ptFC)

print "Adding/calculating dgnKey field in feature classes..."
fld_found = arcpy.ListFields(ptFC, dgnKey)
if not fld_found:
    arcpy.AddField_management(ptFC, dgnKey, "TEXT")
arcpy.CalculateField_management(ptFC, dgnKey, "str(!JUR!) + str(!WC! + str(!MSLINK!))", "PYTHON_9.3")

print "Adding/calculating key fields in tables..."
fld_found = arcpy.ListFields(FDH, cablekey_fld)
if not fld_found:
    arcpy.AddField_management(FDH, cablekey_fld, "TEXT")
arcpy.CalculateField_management(FDH, cablekey_fld, "str(!JUR!) + str(!WC! + str(!CABLE_ID!))", "PYTHON_9.3")

fld_found = arcpy.ListFields(FDT, cablekey_fld)
if not fld_found:
    arcpy.AddField_management(FDT, cablekey_fld, "TEXT")
arcpy.CalculateField_management(FDT, cablekey_fld, "str(!JUR!) + str(!WC! + str(!CABLE_ID!))", "PYTHON_9.3")


# Index fields
print "Indexing relate fields..."
index_found = arcpy.ListIndexes(ptFC, "dgnKey_index")
if not index_found:
    arcpy.AddIndex_management(ptFC, dgnKey, "dgnKey_index")

index_found = arcpy.ListIndexes(FDT, "cablekey_index")
if not index_found:
    arcpy.AddIndex_management(FDT, cablekey_fld, "cablekey_index")

index_found = arcpy.ListIndexes(FDH, "cablekey_index")
if not index_found:
    arcpy.AddIndex_management(FDH, cablekey_fld, "cablekey_index")

#******************* FDTAddressRange and FDT Address *****************
if arcpy.Exists(FDTServRange):
    if int(arcpy.GetCount_management(FDTServRange).getOutput(0)) > 0:
        print FDTServRange+" Table row count before removing duplicates = " +str(arcpy.GetCount_management (FDTServRange))
        if arcpy.Exists(FDTAddressRange):
            arcpy.Delete_management (FDTAddressRange)
        print "Removing duplicates from FDTServRange to create FDTAddressRange Table."
        arcpy.Statistics_analysis(FDTServRange, FDTAddressRange, "ADDRESS_ID FIRST", "JUR;WC;IPID;SERVING_RANGE;MARK_STREET_NAME;SUB_ADDRESS;TERRITORIAL_UNIT;ZIP_CODE")
        print "Completed removing duplicates."
        print FDTAddressRange+" Table row count after duplicates removed = " +str(arcpy.GetCount_management (FDTAddressRange))
        arcpy.AddField_management(FDTAddressRange, "ADDRESS_CONCAT", "TEXT", "255")
        arcpy.AddField_management(FDTAddressRange, "IPIDKEY", "TEXT", "50")
        arcpy.CalculateField_management(FDTAddressRange, "IPIDKEY", "!JUR!+ !WC!+str( !IPID!)", "PYTHON_9.3", "")

        where_clause = ("SERVING_RANGE IS NOT NULL AND MARK_STREET_NAME IS NOT NULL AND SUB_ADDRESS IS NULL")
        arcpy.MakeTableView_management(FDTAddressRange, "FDTAddressRange_Lyr",where_clause)
        #print arcpy.GetCount_management ("FDTAddressRange_Lyr")
        arcpy.CalculateField_management("FDTAddressRange_Lyr", "ADDRESS_CONCAT", "!SERVING_RANGE!+\" \"+!MARK_STREET_NAME!", "PYTHON_9.3", "")
        
        where_clause = ("SERVING_RANGE IS NOT NULL AND MARK_STREET_NAME IS NULL AND SUB_ADDRESS IS NOT NULL")
        arcpy.MakeTableView_management(FDTAddressRange, "FDTAddressRange_Lyr",where_clause)
        #print arcpy.GetCount_management ("FDTAddressRange_Lyr")
        arcpy.CalculateField_management("FDTAddressRange_Lyr", "ADDRESS_CONCAT", "!SERVING_RANGE!+\" \"+!SUB_ADDRESS!", "PYTHON_9.3", "")
                        
        where_clause = ("SERVING_RANGE IS NULL AND MARK_STREET_NAME IS NOT NULL AND SUB_ADDRESS IS NOT NULL")
        arcpy.MakeTableView_management(FDTAddressRange, "FDTAddressRange_Lyr",where_clause)
        #print arcpy.GetCount_management ("FDTAddressRange_Lyr")
        arcpy.CalculateField_management("FDTAddressRange_Lyr", "ADDRESS_CONCAT", "!MAKR_STREET_NAME!+\" \"+!SUB_ADDRESS!", "PYTHON_9.3", "")

        where_clause = ("SERVING_RANGE IS NOT NULL AND MARK_STREET_NAME IS NOT NULL AND SUB_ADDRESS IS NOT NULL")
        arcpy.MakeTableView_management(FDTAddressRange, "FDTAddressRange_Lyr",where_clause)
        #print arcpy.GetCount_management ("FDTAddressRange_Lyr")
        arcpy.CalculateField_management("FDTAddressRange_Lyr", "ADDRESS_CONCAT", "!SERVING_RANGE!+\" \"+!MARK_STREET_NAME!+\" \"+!SUB_ADDRESS!", "PYTHON_9.3", "")
#Geocoding FDTAddressRangeTable
        if arcpy.Exists(FDTAddress):
            arcpy.Delete_management (FDTAddress)
        print "Geocoding FDTAddressRange Table to create FDTAddress Point Feature class..."
        arcpy.GeocodeAddresses_geocoding(FDTAddressRange, GeocodingLocator, "Street ADDRESS_CONCAT;City TERRITORIAL_UNIT;State <None>;ZIP ZIP_CODE", FDTAddress, "STATIC")
        print "Geocoding complete..."

    index_found = arcpy.ListIndexes(FDTAddress, "ipidkey_index")
    if not index_found:
        arcpy.AddIndex_management(FDTAddress, ipidkey_fld, "ipidkey_index")
##******************* FDTAddressRange and FDT Address END *****************

## *******************FDH SETTING GRAPHIC SOURCE A AND B *********************
if arcpy.Exists(FDH):
    if int(arcpy.GetCount_management(FDH).getOutput(0)) > 0:
        print arcpy.GetCount_management (FDH)
        
        fld_found = arcpy.ListFields(FDH, txtKey)
        if not fld_found:
            arcpy.AddField_management(FDH, txtKey, "TEXT")
        #arcpy.CalculateField_management(FDH, txtKey, "str(!JUR!) + str(!WC! + str(!MSLINK!))", "PYTHON_9.3")
        arcpy.CalculateField_management(FDH, txtKey, "str(!JUR!) + str(!WC! + str(!Graphic_Link_Num!))", "PYTHON_9.3")

        fld_found = arcpy.ListFields(FDH, "FOUND_DGN_FEATURE")
        if not fld_found:
            arcpy.AddField_management(FDH, "FOUND_DGN_FEATURE", "TEXT")

        fld_found = arcpy.ListFields(FDH, "POINT_X")
        if not fld_found:
            arcpy.AddField_management(FDH, "POINT_X", "DOUBLE")
            
        fld_found = arcpy.ListFields(FDH, "POINT_Y")
        if not fld_found:
            arcpy.AddField_management(FDH, "POINT_Y", "DOUBLE")

        print "Adding Index..."
        index_found = arcpy.ListIndexes(FDH, "txtKey_index")
        if not index_found:
            arcpy.AddIndex_management(FDH, txtKey, "txtKey_index")

        fld_found = arcpy.ListFields(FDH, txtIPIDKey)
        if not fld_found:
            arcpy.AddField_management(FDH, txtIPIDKey, "TEXT")
        arcpy.CalculateField_management(FDH, txtIPIDKey, "str(!JUR!) + str(!WC! + str(!IPID!))", "PYTHON_9.3")

        # Join text to geometry and calculate fields. Calculate sets the FDH tabular POINT_X AND POINT_Y with geometry point_x and point_y gields. 
        arcpy.MakeTableView_management(FDH, "FDH_lyr")
        arcpy.MakeFeatureLayer_management(ptFC, "ptFC_lyr", "entity_num = 18")
        print "printing count of fdh point layer"
        print arcpy.GetCount_management ("ptFC_lyr")
        arcpy.AddJoin_management("FDH_lyr", txtKey, "ptFC_lyr", dgnKey, "KEEP_COMMON")
        arcpy.CalculateField_management("FDH_lyr", "FOUND_DGN_FEATURE", "\"YES\"",
                                    "PYTHON_9.3")
        arcpy.CalculateField_management("FDH_lyr", "POINT_X", "!" + os.path.basename(ptFC) + ".POINT_X!",
                                    "PYTHON_9.3")
        arcpy.CalculateField_management("FDH_lyr", "POINT_Y", "!" + os.path.basename(ptFC) + ".POINT_Y!",
                                    "PYTHON_9.3")
        arcpy.CalculateField_management("FDH_lyr", "GRAPHICSOURCE", "\"B\"",
                                    "PYTHON_9.3")
        arcpy.RemoveJoin_management("FDH_lyr")

        #when geometry match not found, setting the POINT_X AND POINT_Y with FDH tabular data LONG and LAT fields
        where_clause = ("FOUND_DGN_FEATURE IS NULL AND TO_LONG < -1")
        print where_clause

        print arcpy.GetCount_management (FDH)
        arcpy.MakeTableView_management(FDH, "FDH_lyr2", where_clause)
        print arcpy.GetCount_management ("FDH_lyr2")
        arcpy.CalculateField_management("FDH_lyr2", "POINT_X", "!TO_LONG!", "PYTHON_9.3")
        arcpy.CalculateField_management("FDH_lyr2", "POINT_Y", "!TO_LAT!", "PYTHON_9.3")
        arcpy.CalculateField_management("FDH_lyr2", "GRAPHICSOURCE", "\"A\"","PYTHON_9.3")
##*******************FDH SETTING GRAPHIC SOURCE A AND B END *********************


## *******************FDT SETTING GRAPHIC SOURCE A AND B ************************
if arcpy.Exists(FDT):
    if int(arcpy.GetCount_management(FDT).getOutput(0)) > 0:
        print FDT+" Table Row Count = " +str(arcpy.GetCount_management (FDT))
        print "Adding temporary fields to FDT Table...."
        fld_found = arcpy.ListFields(FDT, txtKey)
        if not fld_found:
            arcpy.AddField_management(FDT, txtKey, "TEXT")
        #arcpy.CalculateField_management(FDT, txtKey, "str(!JUR!) + str(!WC! + str(!MSLINK!))", "PYTHON_9.3")
        arcpy.CalculateField_management(FDT, txtKey, "str(!JUR!) + str(!WC! + str(!Graphic_Link_Num!))", "PYTHON_9.3")

        fld_found = arcpy.ListFields(FDT, "FOUND_DGN_FEATURE")
        if not fld_found:
            arcpy.AddField_management(FDT, "FOUND_DGN_FEATURE", "TEXT")

        fld_found = arcpy.ListFields(FDT, "POINT_X")
        if not fld_found:
            arcpy.AddField_management(FDT, "POINT_X", "DOUBLE")
            
        fld_found = arcpy.ListFields(FDT, "POINT_Y")
        if not fld_found:
            arcpy.AddField_management(FDT, "POINT_Y", "DOUBLE")

        print "Adding Index..."
        index_found = arcpy.ListIndexes(FDT, "txtKey_index")
        if not index_found:
            arcpy.AddIndex_management(FDT, txtKey, "txtKey_index")

        fld_found = arcpy.ListFields(FDT, txtIPIDKey)
        if not fld_found:
            arcpy.AddField_management(FDT, txtIPIDKey, "TEXT")
        arcpy.CalculateField_management(FDT, txtIPIDKey, "str(!JUR!) + str(!WC! + str(!IPID!))", "PYTHON_9.3")

        # Join text to geometry and calculate fields. Calculate sets the FDT tabular POINT_X AND POINT_Y with geometry point_x and point_y gields. 
        print "Joining FDT Table to Point Geometry Feature class..."
        arcpy.MakeTableView_management(FDT, "FDT_lyr")
        arcpy.MakeFeatureLayer_management(ptFC, "ptFC_lyr", "entity_num = 13")
        print "Printing count of FDT point layer which has Entity Num = 13"
        print arcpy.GetCount_management ("ptFC_lyr")
        arcpy.AddJoin_management("FDT_lyr", txtKey, "ptFC_lyr", dgnKey, "KEEP_COMMON")
        print "Updating FDT table X and Y columns with Geometry X and Y..."
        arcpy.CalculateField_management("FDT_lyr", "FOUND_DGN_FEATURE", "\"YES\"","PYTHON_9.3")
        arcpy.CalculateField_management("FDT_lyr", "POINT_X", "!" + os.path.basename(ptFC) + ".POINT_X!","PYTHON_9.3")
        arcpy.CalculateField_management("FDT_lyr", "POINT_Y", "!" + os.path.basename(ptFC) + ".POINT_Y!","PYTHON_9.3")
        arcpy.CalculateField_management("FDT_lyr", "GRAPHICSOURCE", "\"B\"","PYTHON_9.3")
        arcpy.RemoveJoin_management("FDT_lyr")

	#when geometry match not found, setting the POINT_X AND POINT_Y with FDT tabular data LONG and LAT fields
        #where_clause = ("FOUND_DGN_FEATURE IS NULL")
        where_clause = ("FOUND_DGN_FEATURE IS NULL AND TO_LONG < -1")
        print where_clause

        #print arcpy.GetCount_management (FDT)
        arcpy.MakeTableView_management(FDT, "FDT_lyr2", where_clause)
        print FDT+" table rows that to process for GraphicSource A: " + str(arcpy.GetCount_management ("FDT_lyr2"))
        print "Above rows will use FDT table X and Y fields to generate points (Graphic Source Set to A)"
        arcpy.CalculateField_management("FDT_lyr2", "POINT_X", "!TO_LONG!", "PYTHON_9.3")
        arcpy.CalculateField_management("FDT_lyr2", "POINT_Y", "!TO_LAT!", "PYTHON_9.3")
        arcpy.CalculateField_management("FDT_lyr2", "GRAPHICSOURCE", "\"A\"", "PYTHON_9.3")
##******************* FDT SETTING GRAPHIC SOURCE A AND B END *********************


##********* FDH AND FDT SETTING GRAPHIC SOURCE C AND D ***************************
def processFields(input_tbl, relate_tbl, relate_fld, pntx_fld, pnty_fld, graphic_fld, graphic_val):
    # Loop through each record input table
    with arcpy.da.UpdateCursor(input_tbl, [relate_fld, graphic_fld, "POINT_X", "POINT_Y"]) as cur:
        for row in cur:
            # Loop through each record in the relate table on relate field
            where = arcpy.AddFieldDelimiters(relate_tbl, relate_fld) + " = '" + row[0] + "'"
            count, x_sum, y_sum = 0, 0, 0
            with arcpy.da.SearchCursor(relate_tbl, [pntx_fld, pnty_fld], where) as cur_rel:
                for row_rel in cur_rel:
                    # Average POINT_X and POINT_Y fields
                    if (row_rel[0] is not None and row_rel[0] != 0 and
                        row_rel[1] is not None and row_rel[1] != 0):
                        x_sum += row_rel[0]
                        y_sum += row_rel[1]
                        count += 1
            # Solve average
            if count > 0:
                x_avg = x_sum / count
                y_avg = y_sum / count
                # Update POINT_X, POINT_Y, and GraphicSource fields in input table
                row[1], row[2], row[3] = graphic_val, x_avg, y_avg
                cur.updateRow(row)
                
# SET FDH GRAPHIC SOURCE - C
print "SET FDH GRAPHIC SOURCE - C"
where = arcpy.AddFieldDelimiters(input_ws, graphic_fld) + " IS NULL AND " + arcpy.AddFieldDelimiters(input_ws, cableid_fld) + " <> 'H999'"
arcpy.MakeTableView_management(FDH, "FDH", where)
num_feat = arcpy.GetCount_management("FDH").getOutput(0)
print num_feat + " features returned"
processFields("FDH", FDT, cablekey_fld, "POINT_X", "POINT_Y", graphic_fld, "C")

# SET FDT GRAPHIC SOURCE - C
print "SET FDT GRAPHIC SOURCE - C"
where = arcpy.AddFieldDelimiters(input_ws, graphic_fld) + " IS NULL"
arcpy.MakeTableView_management(FDT, "FDT", where)
num_feat = arcpy.GetCount_management("FDT").getOutput(0)
print num_feat + " features returned"
processFields("FDT", FDH, cablekey_fld, "POINT_X", "POINT_Y", graphic_fld, "C")

# SET FDT GRAPHIC SOURCE - D
print "SET FDT GRAPHIC SOURCE - D"
where = arcpy.AddFieldDelimiters(input_ws, graphic_fld) + " = 'C' OR " + arcpy.AddFieldDelimiters(input_ws, graphic_fld) + " IS NULL"
arcpy.MakeTableView_management(FDT, "FDT", where)
num_feat = arcpy.GetCount_management("FDT").getOutput(0)
print num_feat + " features returned"
processFields("FDT", FDTAddress, ipidkey_fld, "X", "Y", graphic_fld, "D")

# SET FDH GRAPHIC SOURCE - D
print "SET FDT GRAPHIC SOURCE - D"
where = ("(" + arcpy.AddFieldDelimiters(input_ws, graphic_fld) + " IS NULL AND " + arcpy.AddFieldDelimiters(input_ws, cableid_fld) +
         " <> 'H999') OR " + arcpy.AddFieldDelimiters(input_ws, graphic_fld) + " = 'C'")
arcpy.MakeTableView_management(FDH, "FDH", where)
num_feat = arcpy.GetCount_management("FDH").getOutput(0)
print num_feat + " features returned"
processFields("FDH", FDT, cablekey_fld, "POINT_X", "POINT_Y", graphic_fld, "D")

#*********FDT and FDH Feature class creation
# FDT
# Process: Make XY Event Layer
where_clause = ("GRAPHICSOURCE IN ('A', 'B', 'C', 'D')")
print where_clause
# Join text to geometry and calculate fields 
arcpy.MakeTableView_management(FDT, "FDT_lyr3",where_clause)
print "Total Number of FDT rows for geometry generation: "+ str(arcpy.GetCount_management ("FDT_lyr3"))

FDT_ForXY = os.path.join(input_ws, "FDT_ForXY")
if arcpy.Exists(FDT_ForXY):
    arcpy.Delete_management (FDT_ForXY)
arcpy.TableToTable_conversion("FDT_lyr3", input_ws, "FDT_ForXY")
arcpy.MakeXYEventLayer_management(FDT_ForXY, "POINT_X", "POINT_Y", "FDT_ForXY_Lyr", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision", "")

# Process: Feature Class to Feature Class
FDT_FC = os.path.join(input_ws, "FDT_FC")
if arcpy.Exists(FDT_FC):
    arcpy.Delete_management (FDT_FC)
arcpy.FeatureClassToFeatureClass_conversion("FDT_ForXY_Lyr", input_ws, "FDT_FC")
arcpy.MakeFeatureLayer_management(FDT_FC, "FDT_FC_lyr")
arcpy.CalculateField_management("FDT_FC_lyr", "SIZE_", "(!HIGH_PAIR!- !LOW_PAIR!)+1", "PYTHON_9.3", "")

# Process: Making FDT_NotProcessed Table 
arcpy.MakeTableView_management(FDT, "FDT_lyrNP", "GRAPHICSOURCE IS NULL")

# FDH
# Process: Make XY Event Layer
where_clause = ("GRAPHICSOURCE IN ('A', 'B', 'C', 'D')")
print where_clause
# Join text to geometry and calculate fields 
arcpy.MakeTableView_management(FDH, "FDH_lyr3",where_clause)
print arcpy.GetCount_management ("FDH_lyr3")

FDH_ForXY = os.path.join(input_ws, "FDH_ForXY")
if arcpy.Exists(FDH_ForXY):
    arcpy.Delete_management (FDH_ForXY)
arcpy.TableToTable_conversion("FDH_lyr3", input_ws, "FDH_ForXY")
arcpy.MakeXYEventLayer_management(FDH_ForXY, "POINT_X", "POINT_Y", "FDH_ForXY_Lyr", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision", "")

# Process: Feature Class to Feature Class
FDH_FC = os.path.join(input_ws, "FDH_FC")
if arcpy.Exists(FDH_FC):
    arcpy.Delete_management (FDH_FC)
arcpy.FeatureClassToFeatureClass_conversion("FDH_ForXY_Lyr", input_ws, "FDH_FC")

arcpy.MakeFeatureLayer_management(FDH_FC, "FDH_FC_lyr1", "HIGH_PAIR < 144")
arcpy.MakeFeatureLayer_management(FDH_FC, "FDH_FC_lyr2", "HIGH_PAIR >= 144")

print arcpy.GetCount_management ("FDH_FC_lyr1")
arcpy.CalculateField_management("FDH_FC_lyr1", "SIZE_", "144", "PYTHON_9.3")
arcpy.CalculateField_management("FDH_FC_lyr2", "SIZE_", "!HIGH_PAIR!", "PYTHON_9.3")

##********* FDT and FDH Feature Class Creation End *********

    
##*******************VIRTUAL MDU*********************
if arcpy.Exists(VirtualMdu):
    if int(arcpy.GetCount_management(VirtualMdu).getOutput(0)) > 0:
        print arcpy.GetCount_management (VirtualMdu)
        
        fld_found = arcpy.ListFields(VirtualMdu, txtKey)
        if not fld_found:
            arcpy.AddField_management(VirtualMdu, txtKey, "TEXT")
        #arcpy.CalculateField_management(VirtualMdu, txtKey, "str(!JUR!) + str(!WC! + str(!MSLINK!))", "PYTHON_9.3")
        arcpy.CalculateField_management(VirtualMdu, txtKey, "str(!JUR!) + str(!WC! + str(!Graphic_Link_Num!))", "PYTHON_9.3")

        fld_found = arcpy.ListFields(VirtualMdu, "FOUND_DGN_FEATURE")
        if not fld_found:
            arcpy.AddField_management(VirtualMdu, "FOUND_DGN_FEATURE", "TEXT")

        fld_found = arcpy.ListFields(VirtualMdu, "POINT_X")
        if not fld_found:
            arcpy.AddField_management(VirtualMdu, "POINT_X", "DOUBLE")
            
        fld_found = arcpy.ListFields(VirtualMdu, "POINT_Y")
        if not fld_found:
            arcpy.AddField_management(VirtualMdu, "POINT_Y", "DOUBLE")

        print "Adding Index..."
        index_found = arcpy.ListIndexes(VirtualMdu, "txtKey_index")
        if not index_found:
            arcpy.AddIndex_management(VirtualMdu, txtKey, "txtKey_index")

        fld_found = arcpy.ListFields(VirtualMdu, txtIPIDKey)
        if not fld_found:
            arcpy.AddField_management(VirtualMdu, txtIPIDKey, "TEXT")
        arcpy.CalculateField_management(VirtualMdu, txtIPIDKey, "str(!JUR!) + str(!WC! + str(!IPID!))", "PYTHON_9.3")

        # Join text to geometry and calculate fields 
        arcpy.MakeTableView_management(VirtualMdu, "VirtualMdu_lyr")
        arcpy.MakeFeatureLayer_management(ptFC, "ptFC_lyr")
        arcpy.AddJoin_management("VirtualMdu_lyr", txtKey, "ptFC_lyr", dgnKey, "KEEP_COMMON")
        arcpy.CalculateField_management("VirtualMdu_lyr", "FOUND_DGN_FEATURE", "\"YES\"",
                                    "PYTHON_9.3")
        arcpy.CalculateField_management("VirtualMdu_lyr", "POINT_X", "!" + os.path.basename(ptFC) + ".POINT_X!",
                                    "PYTHON_9.3")
        arcpy.CalculateField_management("VirtualMdu_lyr", "POINT_Y", "!" + os.path.basename(ptFC) + ".POINT_Y!",
                                    "PYTHON_9.3")
        arcpy.CalculateField_management("VirtualMdu_lyr", "GRAPHICSOURCE", "\"B\"",
                                    "PYTHON_9.3")
        arcpy.RemoveJoin_management("VirtualMdu_lyr")

#Processing only DC test WC data....
        #jurName = "DC"
        #wcName = "0WLC"
        #where_clause = ("JUR = '"+jurName +"' AND WC = '"+wcName+"' AND FOUND_DGN_FEATURE IS NULL ")
        where_clause = ("FOUND_DGN_FEATURE IS NULL")

        print where_clause

        print arcpy.GetCount_management (VirtualMdu)
        arcpy.MakeTableView_management(VirtualMdu, "VirtualMdu_lyr2", where_clause)
        print arcpy.GetCount_management ("VirtualMdu_lyr2")
        arcpy.CalculateField_management("VirtualMdu_lyr2", "POINT_X", "!TO_LONG!", "PYTHON_9.3")
        arcpy.CalculateField_management("VirtualMdu_lyr2", "POINT_Y", "!TO_LAT!", "PYTHON_9.3")
        arcpy.CalculateField_management("VirtualMdu_lyr2", "GRAPHICSOURCE", "\"A\"", "PYTHON_9.3")
#Process: Make XY Event Layer
        where_clause = ("GRAPHICSOURCE IN ('A', 'B')")
        print where_clause
        # Join text to geometry and calculate fields 
        arcpy.MakeTableView_management(VirtualMdu, "VirtualMdu_lyr3",where_clause)
        print arcpy.GetCount_management ("VirtualMdu_lyr3")
        
        VirtualMdu_ForXY = os.path.join(input_ws, "VirtualMdu_ForXY")
        if arcpy.Exists(VirtualMdu_ForXY):
            arcpy.Delete_management (VirtualMdu_ForXY)
        arcpy.TableToTable_conversion("VirtualMdu_lyr3", input_ws, "VirtualMdu_ForXY")
        arcpy.MakeXYEventLayer_management(VirtualMdu_ForXY, "POINT_X", "POINT_Y", "VirtualMdu_ForXY_Lyr", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision", "")
#        arcpy.MakeXYEventLayer_management(VirtualMdu_ForXY, "POINT_X", "POINT_Y", VirtualMdu_ForXY_Layer, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision", "")

# Process: Feature Class to Feature Class
        VirtualMdu_FC = os.path.join(input_ws, "VirtualMdu_FC")
        if arcpy.Exists(VirtualMdu_FC):
            arcpy.Delete_management (VirtualMdu_FC)
        arcpy.FeatureClassToFeatureClass_conversion("VirtualMdu_ForXY_Lyr", input_ws, "VirtualMdu_FC")
## ******************* END VIRTUAL MDU *********************

## *******************FDH SPLITTER*********************
if arcpy.Exists(FDHSplitter):
    if int(arcpy.GetCount_management(FDHSplitter).getOutput(0)) > 0:
        print arcpy.GetCount_management (FDHSplitter)
        
        fld_found = arcpy.ListFields(FDHSplitter, txtKey)
        if not fld_found:
            arcpy.AddField_management(FDHSplitter, txtKey, "TEXT")
        #arcpy.CalculateField_management(FDHSplitter, txtKey, "str(!JUR!) + str(!WC! + str(!MSLINK!))", "PYTHON_9.3")
        arcpy.CalculateField_management(FDHSplitter, txtKey, "str(!JUR!) + str(!WC! + str(!Graphic_Link_Num!))", "PYTHON_9.3")

        fld_found = arcpy.ListFields(FDHSplitter, "FOUND_DGN_FEATURE")
        if not fld_found:
            arcpy.AddField_management(FDHSplitter, "FOUND_DGN_FEATURE", "TEXT")

        fld_found = arcpy.ListFields(FDHSplitter, "POINT_X")
        if not fld_found:
            arcpy.AddField_management(FDHSplitter, "POINT_X", "DOUBLE")
            
        fld_found = arcpy.ListFields(FDHSplitter, "POINT_Y")
        if not fld_found:
            arcpy.AddField_management(FDHSplitter, "POINT_Y", "DOUBLE")

        fld_found = arcpy.ListFields(FDHSplitter, "OBJECT_RESET")
        if not fld_found:
            arcpy.AddField_management(FDHSplitter, "OBJECT_RESET", "TEXT")

        print "Adding Index..."
        index_found = arcpy.ListIndexes(FDHSplitter, "txtKey_index")
        if not index_found:
            arcpy.AddIndex_management(FDHSplitter, txtKey, "txtKey_index")

        fld_found = arcpy.ListFields(FDHSplitter, txtIPIDKey)
        if not fld_found:
            arcpy.AddField_management(FDHSplitter, txtIPIDKey, "TEXT")
        arcpy.CalculateField_management(FDHSplitter, txtIPIDKey, "str(!JUR!) + str(!WC! + str(!IPID!))", "PYTHON_9.3")

        # Join text to geometry and calculate fields 
        arcpy.MakeTableView_management(FDHSplitter, "FDHSplitter_lyr")
        arcpy.MakeFeatureLayer_management(ptFC, "ptFC_lyr")
        arcpy.AddJoin_management("FDHSplitter_lyr", txtKey, "ptFC_lyr", dgnKey, "KEEP_COMMON")
        arcpy.CalculateField_management("FDHSplitter_lyr", "FOUND_DGN_FEATURE", "\"YES\"", "PYTHON_9.3")
        arcpy.CalculateField_management("FDHSplitter_lyr", "POINT_X", "!" + os.path.basename(ptFC) + ".POINT_X!", "PYTHON_9.3")
        arcpy.CalculateField_management("FDHSplitter_lyr", "POINT_Y", "!" + os.path.basename(ptFC) + ".POINT_Y!", "PYTHON_9.3")
        arcpy.CalculateField_management("FDHSplitter_lyr", "GRAPHICSOURCE", "\"B\"", "PYTHON_9.3")
        arcpy.RemoveJoin_management("FDHSplitter_lyr")

## Processing only DC test WC data....
        #jurName = "DC"
        #wcName = "0WLC"
        #where_clause = ("JUR = '"+jurName +"' AND WC = '"+wcName+"' AND FOUND_DGN_FEATURE IS NULL ")
        where_clause = ("FOUND_DGN_FEATURE IS NULL")

        print where_clause

        print arcpy.GetCount_management (FDHSplitter)
        arcpy.MakeTableView_management(FDHSplitter, "FDHSplitter_lyr2", where_clause)
        print arcpy.GetCount_management ("FDHSplitter_lyr2")
        arcpy.CalculateField_management("FDHSplitter_lyr2", "POINT_X", "!TO_LONG!", "PYTHON_9.3")
        arcpy.CalculateField_management("FDHSplitter_lyr2", "POINT_Y", "!TO_LAT!", "PYTHON_9.3")
        arcpy.CalculateField_management("FDHSplitter_lyr2", "GRAPHICSOURCE", "\"A\"", "PYTHON_9.3")

# Reseting FDHSplitter X and Y with FDH X and Y when LONGKEY match found
        index_found = arcpy.ListIndexes(FDHSplitter, "LongKey_index")
        if not index_found:
            arcpy.AddIndex_management(FDHSplitter, "LONGKEY", "LongKey_index")

        index_found = arcpy.ListIndexes(FDH_FC, "LongKey_index")
        if not index_found:
            arcpy.AddIndex_management(FDH_FC, "LONGKEY", "LongKey_index")

        arcpy.MakeTableView_management(FDHSplitter, "FDHSplitter_lyr")
        arcpy.MakeFeatureLayer_management(FDH_FC, "FDH_FC_lyr")
        
        arcpy.AddJoin_management("FDHSplitter_lyr", "LONGKEY", "FDH_FC_lyr", "LONGKEY", "KEEP_COMMON")
        arcpy.CalculateField_management("FDHSplitter_lyr", "OBJECT_RESET", "\"Y\"", "PYTHON_9.3")
        arcpy.CalculateField_management("FDHSplitter_lyr", "POINT_X", "!" + os.path.basename(FDH_FC) + ".POINT_X!", "PYTHON_9.3")
        arcpy.CalculateField_management("FDHSplitter_lyr", "POINT_Y", "!" + os.path.basename(FDH_FC) + ".POINT_Y!", "PYTHON_9.3")

# Process: Make XY Event Layer
        where_clause = ("GRAPHICSOURCE IN ('A', 'B')")
        print where_clause
        # Join text to geometry and calculate fields 
        arcpy.MakeTableView_management(FDHSplitter, "FDHSplitter_lyr3",where_clause)
        print arcpy.GetCount_management ("FDHSplitter_lyr3")
        
        FDHSplitter_ForXY = os.path.join(input_ws, "FDHSplitter_ForXY")
        if arcpy.Exists(FDHSplitter_ForXY):
            arcpy.Delete_management (FDHSplitter_ForXY)
        arcpy.TableToTable_conversion("FDHSplitter_lyr3", input_ws, "FDHSplitter_ForXY")
        arcpy.MakeXYEventLayer_management(FDHSplitter_ForXY, "POINT_X", "POINT_Y", "FDHSplitter_ForXY_Lyr", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision", "")
#        arcpy.MakeXYEventLayer_management(FDHSplitter_ForXY, "POINT_X", "POINT_Y", FDHSplitter_ForXY_Layer, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision", "")

# Process: Feature Class to Feature Class
        FDHSplitter_FC = os.path.join(input_ws, "FDHSplitter_FC")
        if arcpy.Exists(FDHSplitter_FC):
            arcpy.Delete_management (FDHSplitter_FC)
        arcpy.FeatureClassToFeatureClass_conversion("FDHSplitter_ForXY_Lyr", input_ws, "FDHSplitter_FC")
## *******************SPLITTER END *********************


## ******** SETTING PROVCODE USING GRIP POLYGON FEATURE CLASS **********
gripSetfcList = ["FDH_FC", "FDHSplitter_FC", "FDT_FC", "VIRTUALMDU_FC"]
arcpy.env.workspace = input_ws
for fc in gripSetfcList:
    if arcpy.Exists(fc):
        print fc
        index_found = arcpy.ListIndexes(fc, "ShortKey_index")
        if not index_found:
            arcpy.AddIndex_management(fc, "SHORTKEY", "ShortKey_index")

        index_found = arcpy.ListIndexes(inputGrip_ws+"\\DC_GripWC", "ShortKey_index")
        if not index_found:
            arcpy.AddIndex_management(inputGrip_ws+"\\DC_GripWC", "SHORTKEY", "ShortKey_index")

        arcpy.MakeFeatureLayer_management(fc, fc+"_lyr")
        if stName == "CA":
            gripFC = inputGrip_ws+"\\CA_GripWC"
            arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        if stName == "CT":
            gripFC = inputGrip_ws+"\\CT_GripWC"
            arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        if stName == "DC":
            gripFC = inputGrip_ws+"\\DC_GripWC"
            arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        if stName == "DE":
            gripFC = inputGrip_ws+"\\DE_GripWC"
            arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        if stName == "FL":
            gripFC = inputGrip_ws+"\\FL_GripWC"
            arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        if stName == "MA":
            gripFC = inputGrip_ws+"\\MA_GripWC"
            arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        if stName == "MD":
            gripFC = inputGrip_ws+"\\MD_GripWC"
            arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        if stName == "NJ":
            gripFC = inputGrip_ws+"\\NJ_GripWC"
            arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        if stName == "NY":
            gripFC = inputGrip_ws+"\\NY_GripWC"
            arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        if stName == "PA":
            gripFC = inputGrip_ws+"\\PA_GripWC"
            arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        if stName == "RI":
            gripFC = inputGrip_ws+"\\RI_GripWC"
            arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        if stName == "TX":
            gripFC = inputGrip_ws+"\\TX_GripWC"
            arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        if stName == "VA":
            gripFC = inputGrip_ws+"\\VA_GripWC"
            arcpy.MakeFeatureLayer_management(gripFC, gripFC+"_lyr")

        arcpy.AddJoin_management(fc+"_lyr", "SHORTKEY", gripFC+"_lyr", "SHORTKEY", "KEEP_COMMON")
        arcpy.CalculateField_management(fc+"_lyr", "PROV_CODE", "!" + os.path.basename(gripFC) + ".PROV_CODE!", "PYTHON_9.3")
##******* END SETTING PROV CODE ************

##******* DELETE TEMPORARY FEATURE CLASSES AND TABLES ***********
##print "Deleting temporary feature classes and tables..."
##
##TempfcList = ["Cable_XYLine", "Cables_with_GraphicSourceA", "Cables_with_GraphicSourceB",  "CompTab_Sorted", "CompTab_Sorted_for_CabID", "CompTab_Sorted_for_Size",
##              "CompTab_Sorted_for_Size3", "CompTab_toUse", "CompTab_toUse_Freq", "CompTab_toUseSmmry", "CompTab_toUseSorted",  "CompTab_toUseSorted_StatTab", "FDH_ForXY",
##              "FDHSplitter_ForXY", "FDT_ForXY", "VirtualMdu_ForXY", "CombinedPTSorted", "CombinedPTSorted_StatTab"]
##
##arcpy.env.workspace = input_ws
##for fc in TempfcList:
##    if arcpy.Exists(fc):
##        arcpy.Delete_management (fc)

print time.strftime("%H:%M:%S")
