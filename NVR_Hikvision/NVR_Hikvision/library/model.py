from datetime import datetime

current_date = datetime.now()
# # print(current_date.strftime('%Y-%m-%dT0:0:0Z'))
import NVR_Hikvision
#
a = NVR_Hikvision.NVR(ip_cam="172.16.0.2", admin="admin", password="Cozrum@321", local_host_mongodb="localhost:27017")
# # a.search_log_iso_date("test","Cam_Thu_Duc",'2023-05-23T00:00:00Z','2023-05-23T23:59:59Z',"Tang_1")
#
# def get_all_log(db,collection):
#     current_date = datetime.now()
#     day = str(current_dates.strftime(f'%Y-%m-%dT'))
#     hour = int(current_dates.strftime(f'%H'))
#     hour_st=hour-2
#     hour_en = hour + 2
#     if hour<=11:
#         hour_st='0'+hour_st
#     elif hour<=7:
#         hour_st='0'+hour_st
#         hour_en='0'+hour_en
#     elif hour==1:
#         hour_st=23
#         hour_en='0'+'3
#     start_time_Z = f'{day}{str(hour_st)}:00:00Z'
#     end_time_Z = f'{day}{str(hour_en)}:59:59Z'
#     cam = 0
#     response = a.search_log_iso_date(db, collection, start_time_Z, end_time_Z, cam)
#
# current_dates = datetime.now()
# hour=int(current_dates.strftime(f'%H'))
# hour_ne=hour+2
# print(hour)
# day=str(current_dates.strftime(f'%Y-%m-%dT'))
# print(day)
# start_time_Z = f'{day}{str(hour-2)}:00:00Z'
# end_time_Z = f'{day}{str(hour+2)}:59:59Z'
# print(start_time_Z)
# print(end_time_Z)
# # print(time-start_time)
#
# r=get_all_log('test',"Cam_Thu_Duc")
# print(r)
#
a.search_log_iso_date('test','Cam_Thu_Duc','2023-05-23T09:25:00Z','2023-05-23T23:59:59Z',0)

# a='2023-05-23T08:00:00Z'
#
# year=a[0:4]
# mon=a[5:7]
# day=a[8:10]
# hour=a[11:13]
# min=a[14:16]
# sec=a[17:19]
# print(year)
# print(mon)
# print(day)
# print(hour)
# print(min)
# print(sec)
