import arcpy
fc=r'D:\ElectricDataV\InputData\EDGIS_DEV.sde\EDGIS.CommonFeaturesDataset\EDGIS.MaintenancePlat'
fields= ['MAPNUMBER','MAPOFFICE']


lst = []
with arcpy.da.SearchCursor(fc,fields) as cursor:
    for row in cursor:
        lst.append(str(row[0])+'_'+str(row[1]))
        

import collections
print [x for x,y in collections.Counter(lst).items() if y>1]