import pymongo
from datetime import datetime
import time
from hashlib import md5
from bson.json_util import dumps
cluster="mongodb+srv://htruc:11102001@atlascluster.kznfpxb.mongodb.net/?retryWrites=true&w=majority"

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
# db=myclient.example.courses.find().sort([("namee",pymongo.ASCENDING)]).limit(10)
# print(myclient.list_database_names())
# mydb = myclient['test']


def search_log_iso_date(db,collection,start_time,end_time,cam):
	mydb = myclient[db]
	mycol = mydb[collection]
	search_log=mycol.find({
		'Time':{
			'$gte':(start_time),
			'$lte':(end_time)
		},"Cam":cam})
	for i in search_log:
		print(i)

search_log_iso_date("test",'Cam_Thu_Duc','2023-05-19T09:42:50Z',"2023-05-19T09:46:29Z",cam="Cong")


lst=[1,2,3,4,5,8,7]
a=0
b=0