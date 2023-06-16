from requests.auth import HTTPDigestAuth
import requests
import time
from datetime import datetime
import pymongo
import xml.etree.ElementTree as ET
import os
from copy import deepcopy
from bson.objectid import ObjectId


class NVR:

    def __init__(self,ip_cam,admin,password,local_host_mongodb):
        self.ip_cam=ip_cam
        self.admin=admin
        self.password=password
        self.local_host_mongodb=local_host_mongodb


#Function to search record video log
#cam: desire cam,
#year,month,day,hour,min,sec _start: Start_time
#year,month,day,hour,min,sec _End: End_time
#sum_result: Total number of searches
    def record_video_log(self,cam,year_start,month_start,day_start,hour_start,min_start,sec_start,year_end,month_end,day_end,hour_end,min_end,sec_end,sum_result):
        lst_dict=[]
        url = f"http://{self.ip_cam}/ISAPI/ContentMgmt/Search"
        start_time=str(year_start) + "-" +str(month_start) +'-'+ str(day_start) + "T" + str(hour_start) + ':' + str(min_start) + ':' + str(sec_start) + "Z"
        end_time=str(year_end) + "-" +str(month_end) +'-'+ str(day_end) + "T" + str(hour_end) + ':' + str(min_end) + ':' + str(sec_end) + "Z"
        # print(start_time)
        # print(end_time)
        if cam==1:
          track_id=101
        elif cam==2:
          track_id=201
        elif cam==3:
          track_id=301
        elif cam==4:
          track_id=401
        elif cam==5:
          track_id=501
        elif cam==6:
          track_id=601

        payload = f'''
        <?xml version: \"1.0\" encoding=\"utf-8\"?>\r\n
        <CMSearchDescription>\r\n
            <searchID>484a3530-3939-3239-3038-240f9b2d60ab</searchID>\r\n
            <trackList>\r\n
                <trackID>{track_id}</trackID>
            </trackList>\r\n
            <timeSpanList>\r\n
                <timeSpan>\r\n
                    <startTime>{start_time}</startTime>\r\n
                    <endTime>{end_time}</endTime>\r\n
                </timeSpan>\r\n
            </timeSpanList>\r\n
            <maxResults>{sum_result}</maxResults>\r\n
            <searchResultPostion>0</searchResultPostion>\r\n
            <metadataList>\r\n
                <metadataDescriptor>//recordType.meta.std-cgi.com</metadataDescriptor>\r\n
            </metadataList>\r\n
        </CMSearchDescription>\r\n'''
        headers = {
          'Content-Type': 'application/xml'
        }

        response = requests.request("POST", url, headers=headers, data=payload, auth=HTTPDigestAuth(self.admin, self.password)).text
        # print(response)

        new_data=response[40:]
        import xml.etree.ElementTree as ET

        root = ET.fromstring(new_data)

        for child in root:
            for lop1 in child:
                # print(lop1.tag)
                # print(lop1.text)
                lst=[]
                for lop2 in lop1:
                    # print(lop2.tag)
                    if lop2.tag=='{http://www.hikvision.com/ver20/XMLSchema}trackID':
                        lst.append(lop2.text)
                    if lop2.tag=='{http://www.hikvision.com/ver20/XMLSchema}timeSpan':
                        for lop3 in lop2:
                            if lop3.tag=='{http://www.hikvision.com/ver20/XMLSchema}startTime':
                                lst.append(lop3.text)
                            if lop3.tag=='{http://www.hikvision.com/ver20/XMLSchema}endTime':
                                lst.append(lop3.text)
                    if lop2.tag=="{http://www.hikvision.com/ver20/XMLSchema}mediaSegmentDescriptor":
                        for lop3 in lop2:
                            if lop3.tag=="{http://www.hikvision.com/ver20/XMLSchema}playbackURI":
                                lst.append(lop3.text)
                my_dict = {"Cam": lst[0],
                           "Start_time": lst[1],
                           "End_time": lst[2],
                           "url": lst[3]
                           }
                lst_dict.append(my_dict)
                # print(lst)
                print(my_dict)
        return lst_dict

    #Function to download video through log search
    #cam:camera need to check
    #year,month,day,hour,min,sec: Time need to check
    def download_video(self,cam,address ,year, month, day, hour, min, sec):
        url_api_logsearch_download = "http://172.16.0.2/ISAPI/ContentMgmt/Search"
        name_cam=''
        track_id=''
        if cam == 1:
            track_id = 101
            name_cam = "Cong"
        elif cam == 2:
            track_id = 201
            name_cam = "Tret"
        elif cam == 3:
            track_id = 301
            name_cam = "Tang_1"
        elif cam == 4:
            track_id = 401
            name_cam = "Tang_2"
        elif cam == 5:
            track_id = 501
            name_cam = "Tang_3"
        elif cam == 6:
            track_id = 601
            name_cam = "Tang_4"

        motion_time = str(year) + "-" + str(month) + '-' + str(day) + "T" + str(hour) + ':' + str(min) + ':' + str(sec) + "Z"
        name_video =  str(hour) + 'h' + str(min) + 'p' + str(sec) + 's'

        def create_folder(add,name_cams):
            lst = [f'./RECORD',
                   f'./RECORD/{str(year)}',
                   f'./RECORD/{str(year)}/' + str(month),
                   f'./RECORD/{str(year)}/{str(month)}/' + str(day),
                   f'./RECORD/{str(year)}/{str(month)}/{str(day)}/' + add,
                   f'./RECORD/{str(year)}/{str(month)}/{str(day)}/{add}/' + name_cams]
            for i in lst:
                if not os.path.exists(i):
                    os.mkdir(i)
                    print("Folder %s created!" % i)
                else:
                    print("Folder %s already exists" % i)

        payload = f'''
        <?xml version: \"1.0\" encoding=\"utf-8\"?>\r\n
        <CMSearchDescription>\r\n
            <searchID>484a3530-3939-3239-3038-240f9b2d60ab</searchID>\r\n
            <trackList>\r\n
                <trackID>{track_id}</trackID>
            </trackList>\r\n
            <timeSpanList>\r\n
                <timeSpan>\r\n
                    <startTime>{motion_time}</startTime>\r\n
                    <endTime>{motion_time}</endTime>\r\n
                </timeSpan>\r\n
            </timeSpanList>\r\n
            <maxResults>1</maxResults>\r\n
            <searchResultPostion>0</searchResultPostion>\r\n
            <metadataList>\r\n
                <metadataDescriptor>//recordType.meta.std-cgi.com/</metadataDescriptor>\r\n
            </metadataList>\r\n
        </CMSearchDescription>\r\n'''
        headers = {
            'Content-Type': 'application/xml'
        }

        response = requests.request("POST", url_api_logsearch_download, headers=headers, data=payload,
                                    auth=HTTPDigestAuth('admin', "Cozrum@321")).text

        # print("Response:***** ",response.text)

        new_data = response[40:]
        import xml.etree.ElementTree as ET

        root = ET.fromstring(new_data)
        url_playback=''
        for child in root:
            for lop1 in child:
                # print(lop1.tag)
                # print(lop1.text)
                lst = []
                for lop2 in lop1:
                    # print(lop2.tag)
                    if lop2.tag == '{http://www.hikvision.com/ver20/XMLSchema}trackID':
                        lst.append(lop2.text)
                    if lop2.tag == '{http://www.hikvision.com/ver20/XMLSchema}timeSpan':
                        for lop3 in lop2:
                            if lop3.tag == '{http://www.hikvision.com/ver20/XMLSchema}startTime':
                                lst.append(lop3.text)
                            if lop3.tag == '{http://www.hikvision.com/ver20/XMLSchema}endTime':
                                lst.append(lop3.text)
                    if lop2.tag == "{http://www.hikvision.com/ver20/XMLSchema}mediaSegmentDescriptor":
                        for lop3 in lop2:
                            if lop3.tag == "{http://www.hikvision.com/ver20/XMLSchema}playbackURI":
                                lst.append(lop3.text)
                print(lst)
                url_playback = lst[3]
        url_api_download_video = "http://172.16.0.2/ISAPI/ContentMgmt/download"

        payload = f'''
        <downloadRequest version=\"1.0\" xmlns=\"http://www.isapi.org/ver20/XMLSchema\">\r\n
            <playbackURI>{url_playback}\r\n</playbackURI>\r\n
        </downloadRequest'''
        headers = {
            'Content-Type': 'application/xml'
        }
        response_video = requests.request("POST", url_api_download_video, headers=headers, data=payload,
                                          auth=HTTPDigestAuth('admin', "Cozrum@321"))
        print()
        if response_video.status_code == 200:
            create_folder(address,name_cam)
            with open(f'RECORD/{str(year)}/{str(month)}/{str(day)}/{address}/{name_cam}/{name_video}.mp4', 'wb') as f:
                f.write(response_video.content)
                print("Record data saved to file.")
        return f"Downloading in RECORD folder"

    #Function to search log through MongoDB
    #db:database need to find
    #collection: need to find
    #start_time: Start time to search
    #end_time: end time to search
    def search_log_iso_date(self,db,collection,start_time,end_time,cam):
        lst=[]
        myclient = pymongo.MongoClient(f"mongodb://{self.local_host_mongodb}/")
        mydb = myclient[db]
        mycol = mydb[collection]
        if cam == 0 :
            search_log = mycol.find({
                'Time': {
                    '$gte': (start_time),
                    '$lte': (end_time)
                }})
            for i in search_log:
                # print(i)
                lst.append(i)
            return lst
        else:
            search_log=mycol.find({
                'Time':{
                    '$gte':(start_time),
                    '$lte':(end_time)
                },"Cam":cam})
            for i in search_log:
                # print(i)
                lst.append(i)
            return lst

    def get_cam_list(self):
        lst=[]
        url = f"http://{self.ip_cam}/ISAPI/ContentMgmt/StreamingProxy/channels"

        response = requests.get(url, auth=HTTPDigestAuth(self.admin, self.password)).text
        if response:
            root = ET.fromstring(response)
            res = []
            # Find the list of ID elements
            id_obj = root.findall(".//{http://www.isapi.org/ver20/XMLSchema}id")
            # Extract elements in list
            id_list = [str(item.text) for item in id_obj]
            cnt = 0
            for item in id_list:
                if item[-1] == '1':
                    cnt += 1
                    res.append({str(item) : "cam " + str(cnt)})
            # print(res)
            count=0
            return res  # return re

    def run(self):
        myclient = pymongo.MongoClient(f"mongodb://{self.local_host_mongodb}/")
        mydb = myclient['test']
        mycol = mydb["Cam_Thu_Duc"]

        url = f"http://{self.ip_cam}/ISAPI/ContentMgmt/logSearch"

        payload={}
        headers = {
            'Authorization': 'Bearer ¨XXXXX',
            'content-type': 'application/json',
        }

        id='484a3530-3939-3239-3038-240f9b2d60ab'

        while True:
            a = str(datetime.now())
            time_z = a[:10]
            b = a[11:14]
            m = int(a[14:16])
            s = int(a[17:19]) - 50
            # print(m)
            if 0 <= s < 10:
                s = '0' + str(s)
            elif s < 0:
                s = 60 + s
                m = m - 1
                if m < 0:
                    m = 60 + 1
            # print(s)
            start_time = time_z + 'T' + b + str(m) + ':' + str(s) + 'Z'
            print(type(start_time))
            print(start_time)
            end_time=time_z+"T23:59:59Z"
            command=f'''
            <?xml version='1.0' encoding='utf-8'?>
        <CMSearchDescription version='1.0' xmlns='http://www.hikvision.com/ver20/XMLSchema'>
            <searchID>484a3530-3939-3239-3038-240f9b2d60ab</searchID>
            <timeSpanList>
                <timeSpan>
                    <startTime>{start_time}</startTime>
                    <endTime>{end_time}</endTime>
                </timeSpan>
            </timeSpanList>
            <metaId>log.hikvision.com/Alarm</metaId>
            <searchResultPostion>0</searchResultPostion>
            <maxResults>6</maxResults>
        </CMSearchDescription>
            '''

            response=requests.post(url,command, auth=HTTPDigestAuth(self.admin, self.password)).text
            if response:
                # print(type(response))
                # print("status ****************************************************************** :   ",response)
                data=response[40:]
                root = ET.fromstring(data)
                if root[2].text == "NO MATCHES":
                    pass
                else:
                    name_cam = ''
                    for childs in root:  # country
                        for child in childs:
                            for lop1 in child:
                                lst = []
                                for lop2 in lop1:
                                    # print(lop2.text)
                                    # print(lop2.tag)
                                    if lop2.tag == "{http://www.hikvision.com/ver20/XMLSchema}metaId":
                                        lst.append(lop2.text[18:])
                                        # print(lop2.text)
                                    if lop2.tag == "{http://www.hikvision.com/ver20/XMLSchema}StartDateTime":
                                        lst.append(lop2.text)
                                        # print(lop2.text)

                                    if lop2.tag == "{http://www.hikvision.com/ver20/XMLSchema}localId":
                                        if lop2.text=="D1":
                                            name_cam=ObjectId("64756db4fc7d0180b8c169fa")
                                        elif lop2.text=="D2":
                                            name_cam=ObjectId("64756dc1b9b32448aaed0f3e")
                                        elif lop2.text=="D3":
                                            name_cam=ObjectId("64756d94006980fc3b50268c")
                                        elif lop2.text=="D4":
                                            name_cam=ObjectId("64756dd73085bc4e49aa9053")
                                        elif lop2.text=="D5":
                                            name_cam=ObjectId("64756dda154ea8c72bf9936b")
                                        elif lop2.text=="D6":
                                            name_cam=ObjectId("64756ddf1b3b0cd208d4a362")
                                        lst.append(name_cam)

                                        # print(lop2.text)
                                # print(lst)
                                myquery = { "Alarm": lst[0], "Time": lst[1] , "Cam": lst[2]}
                                print(myquery)
                                duplicate = mycol.find(myquery)
                                count = 0
                                for x in duplicate:
                                    count += 1
                                if count == 0:
                                    print("not exist")
                                    mycol.insert_one(myquery)
                                else:
                                    print("exist")
            # time.sleep(1)
            time.sleep(4)

    def update(self,db,collection,cam,name,add):
        myclient = pymongo.MongoClient(f"mongodb://{self.local_host_mongodb}/")
        mydb = myclient[db]
        mycol = mydb[collection]
        all=mycol.find({'Address':add})
        dictt={}
        for i in all:
            # print(i)
            dictt=i
            dictt.pop('_id')
        new_dict=deepcopy(dictt)
        # print(dictt['Cam'][int(cam)-1][f'{cam}01'])
        new_dict['Cam'][int(cam)-1][f'{cam}01']=str(name)
        # print(dictt)
        # print(new_dict)
        mycol.find_one_and_replace(dictt,new_dict)
        return "Changed"

    def get_new(self):
        myclient = pymongo.MongoClient(f"mongodb://localhost:27017/")
        mydb = myclient['test']
        mycol = mydb['Cam_Thu_Duc']
        newest_doc = mycol.find(sort=[('_id', pymongo.DESCENDING)]).limit(20)
        lst = []
        for i in newest_doc:
            print(i)
            lst.append(i)
        return lst


