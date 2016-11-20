#!/usr/bin/env python

import urllib
import json
import os
import re

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
intent_name="string"
QR=['0','1','2','3','4','5','6']

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {
        }
    global city_names
    city_names=processlocation(req)
    global QR
    global intent_name
    intent_name=processIntentName(req)
    if "ChooseCity" in intent_name:        
        QR[0]="Sector in "+city_names
        QR[1]="Other City?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Property Type"
    elif "ChooseSector" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Other Sector?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Property Type"   
    elif "ChangeType" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Other Type?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Change Location"  
    elif "ChooseHotProperties" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Change Location"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Change City" 
    elif "ChoosePlotArea" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Other Area?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Change Location"
    elif "DefinePriceRange" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Other Range?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Change Location"
    city_names=processlocation(req)
    sector_names=processSector(req)
    property_type=processPropertyType(req)
    unit_property=processUnit(req)
    area_property=processArea(req)
    NoOfDays=processDate(req)
    DateUnit=processDateUnit(req)
    school=processSchool(req)
    malls=processMalls(req)
    transport=processTransport(req)
    security=processSecurity(req)
    airport=processAirport(req)
    fuel=processFuel(req)
    #minimum_value=processMinimum(req)
    maximum_value=processMaximum(req)
    latest=processLatestProperties(req)
    #longitude = '72.981148'
    #latitude = '33.642473'
    #if minimum_value > maximum_value:
    #    minimum_value,maximum_value=maximum_value,minimum_value
    #else:
    # minimum_value,maximum_value=minimum_value,maximum_value    
    baseurl = "https://fazendanatureza.com/bot/botarz.php?city_name="+city_names+"&sector_name="+sector_names+"&minPrice="+maximum_value+"&type="+property_type+"&LatestProperties="+latest+"&UnitArea="+area_property+"&Unit="+unit_property+"&school="+school+"&airport="+airport+"&transport="+transport+"&security="+security+"&shopping_mall="+malls+"&fuel="+fuel
    #+"&longitude"+longitude+"&latitude"+latitude
    result = urllib.urlopen(baseurl).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def processIntentName(req):
    result = req.get("result")
    parameters = result.get("metadata")
    intent = parameters.get("intentName")
    return intent

def processlocation(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("city")
    return city

def processSector(req):
    result = req.get("result")
    parameters = result.get("parameters")
    sector = parameters.get("Location")
    return sector

def processMinimum(req):
    result = req.get("result")
    parameters = result.get("parameters")
    minimum = parameters.get("number")
    return minimum

def processMaximum(req):
    result = req.get("result")
    parameters = result.get("parameters")
    maximum = parameters.get("number1")
    return maximum


def processPropertyType(req):
    result = req.get("result")
    parameters = result.get("parameters")
    propertyType = parameters.get("PropertyType")
    return propertyType

def processLatestProperties(req):
    result = req.get("result")
    parameters = result.get("parameters")
    latest = parameters.get("LatestProperties")
    return latest

def processUnit(req):
    result = req.get("result")
    parameters = result.get("parameters")
    unit = parameters.get("Unit")
    return unit

def processArea(req):
    result = req.get("result")
    parameters = result.get("parameters")
    area = parameters.get("AreaNumber")
    return area

def processDate(req):
    result = req.get("result")
    parameters = result.get("parameters")
    days = parameters.get("NoOfDays")
    return days

def processDateUnit(req):
    result = req.get("result")
    parameters = result.get("parameters")
    dayUnit = parameters.get("DayUnit")
    return dayUnit

def processSchool(req):
    result = req.get("result")
    parameters = result.get("parameters")
    school = parameters.get("school")
    return school

def processMalls(req):
    result = req.get("result")
    parameters = result.get("parameters")
    malls = parameters.get("malls")
    return malls

def processTransport(req):
    result = req.get("result")
    parameters = result.get("parameters")
    transport = parameters.get("transport")
    return transport

def processSecurity(req):
    result = req.get("result")
    parameters = result.get("parameters")
    security = parameters.get("security")
    return security

def processAirport(req):
    result = req.get("result")
    parameters = result.get("parameters")
    airport = parameters.get("airport")
    return airport

def processFuel(req):
    result = req.get("result")
    parameters = result.get("parameters")
    fuel = parameters.get("fuelstation")
    return fuel

message={
         "text": "Send Location",
         "quick_replies": [
           {
               
           "content_type": "location"
                
            }
        ]
           
    }

def makeWebhookResult(data):
    i=0
    length=len(data)
    row_id=['test','test1','test2']
    row_title=['test','test1','test2']
    row_location=['test','test1','test2']
    row_price=['test','test1','test2']
    while (i <length):
        row_id[i]=data[i]['p_id']
        row_title[i]=data[i]['title']
        row_location[i]=data[i]['address']
        row_price[i]=data[i]['address']
        i+=1
    
    # print(json.dumps(item, indent=4))
    speech = "This is the response from server."+ row_title[0]+""+intent_name
    print("Response:")
    print(speech) 

    return {
        "speech": speech,
        "displayText": speech,
        "data": {"facebook": message},
        # "contextOut": [],
        #"source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
