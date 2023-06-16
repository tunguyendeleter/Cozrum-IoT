response= [{'EventNotificationAlert': {
    '@version': '1.0',
    '@xmlns': 'http://www.hikvision.com/ver20/XMLSchema',
    'ipAddress': '172.16.0.2',
    'portNo': '80',
    'protocol': 'HTTP',
    'macAddress': '24:0f:9b:2d:60:ab',
    'dynChannelID': '1',
    'dateTime': '2023-04-25T09:46:29',
    'activePostCount': '1',
    'eventType': 'VMD',
    'eventState': 'active',
    'eventDescription': 'Motion alarm'}}]
info: {'MotionDetection': {'@version': '2.0', '@xmlns': 'http://www.isapi.org/ver20/XMLSchema', 'enabled': 'true', 'enableHighlight': 'true', 'samplingInterval': '5', 'startTriggerTime': '1000', 'endTriggerTime': '1000', 'regionType': 'grid', 'Grid': {'rowGranularity': '18', 'columnGranularity': '22'}, 'MotionDetectionLayout': {'@version': '2.0', '@xmlns': 'http://www.isapi.org/ver20/XMLSchema', 'sensitivityLevel': '40', 'layout': {'gridMap': 'fffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffc'}, 'targetType': None}}}


{'DeviceInfo':
     {'@version': '1.0',
      '@xmlns': 'http://www.hikvision.com/ver20/XMLSchema',
      'deviceName': 'Network Video Recorder',
      'deviceID': '484a3530-3939-3239-3038-240f9b2d60ab',
      'model': 'DS-7108NI-Q1/M',
      'serialNumber': 'DS-7108NI-Q1/M0820220218CCRRJ50992908WVU',
      'macAddress': '24:0f:9b:2d:60:ab',
      'firmwareVersion': 'V4.32.115',
      'firmwareReleasedDate': 'build 211129',
      'encoderVersion': 'V5.0',
      'encoderReleasedDate': 'build 210928',
      'deviceType': 'NVR',
      'telecontrolID': '255',
      'manufacturer': 'hikvision'}}

def filter(data):
    lst=[]
    ip=data[0]['EventNotificationAlert']['ipAddress']
    lst.append(ip)
    time=data[0]['EventNotificationAlert']['dateTime']
    lst.append(time)
    event = data[0]['EventNotificationAlert']['eventDescription']
    lst.append(event)
    return lst
# print(response[0]['EventNotificationAlert'])
print(filter(response))