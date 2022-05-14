import os, sys
import arcpy

##arcpy.analysis.Clip("WorldUrbanCenterPnts_WGS84", "NA_MapCountryArea_Dissolved", out, None)


# buffer points
def BufferCenterPoints(centerPntsPath,centerPntsBuffPath, buffDistUnits):    
    arcpy.analysis.Buffer(centerPntsPath, centerPntsBuffPath, buffDistUnits, 'FULL', 'ROUND', 'NONE', None, 'GEODESIC')
    
    print("Buffer Complete" , arcpy.GetMessages(), sep='\n')

def ClipBuffers(centerPntsBuffPath,clipWithPath,centerPntsBuffClippedPath):
    arcpy.analysis.Clip(centerPntsBuffPath, clipWithPath, centerPntsBuffClippedPath, None)
    print("Clip Complete" , arcpy.GetMessages(), sep='\n')

def GetXYs(centerPntsBuffPath,randomPointsNamePrefix,outPath):
    big_list=[]
    big_list2=[]
    cnt=0
    with arcpy.da.SearchCursor(centerPntsBuffPath,'OBJECTID_1') as cursor:
        for row in cursor:
            cnt+=1
            print(row[0])    
            oid=str(row[0])
            
            mylayer = arcpy.SelectLayerByAttribute_management(centerPntsBuffPath, "NEW_SELECTION", "OBJECTID_1 = " + oid)
            # create random
            randomPointsName=f'{randomPointsNamePrefix}{oid}'
            #arcpy.management.CreateRandomPoints(gdb, randomPointsName, centerPntsBuffClipped , "#", RANDOMPNTCOUNT, "1 Kilometers", "POINT", 0)
            #arcpy.management.CreateRandomPoints(gdb, randomPointsName, centerPntsBuffPath , "#", RANDOMPNTCOUNT, "1 Kilometers", "POINT", 0)
            arcpy.management.CreateRandomPoints(outPath, randomPointsName, mylayer , "#", RANDOMPNTCOUNT, "1 Kilometers", "POINT", 0)
           
            
           
            
            xylist=[]
            xylist2=[]
            with arcpy.da.SearchCursor(outPath +'\\'+ randomPointsName,'SHAPE@XY') as cursor:
                for row in cursor:                
                    xylist.append(str(round(row[0][0],4))+','+str(round(row[0][1],4)))
                    xylist2.append(str(round(row[0][0],4))+','+str(round(row[0][1],4))+','+ 'Area'+str(cnt))
            
            big_list.append((";".join(xylist)) +'\n')  
            big_list2.append(("\n".join(xylist2)) +'\n')          
            
            if (cnt==3):
                break
    
    return big_list,big_list2
    
                
def WriteToFile(xylist1,xylist2):
    with open("outie.txt","w") as myfile: 
        myfile.writelines(xylist1)
    with open("outie2.txt","w") as myfile: 
        myfile.writelines(xylist2)

    
def main(): 
    
    # setup
    cntPntName=f'{region}_UrbanCenterPnts_WGS84'
    dissolvedArea=f'{region}_MapCountryArea_Dissolved'
    
    buffDistUnits  = f'{BUFFERDIST} {BUFFERUNITS}'
    centerPntsBuffName=f'{region}_UrbanCenterPnts_Buff_{BUFFERDIST}_{BUFFERUNITS}'
    centerPntsBuffClippedName=f'{region}_UrbanCenterPnts_Buff_{BUFFERDIST}_{BUFFERUNITS}_Clipped'  
    randomPointsNamePrefix=f'{region}_RandomPoints_{BUFFERDIST}_{BUFFERUNITS}_cnt_{RANDOMPNTCOUNT}_area_'
    
    #paths
    centerPntsPath = os.path.join(GDB,cntPntName)
    centerPntsBuffPath = os.path.join(GDB,centerPntsBuffName)
    clipWithPath = os.path.join(GDB,dissolvedArea)
    centerPntsBuffClippedPath = os.path.join(GDB,centerPntsBuffClippedName)
        
    #do the work
    BufferCenterPoints(centerPntsPath,centerPntsBuffPath, buffDistUnits)
    #ClipBuffers(centerPntsBuffPath,clipWithPath,centerPntsBuffClippedPath)
    xylist1,xylist2=GetXYs(centerPntsBuffPath,randomPointsNamePrefix,GDB)
    
    WriteToFile(xylist1,xylist2)

            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def adhoc2():
    
    stop_w_loc = arcpy.na.CalculateLocations("NA_RandomPoints_6_Miles_cnt_10_area_3", r"C:\Kish\Data\SMP\NA\NorthAmerica.gdb\Routing\Routing_ND", "5000 Meters",
    "Routing_Streets SHAPE;Routing_Streets_Override NONE;Routing_ND_Junctions NONE") 
    
    #"MATCH_TO_CLOSEST", "SourceID", "SourceOID", "PosAlong", "SideOfEdge", "SnapX", "SnapY", "DistanceToNetworkInMeters", None, None, "EXCLUDE", None, "Driving Time")
    
    '''
    search_criteria = "Routing_Streets SHAPE;Routing_Streets_Override NONE;Routing_ND_Junctions NONE"
    stop_w_loc = arcpy.nax.CalculateLocations(r'{GDB}/NA_RandomPoints_6_Miles_cnt_10_area_3',
                                              os.path.join(r'C:\Kish\Data\SMP\NA\NorthAmerica.gdb',"Routing", "Routing_ND"),
                                              search_tolerance="1000 Meters",search_criteria=search_criteria,match_type="MATCH_TO_CLOSEST")[0]
                                              
    '''
    
    print(stop_w_loc)

def adhoc():
    
    stop_w_loc = arcpy.na.CalculateLocations(r'C:\kish\data\PdsCfData.gdb\NA_RandomPoints_6_Miles_cnt_10_area_3',
                                             r"C:\Kish\Data\SMP\NA\NorthAmerica.gdb\Routing\Routing_ND", 
                                             "5000 Meters","Routing_Streets SHAPE;Routing_Streets_Override NONE;Routing_ND_Junctions NONE") 
    
    
    print("CalculateLocations Complete" , arcpy.GetMessages(), sep='\n')
    print(stop_w_loc)

if __name__ == '__main__':

    arcpy.env.overwriteOutput = True
    
    #set up all the args    
    GDB = r'C:\kish\data\PdsCfData.gdb'
    region='NA'
    BUFFERDIST='6'
    BUFFERUNITS = 'Miles'
    RANDOMPNTCOUNT=10
    IN_MEMORY = "in_memory"
    
    #main()
    
    adhoc()
    
print('---Done---')