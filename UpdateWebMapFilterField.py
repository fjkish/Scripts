#!/usr/bin/env python
# Requires Python 2.7+
import urllib
import json
import argparse
import re   
import time


# Helper functions for decoding the unicode values in the webmap json.
def __decodeDict__(dct):
    newdict = {}
    for k, v in dct.iteritems():
        k = __safeValue__(k)
        v = __safeValue__(v)
        newdict[k] = v
    return newdict

def __safeValue__(inVal):
    outVal = inVal
    if isinstance(inVal, unicode):
        outVal = inVal.encode('utf-8')
    elif isinstance(inVal, list):
        outVal = __decode_list__(inVal)
    return outVal

def __decode_list__(lst):
    newList = []
    for i in lst:
        i = __safeValue__(i)
        newList.append(i)
    return newList

class AGOPostError(Exception):
    def __init__(self, webmap, msg):
        print 'ok'
        self.webmap = webmap
        self.msg = msg

def generateToken(username, password, portalUrl):
    '''Retrieves a token to be used with API requests.'''
    parameters = urllib.urlencode({'username' : username,
                                   'password' : password,
                                   'client' : 'referer',
                                   'referer': portalUrl,
                                   'expiration': 60,
                                   'f' : 'json'})
    response = urllib.urlopen(portalUrl + '/sharing/rest/generateToken?',
                              parameters).read()
    try:
        jsonResponse = json.loads(response)
        if 'token' in jsonResponse:
            return jsonResponse['token']
        elif 'error' in jsonResponse:
            print jsonResponse['error']['message']
            for detail in jsonResponse['error']['details']:
                print detail
    except ValueError, e:
        print 'An unspecified error occurred.'
        print e

def updateWebmapService(webmapId,token, portalUrl):    
    try:
        
        params = urllib.urlencode({'token' : token,'f' : 'json'})        
        # Get the item data.
        reqUrl = (portalUrl + '/sharing/content/items/' + webmapId + '/data?' + params)
        itemDataReq = urllib.urlopen(reqUrl).read()
        itemString = str(itemDataReq)
        
        reToFind ='\"definitionExpression\":\"VehicleSpe = \'[0-9]{2}/[0-9]{2}/[0-9]{4}\'\"'        
        
        reFound = bool(re.search(reToFind, itemString))        
        if (reFound):            
            
            ##today's date ... this probably is not correct for a true date field
            dateReplace = time.strftime('%m/%d/%Y')    
            ## match to above reToFind
            replaced = re.sub(reToFind,'\"definitionExpression\":\"VehicleSpe = \''+dateReplace+'\'\"',itemString )                
            
            itemInfoReq = urllib.urlopen(portalUrl +'/sharing/content/items/' +webmapId + '?' + params)
            itemInfo = json.loads(itemInfoReq.read(),object_hook=__decodeDict__)            
            
            ## do the update
            print 'Updating ' + itemInfo['title']                        
            if(itemInfo['ownerFolder'] is not None):
                modRequest = urllib.urlopen(portalUrl +
                                        '/sharing/content/users/' +
                                        itemInfo['owner'] +
                                        '/' + itemInfo['ownerFolder'] +
                                        '/items/' + webmapId +
                                        '/update?' + params ,
                                        urllib.urlencode(
                                            {'text' : replaced}
                                        ))
            else:
                
                modRequest = urllib.urlopen(portalUrl +
                                        '/sharing/content/users/' +
                                        itemInfo['owner'] +
                                        '/items/' + webmapId +
                                        '/update?' + params ,
                                        urllib.urlencode(
                                            {'text' : replaced}
                                        ))
                                        
            # Evaluate the results to make sure it happened
            modResponse = json.loads(modRequest.read())
            if modResponse.has_key('error'):
                raise AGOPostError(webmapId, modResponse['error']['message'])
            else:
                print 'Successfully updated'  
            
            
        else:
            print 'Did not find ' + reToFind
            
       
    except ValueError as e:
        print 'Error - no web map specified'
    except AGOPostError as e:
        print e.webmap
        print 'Error updating web map ' + e.webmap + ': ' + e.msg


# Run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()    
    parser.add_argument('password', help='password')    
    # Read the command line arguments.
    args = parser.parse_args()
    portal = "https://ps-cc.maps.arcgis.com"
    username = 'fkish_PS_CC'
    password = args.password
    # Get a token for the source Portal for ArcGIS.
    token = generateToken(username=username, password=password,portalUrl=portal)
    #Update the webmap json
    updateWebmapService('5fd018a7fd11469f8ed0df927d542829',token=token,portalUrl=portal)
    