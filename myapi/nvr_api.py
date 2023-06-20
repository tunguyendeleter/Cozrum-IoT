import threading
from bson.objectid import ObjectId
from requests.auth import HTTPDigestAuth
from fastapi import FastAPI, Path
import datetime
import requests
import time
from pymongo import MongoClient, DESCENDING
import os
from pydantic import BaseModel
import xml.etree.ElementTree as ET
import json


class Item(BaseModel):
    ip_address : str
    name : str
    password : str
    database : str
    collection : str
    location : str

class NVR_init:
    def __init__(self, ip_address, name, password, db, collection, location):
        self.ip_address = ip_address
        self.name = name
        self.password = password
        self.myclient = MongoClient("mongodb://localhost:27017")
        self.db = self.myclient[db]
        self.collection = self.db[collection]
        self.location = location
    def add_one_db(self, my_dict):
        responsed = self.collection.find(my_dict)
        count = 0
        for i in responsed:
            count += 1
        if count == 0:
            self.collection.insert_one(my_dict)
    def print_one_db(self, my_dict):
        responsed = list(self.collection.find(my_dict))
        for i in responsed:
            i["_id"] = str(i["_id"])
        print(responsed)
    def thread_get_log(self, cam_name, delay):
        thread = threading.Thread(target=self.get_log, args=(cam_name, delay,))
        thread.start()
    def get_log(self, cam_name, delay):
        while True:
            current_datetime = datetime.datetime.now()
            current_datetime = current_datetime - datetime.timedelta(seconds=delay)
            year = str(current_datetime.year)
            month = str(current_datetime.month)
            day = str(current_datetime.day)
            hour = str(current_datetime.hour)
            minute = str(current_datetime.minute)
            second = str(current_datetime.second)
            start_time = year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "Z"
            end_time = year + "-" + month + "-" + day + "T23:59:59Z"
            print(start_time)
            print(end_time)
            command = '''
                <?xml version='1.0' encoding='utf-8'?>
            <CMSearchDescription version='1.0' xmlns='http://www.hikvision.com/ver20/XMLSchema'>
                <searchID>484a3530-3939-3239-3038-240f9b2d60ab</searchID>
                <timeSpanList>
                    <timeSpan>
                        <startTime>''' + start_time + '''</startTime>
                        <endTime> ''' + end_time + '''</endTime>
                    </timeSpan>
                </timeSpanList>
                <metaId>log.hikvision.com/Alarm</metaId>
                <searchResultPostion>0</searchResultPostion>
                <maxResults>6</maxResults>
            </CMSearchDescription>
                '''
            print(start_time)
            print(end_time)
            url = f"http://{self.ip_address}/ISAPI/ContentMgmt/logSearch"
            response=requests.post(url, command, auth=HTTPDigestAuth(self.name, self.password)).text
            if response:
                # print(type(response))
                print("status ****************************************************************** :   ",response)
                root = ET.fromstring(response)
                # Find the playbackURI element
                StartDateTime = root.findall(".//{http://www.hikvision.com/ver20/XMLSchema}StartDateTime")
                camId = root.findall(".//{http://www.hikvision.com/ver20/XMLSchema}localID")
                metaId = root.findall(".//{http://www.hikvision.com/ver20/XMLSchema}metaId")

                # Extract the playback URL
                times = [start.text for start in StartDateTime]
                cams = [end.text for end in camId]
                detects = [end.text for end in metaId]

                for i in range(0, len(times)):
                    if cams[i] == "D1":
                        cams[i] = cam_name[i]
                    elif cams[i] == "D2":
                        cams[i] = cam_name[i]
                    elif cams[i] == "D3":
                        cams[i] = cam_name[i]
                    elif cams[i] == "D4":
                        cams[i] = cam_name[i]
                    elif cams[i] == "D5":
                        cams[i] = cam_name[i]
                    elif cams[i] == "D6":
                        cams[i] = cam_name[i]
                    myquery = {"Alarm": detects[i], "Time": times[i], "Cam": cams[i]}
                    print(myquery)
                    mydoc = self.collection.find(myquery)
                    cnt = 0
                    for x in mydoc:
                        cnt += 1
                    if cnt == 0:
                        print("not exit")
                        self.collection.insert_one(myquery)
                    else:
                        print("exit")
                time.sleep(2)

