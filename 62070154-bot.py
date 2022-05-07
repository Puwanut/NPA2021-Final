import json
import time
import requests
requests.packages.urllib3.disable_warnings()

# --- RestConf --- #
api_url = "https://10.0.15.110/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback62070154"
headers = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }
basicauth = ("admin", "cisco")
# --- RestConf --- #

# --- Webex API --- #
webex_accesstoken = 'ZDQ4YzhlN2UtNjhmYi00NjA2LTk3NTQtNGQyNGU5NmFjZTVkMTE4YzQ1NWYtMmY3_P0A1_9a8a306f-5965-407f-a4b3-63b85af39c54'
webex_roomid = 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vY2U2ZTk4YTAtY2RkNy0xMWVjLTgxZTktNGYyNmEzZmYyMGZi'
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

def chatbot():
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
                response = requests.post(webex_baseurl, headers=webex_headers, json=webex_postParams)
        time.sleep(1)

chatbot()