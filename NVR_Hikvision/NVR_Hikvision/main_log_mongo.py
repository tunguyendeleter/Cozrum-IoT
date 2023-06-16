from requests.auth import HTTPDigestAuth
import requests
import time
from datetime import datetime
import pymongo
import xml.etree.ElementTree as ET

def main():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["test"]
    mycol = mydb["Cam_Thu_Duc"]

    url = "http://172.16.0.2/ISAPI/ContentMgmt/logSearch"

    payload={}
    headers = {
        'Authorization': 'Bearer ¨XXXXX',
        'content-type': 'application/json',
    }

    id='484a3530-3939-3239-3038-240f9b2d60ab'


    def remove_duplicate(db,collection):
        mydb = myclient[db]
        mycol = mydb[collection]
        mycol.find().sort("Timestamp", pymongo.ASCENDING)
        mycol.aggregate([{ "$sort": { "Timestamp": 1 } },
        {
          "$group": {
        "_id": { "Time":"$Time","Cam":"$Cam" },
        "doc": { "$first": "$$ROOT" }
        }
         },
        { "$replaceRoot": { "newRoot": "$doc" } },
        { "$out": collection }])

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
        #response = requests.request("GET", url, headers=headers, data=payload)

        #print(response.text)

        # print(command)
        #url = 'http://httpbin.org/digest-auth/auth/user/pass'


        response=requests.post(url,command, auth=HTTPDigestAuth('admin', "Cozrum@321")).text
        if response:
            # print(type(response))
            # print("status ****************************************************************** :   ",response)
            data=response[40:]
            root = ET.fromstring(data)
            if root[2].text == "NO MATCHES":
                pass
            else:
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
                                    name_cam=''
                                if lop2.tag == "{http://www.hikvision.com/ver20/XMLSchema}localId":
                                    if lop2.text=="D1":
                                        name_cam="Cong"
                                    elif lop2.text=="D2":
                                        name_cam="Tang_tret"
                                    elif lop2.text=="D3":
                                        name_cam="Tang_1"
                                    elif lop2.text=="D4":
                                        name_cam="Tang_2"
                                    elif lop2.text=="D5":
                                        name_cam="Tang_3"
                                    elif lop2.text=="D6":
                                        name_cam="Tang_4"
                                    lst.append(name_cam)

                                    # print(lop2.text)
                            # print(lst)
                            # timestamp_Z=float(datetime.timestamp(datetime.now()))
                            myquery = {"_id": str(datetime.now())[22:]+'_'+lst[1]+'_'+lst[2], "Alarm": lst[0], "Time": lst[1] , "Cam": lst[2]}
                            print(myquery)
                            mydoc = mycol.find( {"Alarm": lst[0], "Time": lst[1] , "Cam": lst[2]})
                            cnt = 0
                            for x in mydoc:
                                cnt += 1

                            if cnt == 0:
                                print("not exit")
                                mycol.insert_one(myquery)
                            else:
                                print("exit")
                            print(cnt)
                            # remove_duplicate("test","Cam_Thu_Duc")
        # time.sleep(1)
        time.sleep(4)

if __name__ == '__main__':
    main()
