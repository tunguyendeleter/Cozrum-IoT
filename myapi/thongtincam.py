from pymongo import MongoClient
from pydantic import BaseModel
from fastapi import FastAPI, Path
from requests.auth import HTTPDigestAuth
import requests
import xml.etree.ElementTree as ET
from bson.objectid import ObjectId
import copy

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


a = NVR_init("172.16.0.2", "admin", "Cozrum@321", "test", "cam_info", "location")
app = FastAPI()

class nvr_information(BaseModel):
    ip : str
    name : str
    password : str
@app.post('/add_nvr_info')
def add_nvr_info(body : nvr_information):
    '''
    post new information into database
    body contains
    ip address | name | password | camera name | location
    '''
    element = {"Ip adress": body.ip, "name": body.name, "password": body.password}
    a.collection.insert_one(element)
    return {"Ip adress": body.ip, "name": body.name, "password": body.password}

@app.get('/list_nvr_info')
def list_nvr_info():
    '''
    list all information in database
    '''
    rows = list(a.collection.find({}))
    for i in rows:
        i["_id"] = str(i["_id"])
    return rows

@app.get('/get_cam_list')
def get_cam_list():
    '''
    add new information into database
    body contains
    ip address | name | password | camera name | location
    '''
    lst = []
    url = f"http://{a.ip_address}/ISAPI/ContentMgmt/StreamingProxy/channels"

    response = requests.get(url, auth=HTTPDigestAuth(a.name, a.password)).text
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
                res.append({str(item): "cam " + str(cnt)})
        my_dict = {'ip': a.ip_address, 'admin': a.name, 'password': a.password, 'Cam': res, 'location': a.location}
        a.add_one_db(my_dict)
        a.print_one_db(my_dict)
        return lst

@app.get('/rename_cam')
def rename_cam(id_cam, cam_idx, name):
    '''
    update new camera name at a cam with ID
    '''
    object_id = ObjectId(id_cam)
    i = a.collection.find_one(object_id)
    del i["_id"]
    print(i)
    new_dict = copy.deepcopy(i)
    try:
        new_dict['Cam'][int(cam_idx)-1][f'{cam_idx}01'] = str(name)
        a.collection.find_one_and_replace(i, new_dict)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    rename_cam("647416587105571c955bd86e", 5,"whatthe")
    # get_cam_list()