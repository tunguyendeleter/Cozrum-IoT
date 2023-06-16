from hikvisionapi import Client
import datetime

def filter(data):
    lst=[]
    ip=data[0]['EventNotificationAlert']['ipAddress']
    lst.append(ip)
    time=data[0]['EventNotificationAlert']['dateTime']
    lst.append(time)
    event = data[0]['EventNotificationAlert']['eventDescription']
    lst.append(event)
    date=datetime.datetime.now()
    lst.append(str(date))
    return lst


cam = Client('http://172.16.0.2', 'admin', password='Cozrum@321', timeout=1)

try:
    response1 = cam.System.deviceInfo(method='get')
    print(response1)
    response = cam.Event.notification.alertStream(method='get', type='stream')
    if response:
        print( "response: ",filter(response))
    motion_detection_info = cam.System.Video.inputs.channels[1].motionDetection(method='get')
    inf=cam._check_session()
    print(inf)
    # if motion_detection_info:
    #     print("info:",motion_detection_info)

except Exception:
    pass
