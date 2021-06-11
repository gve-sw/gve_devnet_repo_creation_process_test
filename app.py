""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

# Import Section
from flask import Flask, render_template, request, url_for, redirect
from collections import defaultdict
import datetime
import requests
import json
from dotenv import load_dotenv
import os
#import merakiAPI
from dnacentersdk import api

# load all environment variables
load_dotenv()


# Global variables
app = Flask(__name__)


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/progress')
def ajax_index():
    global i
    i+=20
    print(i)
    return str(i)

# Methods
# Returns location and time of accessing device
def getSystemTimeAndLocation():
    # request user ip
    userIPRequest = requests.get('https://get.geojs.io/v1/ip.json')
    userIP = userIPRequest.json()['ip']

    # request geo information based on ip
    geoRequestURL = 'https://get.geojs.io/v1/ip/geo/' + userIP + '.json'
    geoRequest = requests.get(geoRequestURL)
    geoData = geoRequest.json()
    
    #create info string
    location = geoData['country']
    timezone = geoData['timezone']
    current_time=datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    timeAndLocation = "System Information: {}, {} (Timezone: {})".format(location, current_time, timezone)
    
    return timeAndLocation

#Read data from json file
def getJson(filepath):
	with open(filepath, 'r') as f:
		json_content = json.loads(f.read())
		f.close()

	return json_content

#Write data to json file
def writeJson(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f)
    f.close()


##Routes
#Instructions

#Widget
@app.route('/widget', methods=["GET", "POST"])
def webex():
    try:
        #Page without error message and defined header links
        return render_template('widget.html', hiddenLinks=False, timeAndLocation=getSystemTimeAndLocation(), accessToken=os.environ.get('WEBEX_TEAMS_ACCESS_TOKEN'))
    except Exception as e:
        print(e)
        #OR the following to show error message
        return render_template('widget.html', error=False, errormessage="CUSTOMIZE: Add custom message here.", errorcode=e, timeAndLocation=getSystemTimeAndLocation())

#Index
@app.route('/')
def index():
    try:
        #Page without error message and defined header links 
        return render_template('instructions.html', hiddenLinks=False, timeAndLocation=getSystemTimeAndLocation())
    except Exception as e: 
        print(e)  
        #OR the following to show error message 
        return render_template('instructions.html', error=False, errormessage="CUSTOMIZE: Add custom message here.", errorcode=e, timeAndLocation=getSystemTimeAndLocation())


