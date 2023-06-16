from flask import Flask,request
from flask_cors import CORS,cross_origin
import requests
import config
from pathlib import Path

#Tạo file images trong file chứa code
#https://documenter.getpostman.com/view/13088306/TVeqcn2C#81576510-b381-4eac-a6b0-a53ba8c9fa90

import json
import sqlite3

class employee:
    def __init__(self):
        self.infomations = information()


class information:
    def __init__(self):
        self.date = ""
        self.placeID = ""
        self.deviceID = ""
        self.personName = ""
        self.aliasID = ""
        self.id = ""
        self.detected_image_url = ""
        self.local_url= ""


def insert_database(db, data):
    conn = sqlite3.connect(db + ".db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO "
        + db
        + " VALUES(:date , :placeID , :deviceID , :personName , :aliasID , :id , :detected_image_url, :local_url )",
        {
            "date": data.date,
            "placeID": data.placeID,
            "deviceID": data.deviceID,
            "personName": data.personName,
            "aliasID": data.aliasID,
            "id": data.id,
            "detected_image_url": data.detected_image_url,
            "local_url" : data.local_url
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
            date text,
            placeID text,
            deviceID text,
            personName text,
            aliasID text,
            id text,
            detected_image_url text,
            local_url text
            )"""
        )
    except Exception as e:
        print(e)
    conn.commit()
    conn.close()

#Cập nhật trên db,db là database có sẵn
def add_employee(db, data):
    obj1 = employee()
    # delete_all_database(db)
    for key in data:
        if key == "date":
            obj1.infomations.date = data[key]
        elif key == "placeID":
            obj1.infomations.placeID = data[key]
        elif key == "deviceID":
            obj1.infomations.deviceID = data[key]
        elif key == "personName":
            obj1.infomations.personName  = data[key]
        elif key == "aliasID":
            obj1.infomations.aliasID = data[key]
        elif key == "id":
            obj1.infomations.id = data[key]
        elif key == "detected_image_url":
            obj1.infomations.detected_image_url  = data[key]
            obj1.infomations.local_url  = download_images(data[key], data["date"])
    insert_database(db, obj1.infomations)
    search_path_database(db, "")

#datas là dữ liệu trả về liên tục trên webhook
def download_images(data, date):
    #for key in data:
        #if key == "detected_image_url":
    img_data = requests.get(data).content
    a=date[11:].replace(":","_")
    local_url=f'{date[0:10]}_{a}'
    path = Path.cwd()
    cmd = f'{path}\images\{local_url}.jpg'
    with open("images/" + date[0:10] +'_'+ a + ".jpg", "wb") as handler:
        handler.write(img_data) #down ảnh về file
    return cmd





url = "https://43c2-123-21-38-50.ngrok-free.app"

payload={
  "action_type": "update",
  "aliasID": "",
  "data_type": "log",
  "date": "",
  "detected_image_url": "",
  "deviceID": "H2246HV0129",
  "deviceName": "H2246HV0129",
  "hash": "",
  "id": "",
  "keycode": "",
  "personID": "",
  "personName": "",
  "personTitle": "",
  "placeID": "4628",
  "placeName": "Myhome",
  "mask": "0",
  "time": ''
}
headers = {
  'Authorization': 'Authorization'
}

app= Flask(__name__)
CORS(app)
app.config['COR HEADERS']="content type"

@app.route('/',methods=['POST','GET'])
@cross_origin(origin="*")
def index():
    create_database("Test")
    a=json.loads(request.data.decode("utf-8"))
    add_employee("Test",a)
    print(type(a))
    print("Thong tin Hanet : ",a)
    #download_images(a)
    from flask import jsonify
    resp=jsonify(success=True)
    return resp

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=9999)