cam_name = ["Cong", "Tret", "tang 3", "tang 4", "tang 5", "tang 6"]
file_path = os.path.join(os.path.dirname(__file__), "database.json")
settings = json.load(open(file_path, "r"))
a = NVR_init("172.16.0.2", "admin", "Cozrum@321", settings["database"], settings["collection"], "location")
app = FastAPI()

@app.get("/")
def index():
    return "welcome to my api"

@app.post("/set-database")
def modify_database(body : Item):
    global a
    file_path = os.path.join(os.path.dirname(__file__), "database.json")
    settings = {
        "ip_address" : body.ip_address,
        "name" : body.name,
        "password" : body.password,
        "database" : body.database,
        "collection" : body.collection,
        "location" : body.location
    }
    json.dump(settings, open(file_path, "w"))
    file_path = os.path.join(os.path.dirname(__file__), "database.json")
    settings = json.load(open(file_path, "r"))
    a = NVR_init(settings["ip_address"], settings["name"], settings["password"], settings["database"], settings["collection"], settings["location"])

@app.get("/download-playback/{ID}")
def download_playback_by_mongoid(ID : str):
    playback_info = get_playback_by_mongoid(ID)
    url_playback = playback_info[0]["playbackURI"]
    '''
    Down load playback by playback URL
    :param url_playback:
    :return:
    '''
    payload = f'''
        <downloadRequest version=\"1.0\" xmlns=\"http://www.isapi.org/ver20/XMLSchema\">\r\n
        <playbackURI>{url_playback}\r\n</playbackURI>\r\n
        </downloadRequest'''
    headers = {
        'Content-Type': 'application/xml'
    }
    url_api_download_video = f"http://{a.ip_address}/ISAPI/ContentMgmt/download"
    response_video = requests.request("POST", url_api_download_video, headers=headers, data=payload, auth=HTTPDigestAuth(a.name, a.password))
    if response_video.status_code == 200:
        start_idx = url_playback.find("tracks/")
        substring = url_playback[start_idx + len("tracks/"):]
        end_idx = substring.find("/")
        cam_trackid = substring[:end_idx]

        start_idx = url_playback.find("starttime=")
        substring = url_playback[start_idx + len("starttime="):]
        end_idx = substring.find("&")
        start_time = substring[:end_idx]

        start_idx = url_playback.find("endtime=")
        substring = url_playback[start_idx + len("endtime="):]
        end_idx = substring.find("&")
        end_time = substring[:end_idx]

        name_video = start_time + "_" + end_time + '_' + cam_trackid
        create_path(response_video, name_video)
        return "Download playback successfully"

@app.get("/search-playback/{start_time}/{end_time}/{max_result}/{search_position}")
def search_playback_by_time(cam_trackid : str, start_time : str, end_time : str, max_result : str, search_position : str):
    '''
    log the playback URL information from start time to stop time
    :param cam_trackid:
    :param start_time:
    :param end_time:
    :param max_result:
    :param search_position:
    :return:
    '''
    command = f'''
    <?xml version: \"1.0\" encoding=\"utf-8\"?>
    <CMSearchDescription>
        <searchID>484a3530-0000-0000-0000-240f9b2d60ab</searchID>
        <trackList>
            <trackID>{cam_trackid}</trackID>
        </trackList>
        <timeSpanList>
            <timeSpan>
                <startTime>{start_time}</startTime>
                <endTime>{end_time}</endTime>
            </timeSpan>
        </timeSpanList>
        <maxResults>{max_result}</maxResults>
        <searchResultPostion>{search_position}</searchResultPostion>
        <metadataList>
            <metadataDescriptor>//recordType.meta.std-cgi.com</metadataDescriptor>
        </metadataList>
    </CMSearchDescription>
    '''
    url = f"http://{a.ip_address}/ISAPI/ContentMgmt/Search"
    response = requests.post(url, command, auth=HTTPDigestAuth(a.name, a.password)).text
    print(response)
    import xml.etree.ElementTree as ET

    # Parse the XML string
    root = ET.fromstring(response)

    # Find the playbackURI element
    starttimes = root.findall(".//{http://www.hikvision.com/ver20/XMLSchema}startTime")
    endtimes = root.findall(".//{http://www.hikvision.com/ver20/XMLSchema}endTime")
    playback_uris = root.findall(".//{http://www.hikvision.com/ver20/XMLSchema}playbackURI")

    # Extract the playback URL
    urls = [uri.text for uri in playback_uris]
    starts = [start.text for start in starttimes]
    ends = [end.text for end in endtimes]

    # Print the extracted URLs
    list = []
    for i in range(len(playback_uris)):
        list.append({"playbackURI" : urls[i], "startTime" : starts[i], "endTime" : ends[i]})
    print(list)
    return list