#Settings
@app.route('/settings',methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        try:
            #Page without error message and defined header links
            return render_template('settings.html', hiddenLinks=False, timeAndLocation=getSystemTimeAndLocation())
        except Exception as e:
            print(e)
            #OR the following to show error message
            return render_template('settings.html', error=False, errormessage="CUSTOMIZE: Add custom message here.", errorcode=e, timeAndLocation=getSystemTimeAndLocation())
    if request.method == 'POST':
        value1 =  request.form.get("value1")
        print('value1=',value1)
        return render_template('settings.html', error=False, errormessage="Saved!!!!", timeAndLocation=getSystemTimeAndLocation())


#Login
@app.route('/login')
def login():
    try:
        #Page without error message and defined header links 
        return render_template('login.html', hiddenLinks=True, timeAndLocation=getSystemTimeAndLocation())
    except Exception as e: 
        print(e)  
        #OR the following to show error message 
        return render_template('login.html', error=False, errormessage="CUSTOMIZE: Add custom message here.", errorcode=e, timeAndLocation=getSystemTimeAndLocation())

#collage
@app.route('/collage')
def collage():
    try:
        #Page without error message and defined header links 
        return render_template('collage.html', hiddenLinks=False, timeAndLocation=getSystemTimeAndLocation())
    except Exception as e: 
        print(e)  
        #OR the following to show error message 
        return render_template('collage.html', error=False, errormessage="CUSTOMIZE: Add custom message here.", errorcode=e, timeAndLocation=getSystemTimeAndLocation())

#Table with menu
@app.route('/tablemenu', methods=['GET', 'POST'])
def tablemenu():
    try:
        
        #Retrieve devices list from json file
        devices = getJson("devices.json")
        deviceToEdit = {}
        
        #Show table with all devices
        if request.method == 'GET':
            return render_template('tablemenu.html', hiddenLinks=False, devices = devices, timeAndLocation=getSystemTimeAndLocation())


        #Find device to edit in devices list and render edit page (include device info) 
        if request.method == 'POST':
            
            deviceId =  request.form.get("editEntry")
            
            for device in devices:
                if device['id'] == deviceId:
                    deviceToEdit = device
            
            return render_template('editTableEntry.html', hiddenLinks=False,  device = deviceToEdit, timeAndLocation=getSystemTimeAndLocation()) 

    except Exception as e: 
        print(e)  
        #OR the following to show error message 
        return render_template('tablemenu.html', error=True, devices = devices, errormessage="CUSTOMIZE: Add custom message here.", errorcode=e, timeAndLocation=getSystemTimeAndLocation())

#Edit page for table entry
@app.route('/editTableEntry', methods=['GET', 'POST'])
def editTableEntry():
    try:
        if request.method == 'POST':
            
            #Retrieve devices list from json file
            devices = getJson("devices.json")

            #Submitted form values:
            deviceId = request.form.get("saveEntry")
            deviceName = request.form.get("deviceName")
            deviceCoverage = request.form.get("radio-inline")
            deviceSoftwareType = request.form.get("deviceSoftwareType")
            deviceSoftwareVersion = request.form.get("deviceSoftwareVersion")
            deviceRole = request.form.get("deviceRole")
       
            #Find device to edit in devices list and change the values according to the submitted user input
            for device in devices:
                if device['id'] == deviceId:
                    device['name'] = deviceName
                    device['coverage'] = deviceCoverage
                    device['softwareType'] = deviceSoftwareType
                    device['softwareVersion'] = deviceSoftwareVersion
                    device['role'] = deviceRole

            #Write updated devices info to json file
            writeJson("devices.json", devices)

            #Redirect to table view
            return redirect(url_for('tablemenu'))

    except Exception as e: 
        print(e)  
        #OR the following to show error message 
        return render_template('editTableEntry.html', error=True, errormessage="CUSTOMIZE: Add custom message here.", errorcode=e, timeAndLocation=getSystemTimeAndLocation())

#Table
@app.route('/table')
def table():
    try:
        #Page without error message and defined header links 
        return render_template('table.html', hiddenLinks=False, timeAndLocation=getSystemTimeAndLocation())
    except Exception as e: 
        print(e)  
        #OR the following to show error message 
        return render_template('table.html', error=False, errormessage="CUSTOMIZE: Add custom message here.", errorcode=e, timeAndLocation=getSystemTimeAndLocation())
        
# https://www.chartjs.org/docs/latest/charts/line.html
@app.route('/line')
def line():
    return render_template('line.html')


# https://www.chartjs.org/docs/latest/charts/bar.html
@app.route('/bar')
def bar():
    return render_template('bar.html') 

# https://www.chartjs.org/docs/latest/charts/doughnut.html
@app.route('/pie')
def pie():
    return render_template('pie.html') 

#Columnpage
@app.route('/columnpage')
def columnpage():
    try:
        #Organization and networkstructure
        dropdown_content = [{'networks': [ {'networkid': 'L_xxxx1','networkname': 'GVE DevNet Network 1'},{'networkid': 'L_xxx2','networkname': 'GVE DevNet Network 2'}],'orgaid': 'xxxx1', 'organame': 'GVE DevNet'}, {'networks': [{'networkid': 'N_xxxx3', 'networkname': 'Cisco Network 1'}, {'networkid': 'N_xxxx4', 'networkname': 'Cisco Network 2'}], 'orgaid': 'xxxx2', 'organame': 'Cisco'}]
        #currently selected elements in dropdown
        selected_elements = {} #{'organization': ORGANIZATION, 'network_id': network_id}
        #Page without error message and defined header links 
        return render_template('columnpage.html', hiddenLinks=False, dropdown_content = dropdown_content, selected_elements = selected_elements, timeAndLocation=getSystemTimeAndLocation(), error=True, errormessage="CUSTOMIZE: Add custom message here.", errorcode=200)
    except Exception as e: 
        print(e)  
        #OR the following to show error message 
        return render_template('columnpage.html', hiddenLinks=False, dropdown_content = dropdown_content, selected_elements = selected_elements, error=True, errormessage="CUSTOMIZE: Add custom message here.", errorcode=e, timeAndLocation=getSystemTimeAndLocation())

#MerakiAPI
@app.route('/meraki')
def meraki():
    try:
        merakiOrganizations = {}
        #Add the following lines and "import merakiAPI" to execute the Meraki API example
        #merakiOrganizations = merakiAPI.getOrganizations()
        #for orga in merakiOrganizations:
        #    merakiNetworks = merakiAPI.getNetworks(orga['id'])
        #    orga.update([("networks", merakiNetworks)])

        return render_template('merakiAPI.html', orgaStructure = merakiOrganizations, hiddenLinks=False, timeAndLocation=getSystemTimeAndLocation())
    except Exception as e: 
        print(e)  
        return render_template('merakiAPI.html', hiddenLinks=False, error=True, errormessage="", errorcode=e, timeAndLocation=getSystemTimeAndLocation())
      
@app.route('/dnac')
def dnac():
        # include ip address of dna center instance
        dnac = api.DNACenterAPI(
                        base_url='',
                        version='2.1.2',
                        verify=False,
                        single_request_timeout=99999)
        counters = {}
        scores = {}

        counters["wlc"] = 0
        counters["switches_hubs"] = 0
        counters["router"] = 0
        counters["ap"] = 0

        device_list  = []
        health_report_list = []
        client_list = []
        client_count = {}
        reachable_count = 0
        unreachable_count = 0

        total_devices = dnac.devices.get_device_count()
        all_devices_info = []
        all_offline_devices = []
        offset = 1
        limit = 500

        while offset < total_devices["response"]:
            devices = dnac.devices.get_device_list(offset=offset,limit=limit)
            all_devices_info += devices["response"]
            offset += 500

        for device in all_devices_info:
            temp = {}
            # Hostname,Location,Status,Uptime,Serial#,Model#,OS
            temp["hostname"] = device.hostname
            temp["location"] = device.location
            temp["status"] = device.reachabilityStatus
            temp["uptime"] = str(device.upTime).replace(",", " ")
            temp["serial"] = device.serialNumber
            temp["type"] = device.type
            temp["family"] = device.family
            temp["os"] = device.softwareVersion

            if device.family == "Wireless Controller":
                counters["wlc"] = counters["wlc"] + 1

            if device.family == "Switches and Hubs":
                counters["switches_hubs"] = counters["switches_hubs"] + 1
            if device.family == "Routers":
                counters["router"] = counters["router"] + 1
            if device.family == "Access Points":
                counters["ap"] = counters["ap"] + 1

            if device.reachabilityStatus == "Reachable":
                reachable_count = reachable_count + 1
            else:
                all_offline_devices.append(temp)
                unreachable_count = unreachable_count + 1

            device_list.append(temp)
        
        health = dnac.topology.get_overall_network_health()

        for report in health["healthDistirubution"]:
            temp =  {}

            if report["category"] == "Access":
                scores["access"] = report.healthScore
            
            if report["category"] == "Distribution":
                scores["distribution"] = report.healthScore

            if report["category"] == "Router":
                scores["router"] = report.healthScore
            
            if report["category"] == "WLC":
                scores["wlc"] = report.healthScore
            
            if report["category"] == "AP":
                scores["ap"] = report.healthScore

            temp["category"] = report.category
            
            if temp["category"] == "Distribution":
                temp["category"] = "Distribution/Core"

                
            temp["totalCount"] = report.totalCount
            temp["healthScore"] = report.healthScore
            temp["goodPercentage"] = report.goodPercentage
            temp["badPercentage"] = report.badPercentage
            temp["fairPercentage"] = report.fairPercentage
            temp["unmonPercentage"] = report.unmonPercentage
            temp["goodCount"] = report.goodCount
            temp["badCount"] = report.badCount
            temp["fairCount"] = report.fairCount
            temp["unmonCount"] = report.unmonCount

            health_report_list.append(temp)

        clients = dnac.clients.get_overall_client_health()
        client_reports = clients.response[0]["scoreDetail"]

        for report in client_reports:
            if report["scoreCategory"]["value"] == "ALL":
                print("All client count " + str(report["clientUniqueCount"]))
                client_count["all"] = report["clientUniqueCount"]

            if report["scoreCategory"]["value"] == "WIRED":
                print("Wired client count " + str(report["clientUniqueCount"]))
                client_count["wired"] = report["clientUniqueCount"]

            if report["scoreCategory"]["value"] == "WIRELESS":
                print("Wireless client count " + str(report["clientUniqueCount"]))
                client_count["wireless"] = report["clientUniqueCount"]


        # Retrieve ALL Network Sites (Buildings & Geo-Areas)
        site_healthList = dnac.sites.get_site_health()

        site_health_labels = []
        site_health_scores = []
        site_client_count = []
        application_site_count = []
        application_site_labels = []

        issues_site_count = []
        issues_site_labels = []
        issues_site_details = []

        for site_health in site_healthList["response"]:
            application_site = {}
            issue_temp = {}
            total_issues = 0

            application_site["name"]= site_health["siteName"]
            application_site["id"]= site_health["siteId"]
            application_site["appHealth"]= site_health["applicationHealth"]
            application_site["totalCount"]= site_health["applicationTotalCount"]


            issues = dnac.issues.issues(site_id=site_health["siteId"])

            for issue in issues["response"]:
                if issue["priority"] == "P1":
                    issue_temp["name"] = issue["name"]
                    issue_temp["mac"] = issue["clientMac"]
                    issue_temp["deviceRole"] = issue["deviceRole"]
                    issue_temp["status"] = issue["status"]
                    issue_temp["occurence"] = issue["last_occurence_time"]
                    total_issues += 1

                if issue["priority"] == "P2":
                    total_issues += 1

            site_health_labels.append(site_health["siteName"])
            application_site_labels.append(site_health["siteName"])
            issues_site_labels.append(site_health["siteName"])
            issues_site_details.append(issue_temp)

            site_health_scores.append(site_health["networkHealthAverage"])
            issues_site_count.append(total_issues)

            if site_health["applicationTotalCount"] == None:
                application_site_count.append(0)
            else:
                application_site_count.append(site_health["applicationTotalCount"])

            if site_health["numberOfWirelessClients"] == None:
                site_client_count.append(0)
            else:
                site_client_count.append(site_health["numberOfWirelessClients"])

        
        #issues = dnac.issues.issues()
        #print(issues)




        return render_template('dnac.html',devices=device_list,
                                        counters=counters,
                                        reports=health_report_list,
                                        scores=scores,
                                        client_count=client_count,
                                        reachable_count=reachable_count,
                                        unreachable_count=unreachable_count,
                                        site_health_labels=site_health_labels,
                                        site_health_scores=site_health_scores,
                                        site_client_count=site_client_count,
                                        application_site_count=application_site_count,
                                        application_site_labels=application_site_labels,
                                        all_offline_devices=all_offline_devices,
                                        issues_site_count = issues_site_count,
                                        issues_site_labels = issues_site_labels,
                                        issues_site_details = issues_site_details,
                                        region="Americas")

@app.route('/observables', methods=['GET', 'POST'])
def observables():
    if request.method == 'GET':
        try:
            # Page without error message and defined header links
            return render_template('observables.html', hiddenLinks=False, timeAndLocation=getSystemTimeAndLocation(),
                                   title='SecureX Observables')
        except Exception as e:
            print(e)
            # OR the following to show error message
            return render_template('observables.html', error=False, errormessage="CUSTOMIZE: Add custom message here.",
                                   errorcode=e, timeAndLocation=getSystemTimeAndLocation(), title='SecureX Observables')
    elif request.method == 'POST':
        # Login to SecureX and get access token
        url = "https://visibility.apjc.amp.cisco.com/iroh/oauth2/token"
        payload = 'grant_type=client_credentials'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload, auth=(os.getenv('SECUREX_CLIENT_ID'),
                                                                                      os.getenv('SECUREX_PASSWORD')))
        token = response.json()['access_token']

        # Fetch observables with SecureX Inspect API
        payload = {
            "content": request.form['string_input']
        }
        url = "https://visibility.apjc.amp.cisco.com/iroh/iroh-inspect/inspect"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        unsorted = response.json()
        items = defaultdict(list)
        for element in unsorted:
            key = element['type']
            value = element['value']
            items[key].append(value)
        # print(items)

        return render_template('observables.html', hiddenLinks=False, timeAndLocation=getSystemTimeAndLocation(),
                               observables=items.items(), title='SecureX Observables')
      
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)