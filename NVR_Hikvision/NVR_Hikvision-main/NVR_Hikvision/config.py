import NVR_Hikvision
import pymongo
from copy import deepcopy
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["test"]
# mycol = mydb["Config cam Thu_Duc"]
# ip_cam='172.16.0.2'
# track_id=''
# cam=0
# lst=[]
# for i in range(1,7):
#     if i == 101 :
#         track_id="Cong"
#         lst.append(track_id)
#     if i == 201 :
#         track_id="Tang tret"
#         lst.append(track_id)
#
#     if i == 301 :
#         track_id = "Tang_1"
#         lst.append(track_id)
#     if i == 401 :
#         track_id = "Tang_2"
#         lst.append(track_id)
#
#     if i == 501 :
#         track_id = "Tang_3"
#         lst.append(track_id)
#
#     if i == 601 :
#         track_id = "Tang_4"
#         lst.append(track_id)
#
# a = {'ip': ip_cam, 'admin': "admin", " password ": "CZozrum@321", "Cam": lst}
# mycol.insert_one(a)
# cam=input("Nhap cam : ")
# new_name_cam=input(" Nhap ten cam: ")

a = NVR_Hikvision.NVR(ip_cam="172.16.0.2", admin="admin", password="Cozrum@321", local_host_mongodb="localhost:27017")
# b=a.get_cam_list()
# if cam=='1':
#     b[0]['101']=new_name_cam
# if cam=='2':
#     b[1]['201']=new_name_cam
# if cam=='3':
#     b[2]['301']=new_name_cam
# if cam=='4':
#     b[3]['401']=new_name_cam
# if cam=='5':
#     b[4]['501']=new_name_cam
# if cam=='6':
#     b[5]['601']=new_name_cam
#
#
# # for keys, value in b[1].items():
# #    print(int(keys))
# print(b)


# b=a.get_cam_list('test','Config_cam',"19C Bui Thi Xuan")
# print(b)
# print(type(b))

#
def update(db,collection,cam,name,add):
    myclient = pymongo.MongoClient(f"mongodb://localhost:27017/")
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


update(db='test',collection='Config_cam',cam='1',name="Cong",add='19C Bui Thi Xuan')