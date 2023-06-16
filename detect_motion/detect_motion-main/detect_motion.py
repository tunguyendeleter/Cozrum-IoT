import cv2
import winsound
import time
import threading
#import imutils
import datetime

from flask import Flask,request,redirect, url_for, render_template
import config
from pathlib import Path
import json
import sqlite3



class employee:
    def __init__(self):
        self.infomations = information()


class information:
    def __init__(self):
        self.date = ""
        self.local_url= ""


def insert_database(db, data):
    conn = sqlite3.connect(db + ".db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO "
        + db
        + " VALUES(:date , :local_url )",
        {
            "date": data.date,
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
            local_url text
            )"""
        )
    except Exception as e:
        #print(e)
        pass
    conn.commit()
    conn.close()

#Cập nhật trên db,db là database có sẵn
def add_employee(db, data1,data2):
    obj1 = employee()
    # delete_all_database(db)
    for key in data1:
        obj1.infomations.date = data1[key]
    for key in data2:
        obj1.infomations.local_url = data1[key]
    insert_database(db, obj1.infomations)
    search_path_database(db, "")


alarm = False
alarm_mode = False
check_video = False
loop = True



def beep_alarm(writer, frame):
    global alarm
    writer.write(frame)
    #print("ALARM")
    alarm = False

#lst=[]
#lst_path=[]

def get_events(url,name,vi_tri,level):
    global alarm
    global alarm_mode
    global check_video
    global loop
    global lst_path
    global lst
    lst=[]
    lst_path=[]

    obj1 = employee()

    #cap = cv2.VideoCapture("YOUR_URL")
    cap = cv2.VideoCapture(url)

    width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer= cv2.VideoWriter('basicvideo123.mp4', cv2.VideoWriter_fourcc(*'m', 'p', '4', 'v'), 20, (width,height))

    _, start_frame = cap.read()
    # start_frame = imutils.resize(start_frame, width=900)
    start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
    start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)
    alarm_counter = 0
    while True:
        _, frame = cap.read()
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if threshold.sum() > level:
            #print(threshold.sum())
            alarm_counter += 1
        else:
            if alarm_counter > 0 and alarm_counter < 50:
                alarm_counter -= 1
            elif alarm_counter > 50:
                alarm_counter -= 3
        #cv2.imshow("Cam", threshold)
        print(alarm_counter)
        cv2.imshow(name, cv2.resize(frame,(900,500)))

        if alarm_counter > 15:
            if not alarm:
                alarm = True
                if check_video == False:
                    check_video = True
                    a = str(datetime.datetime.now())
                    obj1.infomations.date = a
                    lst.append(a)
                    print(str(a[0:19]))
                    hour=str(a[11:19].replace(':','_'))
                    day=str(a[0:10])
                    path=hour + '_' + day +"_" + vi_tri+".mp4"
                    obj1.infomations.local_url = path
                    lst_path.append(path)
                    insert_database("Test", obj1.infomations)
                    writer = cv2.VideoWriter(path , cv2.VideoWriter_fourcc(*'m', 'p', '4', 'v'), 20,(width, height))
            threading.Thread(target=beep_alarm(writer, frame)).start()
        else:
            check_video = False
            writer.release()

        key_pressed = cv2.waitKey(30)
        if key_pressed == ord("q"):
            alarm_mode = False
            print(lst)
            print(lst_path)
            break
        cv2.imshow(name, cv2.resize(frame,(900,500)))
    cap.release()
    cv2.destroyAllWindows()
    # if len(lst_path)>10:
    #     lst_path[0]=lst_path[5]
    #     lst_path[1]=lst_path[6]
    #     lst_path[2]=lst_path[7]
    #     lst_path[3]=lst_path[8]
    #     lst_path[4]=lst_path[9]


#a=  threading.Thread(target=get_events,args=("YOUR_URL","hello","cong",1800000,"q")).start()

t = threading.Thread(target=get_events,args=(0,"cam","webcam",100000)).start()

app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/update_time')
def update_time():
    return str(lst_path)

if __name__ == "__main__":
    app.run()
