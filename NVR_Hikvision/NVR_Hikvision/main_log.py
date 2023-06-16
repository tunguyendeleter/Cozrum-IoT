from requests.auth import HTTPDigestAuth
import requests
import time
from datetime import datetime
import sqlite3
url = "http://172.16.0.2/ISAPI/ContentMgmt/logSearch"
import xml.etree.ElementTree as ET

class employee:
    def __init__(self):
        self.infomations = information()

class information:
    def __init__(self):
        self.Detect = ""
        self.Time= ""
        self.Cam=""

def insert_database(db, data):
    conn = sqlite3.connect(db + ".db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO "
        + db
        + " VALUES(:Detect , :Time , :Cam )",
        {
            "Detect": data.Detect,
            "Time": data.Time,
            "Cam": data.Cam
        },
    )
    conn.commit()
    conn.close()

#tìm table có sẵn theo keyword
def search_path_database(db, key):
    conn = sqlite3.connect(db + ".db") #connect
    c = conn.cursor()
    c.execute("SELECT * FROM " + db + " WHERE date = :date", {"date": key})
    print(c.fetchall()) #in ra những gì mình chọn vào table
    conn.commit()
    conn.close()

def filter(db):
    conn = sqlite3.connect(db + ".db")  # connect
    c = conn.cursor()
    c.execute("""delete from Detect_Cam
where rowid in (
  select rowid
  from (
    select
      rowid,
      row_number() over (
        partition by Detect,Time, Cam
        -- order by some_expression
        ) as n
    from Detect_Cam
  )
  where n > 1
);""")
    conn.commit()
    conn.close()

#xóa tất cả data base
def delete_all_database(db):
    conn = sqlite3.connect(db + ".db")
    c = conn.cursor()
    c.execute("DELETE from " + db)
    conn.commit()
    conn.close()

#Tạo 1 data base mới
def create_database(name):
    conn = sqlite3.connect(name + ".db")
    c = conn.cursor()
    try:
        c.execute(
            """CREATE TABLE """
            + name
            + """(
            Detect text,
            Time text,
            Cam text
            )"""
        )

    except Exception as e:
        #print(e)
        pass
    conn.commit()
    conn.close()

obj1 = employee()
create_database("Detect_Cam")


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
    s = int(a[17:19]) - 40
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
                                lst.append(lop2.text)
                                obj1.infomations.Detect=lop2.text[18:]
                                # print(lop2.text)
                            if lop2.tag == "{http://www.hikvision.com/ver20/XMLSchema}StartDateTime":
                                lst.append(lop2.text)
                                obj1.infomations.Time = lop2.text
                                # print(lop2.text)
                            if lop2.tag == "{http://www.hikvision.com/ver20/XMLSchema}localId":
                                lst.append(lop2.text)
                                obj1.infomations.Cam = lop2.text
                                # print(lop2.text)
                                insert_database("Detect_Cam", obj1.infomations)
                                filter("Detect_Cam")
                        print(lst)
    # time.sleep(1)
    time.sleep(4)
