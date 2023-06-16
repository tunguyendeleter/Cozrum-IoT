from flask import Blueprint,request,jsonify
from datetime import datetime
from NVR_Hikvision import NVR
import threading


books=Blueprint("books",__name__)


a = NVR(ip_cam="172.16.0.2", admin="admin", password="Cozrum@321", local_host_mongodb="localhost:27017")

@books.route("/")
def main():
    return ["******************************((:  WELCOME TO NVR SERVER  :))******************************",
           "https://github.com/hoangtruc1110/NVR_Hikvision.git" ,
           "Read it",
           "Thanks",
            "Goodbye Cozrum",
            "Cam on anh chi, sep Tu, anh Tu, Trang, Lien da dong hang cung em"]

@books.route("/realtime/<string:db>/<string:collection>",methods=['GET'])
def get_all_log(db,collection):
    current_date = datetime.now()
    start_time = current_date.strftime(f'%Y-%m-%dT00:00:00Z')
    end_time = current_date.strftime(f'%Y-%m-%dT23:59:59Z')
    cam = 0
    response = a.search_log_iso_date(db, collection, start_time, end_time, cam)
    for i in response:
        i['_id'] = str(i['_id'])
        i['Cam']=str(i['Cam'])
    t1 = threading.Thread(target=a.run).start()
    t2 = threading.Thread(target=response, args=(db,collection)).start()
    return response


@books.route("/get-all-log/1")
def get_all_log_1():
    return "hello"

@books.route('/with_parameters')
def with_parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    return jsonify(message="My name is " + name + " and I am " + str(age) + " years old")

@books.route("/get-log/<int:cam>",methods=['GET'])
def get_record_log(cam):
    real_time = str(datetime.now())
    year = int(real_time[0:4])
    mon = int(real_time[5:7])
    day = int(real_time[8:10])
    response=a.record_video_log(cam,year,mon,day,0,0,0,year,mon,day,23,59,59,50)
    return response

@books.route("/get-log/<int:cam>/track",methods=['GET'])
def get_record_log_track(cam):
    start = str(request.args.get('start'))
    end = str((request.args.get('end')))
    year_st=start[0:4]
    mon_st=start[5:7]
    day_st=start[8:10]
    hour_st=start[11:13]
    min_st=start[14:16]
    sec_st=start[17:19]
#------------------------
    year_end=end[0:4]
    mon_end=end[5:7]
    day_end=end[8:10]
    hour_end=end[11:13]
    min_end=end[14:16]
    sec_end=end[17:19]
    sum_result = str((request.args.get('sum')))
    response=a.record_video_log(cam,year_st,mon_st,day_st,hour_st,min_st,sec_st,year_end,mon_end,day_end,hour_end,min_end,sec_end,sum_result)
    return response

@books.route("/downloadmotionvideo/<string:add>/<int:cam>",methods=['GET'])
def download_motion_video(cam,add):
    time=request.args.get('time')
    year_z=time[0:4]
    month_z=time[5:7]
    day_z=time[8:10]
    hour_z=time[11:13]
    min_z=time[14:16]
    sec_z=time[17:19]
    response=a.download_video(cam,add,year_z,month_z,day_z,hour_z,min_z,sec_z)
    return response

@books.route("/searchlogmongo/<string:db>/<string:collection>",methods=['GET'])
def search_log_mongo_all(db,collection):
    current_date = datetime.now()
    start_time=current_date.strftime(f'%Y-%m-%dT00:00:00Z')
    end_time = current_date.strftime(f'%Y-%m-%dT23:59:59Z')
    cam=0
    response=a.search_log_iso_date(db,collection,start_time,end_time,cam)
    for i in response:
        i['_id']=str(i['_id'])
    return response


@books.route("/searchlogmongo/<string:db>/<string:collection>/<string:cam>",methods=['GET'])
def search_log_mongo_percam(db,collection,cam):
    current_date = datetime.now()
    start_time=current_date.strftime(f'%Y-%m-%dT00:00:00Z')
    end_time = current_date.strftime(f'%Y-%m-%dT23:59:59Z')
    response=a.search_log_iso_date(db,collection,start_time,end_time,cam)
    for i in response:
        i['_id']=str(i['_id'])
    return response


@books.route("/searchlogmongo/<string:db>/<string:collection>/<string:cam>/search",methods=['GET'])
def search_log_mongo(db,collection,cam):
    start_time=str(request.args.get("start"))
    end_time=str(request.args.get("end"))
    response=a.search_log_iso_date(db,collection,start_time,end_time,cam)
    for i in response:
        i['_id']=str(i['_id'])
    return response


@books.route("/getlistcam",methods=['GET'])
def get_list_cam():
    response=a.get_cam_list()
    # for i in response:
    #     i['_id']=str(i['_id'])
    return response

@books.route("/updatenamecam/<string:db>/<string:collection>/<string:add>",methods=['PUT'])
def update(db,collection,add):
    cam = int(request.args.get("cam"))
    name_change=str(request.args.get("name"))
    response=a.update(db,collection,cam,name_change,add)
    return response


@books.route("/search",methods=['GET'])
def currently():
    response=a.get_new()
    for i in response:
        i['_id']=str(i['_id'])
        i['Cam']=str(i['Cam'])
    return response


