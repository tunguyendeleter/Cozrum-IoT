# NVR_Hikvision
Library NVR Hikvision
This library uses FastAPI instead of Flask

### Folder

    ├── myapi                    
        ├── nvr_api.py (main)    # API to get log, search camera information
        ├── thongtincam.py       # API to store camera information on collection
        ├── log_api.py           # Get camera information and config
        └── database.json        # VPN and database information
#### nvr_api.py : main code
From above library, you can
+ search playback video information within specific time :
    -     search_playback_by_time()
+ get playback video from collection :
    -     get_playback_by_mongoid()
+ download video in NVR :
    -     download_playback_by_mongoid()
+ search log in MongoDB :
    -     search_log_by_time()
    -     search_log_by_id()
+ get data in collection by page :
    -     log_db_by_page()
+ get data continuously :
    -     NVR_init.get_log()
    -     NVR_init.thread_get_log() 
Step 1:
- You must have
  + IP Address of NVR Hikvision
  + admin, password
  + port
  + VPN 
 
 Step 2:
 - Connect to VPN 
 - Create MongoDB collections
 - Example of keys in collection:
    + Collection 1:
    ```json
    {
      "_id": "id",
      "Alarm": "action",
      "Time": "time",
      "Cam": "track id"
    }
    ```
 Step 3:
 - Modify database.json with "ip_address", "name", "password", "db", "collection", "location".
 - Run nvr_api.py by "uvicorn nvr_api:app --reload", FastAPI command in command prompt
 - You need to read and have knowledge about Flask API to understand controller.py
 - Test API at http://127.0.0.1:8000/docs on browser

#### thongtincam.py : 
From above library, you can
+ add new NVR information to mongoDB :
    -     add_nvr_info()
+ get list of all information from collection :
    -     list_nvr_info()
+ get cam list from connecting HVR :
    -     get_cam_list()
+ rename cam in collection :
    -     rename_cam()

for more information, connect me by email "tunguyendeleter@gmail.com"