@app.get("/search-log/{timestart}/{timeend}")
def search_log_by_time(timestart : str, timeend : str):
    '''
    log data from database by time start and time end
    :param timestart:
    :param timeend:
    :return:
    '''
    js_list = []
    list = a.collection.find({"Time": {"$gte": timestart, "$lte": timeend}})
    for x in list:
        del x["_id"]
        js_list.append(x)
    return js_list


@app.get("/search-log-page/{max_result}")
def log_db_by_page(max_result : int):
    '''
    log information from database by page number
    page size = 20
    '''
    # Query for the 20 newest documents
    documents = a.collection.find().sort("_id", DESCENDING).limit(max_result)
    list = []
    for x in documents:
        del x["_id"]
        list.append(x)
    list.reverse()

    # Iterate over the retrieved documents
    return list


@app.get("/search-log-id/{ID}")
def log_db_by_mongoid(id_cam):
    '''
    log information from database by ID
    :param id_cam:
    :return:
    '''
    object_id = ObjectId(id_cam)
    i = a.collection.find_one(object_id)
    print(i)
    return i


def create_path(response_video ,name_video):
    '''
    create new folder to store videos or playback
    :param response_video:
    :param name_video:
    :return:
    '''
    now = datetime.datetime.now()
    # dd/mm/YY
    dt_string = now.strftime("%Y/%m/%d")
    path = "nam " + dt_string[0:4] + "/thang " + dt_string[5:7] + "/ngay " + dt_string[8:10]
    if os.path.exists("nam " + dt_string[0:4]) == False:
        os.makedirs("nam " + dt_string[0:4])
    if os.path.exists("nam " + dt_string[0:4] + "/thang " + dt_string[5:7]) == False:
        os.makedirs("nam " + dt_string[0:4] + "/thang " + dt_string[5:7])
    if os.path.exists(path) == False:
        os.makedirs(path)

    if os.path.exists(path + f'/{name_video}.mp4') == False:
        with open(path + f'/{name_video}.mp4', 'wb') as f:
            f.write(response_video.content)
        return "Record data saved to file."
    else:
        return "file already exist"

@app.get("/get_playback_by_ID_mongo/{ID}")
def get_playback_by_mongoid(ID : str):
    object_id = ObjectId(ID)
    track = a.collection.find_one(object_id)
    print(track)
    i = len(track["Alarm"]) - 1
    while track["Alarm"][i] != "/":
        i -= 1
    trackid = track["Alarm"][i+1:]
    if len(trackid) == 1:
        trackid += "01"
    else:
        trackid += "1"
    # print(track["Time"][0:11] + "23:59:59Z")
    return search_playback_by_time(trackid, track["Time"], track["Time"][0:11] + "23:59:59Z", 1, 0)


# if __name__ == "__main__":
    # download_playback("647e94314685ab6a1446b33a")
    # log_db_by_id("646dc272bff39cb3a4b2f827")
    # search_playback_by_time("101", "2023-05-24T14:52:37Z", "2023-05-24T23:01:55Z", 5, 0)
    # log_db_by_page(5)
    # a.thread_get_log(cam_name, 70)
    # get_playback_by_ID_mongo("646dc610bff39cb3a4b2f84b")
    # get_log()


