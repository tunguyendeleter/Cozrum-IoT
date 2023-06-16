from requests.auth import HTTPDigestAuth
from datetime import datetime
import requests
import time
import json
#Variables
username = "admin"
password = "Cozrum@321"
url = "http://172.16.0.2/ISAPI/Event/notification/alertStream"
headers = {
    'Authorization': 'Bearer ¨XXXXX',
    'content-type': 'application/json',
}
url_states = "http://localhost:8123/api/states/"
sensor_name = "sensor.hikvision_door"

# Creating Sensor
# try:
#     timestamp = str(datetime.now())
#     data = json.dumps({'state': 'off', 'attributes': {'Time': timestamp}})
#     response = requests.post(url_states + sensor_name, headers=headers, data=data)
#     print("Creating Sensor on start script")
# except:
#     print("Creating Sensor Failed")


while True:
    try:
        stream = requests.get(url, stream=True, auth=HTTPDigestAuth(username, password))
        print("Status code: " , stream.status_code)
        for line in stream.iter_lines(chunk_size=1):
            str_line = line.decode("utf-8", "ignore")
            print(str_line)
            #Check for event
            if str_line.find('"subEventType":	25') != -1:
                result = str_line.find('eventState')
                print("Found event!")
                try:
                    timestamp = str(datetime.now())
                    data = json.dumps({'state': 'on', 'attributes': {'Time': timestamp}})
                    response = requests.post(url_states + sensor_name, headers=headers, data=data)
                    print("Door Open")
                    #put the sensor "on" for 5 seconds
                    time.sleep(5)
                    timestamp = str(datetime.now())
                    data = json.dumps({'state': 'off', 'attributes': {'Time': timestamp}})
                    # response = requests.post(url_states + sensor_name, headers=headers, data=data)
                    # print("Door Closed")
                #     continue
                except:
                    print("Updating sensor failed")
                    continue
        if stream.status_code == 401 or stream.status_code == 403:
            time.sleep(5)
    except (ValueError,requests.exceptions.ConnectionError,requests.exceptions.ChunkedEncodingError) as err:
        print("Connection Failed")
        continue