# NVR_Hikvision
Library NVR Hikvision

Hi everyone!
Now, i want to introduce you to my NVR library.

NVR_Hikvision.py : main code
From above library, you can
+ get track id of video channel to dev : get_cam_list()
+ search 'Record log' in NVR : record_video_log()
+ download video in NVR : download_video()
+ search log in MongoDB through isodate : search_log_iso_date()
+ get the lastest 20 event : get_new()
+ get data continuously : run()
+ set up to upload localhost in Library folder

Step 1:
- You must have
  + IP Address of NVR Hikvision
  + admin, password
  + port
  + VPN 
 
 Step 2:
 - Install the required libraries in NVR_Hikvision.py and controller.py in Library/BOOK/controller.py
 - Fill data in controller.py
 - Creat 'test' DB 
 - Collection :
   + 'Cam_Thu_Duc'
   + 'Config_cam
   + 'house'
   + 'room'
- key 'house','room','cam' in 'Cam_Thu_Duc' collection is identified by Object_id.

 Step 3:
 - Run app.py
 - You need to read and have knowledge about Flask API to understand controller.py
 - Search API to controller with arguement which is got in MongoDB or log in {{ip address}} on browser


if you have a question, send your question to hoangtruc8498@gmail.com










