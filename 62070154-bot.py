import json
import time
from urllib import response
import requests
requests.packages.urllib3.disable_warnings()

# --- RestConf --- #
api_url = "https://10.0.15.110/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback62070154"
api_url_set = "https://10.0.15.110/restconf/data/ietf-interfaces:interfaces/interface=Loopback62070154"
headers = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }
basicauth = ("admin", "cisco")
# --- RestConf --- #

# --- Webex API --- #
webex_accesstoken = 'ODBhYjk4MzItMjAxMi00YzgyLWIwOWItZWVjZGM2OTYxZDNjYTZlZDk3Y2UtZGQw_P0A1_9a8a306f-5965-407f-a4b3-63b85af39c54'
webex_roomid = 'Y2lzY29zcGFyazovL3VzL1JPT00vNjUwODkzMjAtY2QxOS0xMWVjLWE1NGUtNGQ2MmNhMWM4YmVl'
webex_baseurl = 'https://webexapis.com/v1/messages'
webex_headers = {
    'Authorization': 'Bearer {}'.format(webex_accesstoken),
    'Content-Type': 'application/json'
}
# --- Webex API --- #

def getOpeStatusLoopback():
    response = requests.get(api_url, auth=basicauth, headers=headers, verify=False)

    if response.status_code == 404: #not found interface
        return "Loopback62070154 - Operational status is down"
    else: #Response [200]
        response_json = response.json()
        return "Loopback62070154 - Operational status is " + response_json["ietf-interfaces:interface"]["oper-status"]

def setEnableLoopback():
    yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback62070154",
        "description": "My second RESTCONF loopback",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "192.168.1.1",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
        }
    }
    response = requests.put(api_url_set, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
    print(response)


def chatbot():
    prev_enable = False
    webex_getParams = {
        "roomId": webex_roomid,
        "max": 1
    }
    while True:
        response = requests.get(webex_baseurl, headers=webex_headers, params=webex_getParams).json()
        if len(response["items"]) > 0:
            last_msg = response["items"][0]["text"]
            print("Received message: " + last_msg)
            if last_msg == "62070154":
                webex_postParams = {
                    "roomId": webex_roomid,
                    "text": getOpeStatusLoopback()
                }
                status = webex_postParams["text"].split()[5]
                
                if prev_enable == True:
                    if (status == "down"):
                        webex_postParams = {
                            "roomId": webex_roomid,
                            "text": "Enable Loopback62070154 - Now the Operational status is still down"
                        }
                        response = requests.post(webex_baseurl, headers=webex_headers, json=webex_postParams)
                    if (status == "up"):
                        webex_postParams = {
                            "roomId": webex_roomid,
                            "text": "Enable Loopback62070154 - Now the Operational status is up again"
                        }
                        response = requests.post(webex_baseurl, headers=webex_headers, json=webex_postParams)
                else:
                    prev_enable = False
                    response = requests.post(webex_baseurl, headers=webex_headers, json=webex_postParams)
                    if status == "down":
                        setEnableLoopback()
                        prev_enable = True

                    
        time.sleep(1)

chatbot()