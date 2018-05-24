#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


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
    print ("started processing")
    if req.get("result").get("action") != "get_purchorg":
        return {}
    baseurl = "http://in-blr-slog.corp.capgemini.com:50000/sap/opu/odata/SAP/ZCB_PO1_SRV/po_headerSet?$format=json"
    ores = requests.get(baseurl, auth=HTTPBasicAuth('TRAIN6-A2', 'Welcome@123'))
    #yql_query = makeYqlQuery(req)
    #print ("yql query created")
    #if yql_query is None:
    #    print("yqlquery is empty")
    #    return {}
    #yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
    #print(yql_url)

    #result = urllib.urlopen(yql_url).read()
    #print("yql result: ")
    #print(result)
    
    all_data = ores.json()
    jsondata_dumps = json.dumps(all_data)
    
    data = json.loads(jsondata_dumps)
    res = makeWebhookResult(data)
    return res





def makeWebhookResult(data):
# get purchase group    
    result = req.get("result")
    parameters = result.get("parameters")   
    prgrp = parameters.get("purchgrp")
    ponumber = parameters.get("number")
    if req.get("result").get("action") == "get_purchorg":
       if prgrp == "purchgrp":
        
            for line in data:
                if ponumber == jsondata[line]:
                    purchgrp = jsondata['d']['results'][line]['PurGroup']
                    speech = "The purchase group of" + ponumber + " is" + purchgrp
                    print("Response:")
                    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {"slack": slack_message, "facebook": facebook_message},
        # "contextOut": [],
        "source": "Ada"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')