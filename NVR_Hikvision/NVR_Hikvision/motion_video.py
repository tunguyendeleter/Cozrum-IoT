import requests
from requests.auth import HTTPDigestAuth
import os

url_api_logsearch_download = "http://172.16.0.2/ISAPI/ContentMgmt/Search"

n=int(input("Nhập Camera cần check 1-6 : "))
#input start_time
year=int(input("Nhập năm : "))
month=int(input("Nhập tháng : "))
day=int(input("Nhập ngày : "))
hour=int(input("Nhập giờ : "))
min=int(input("Nhập phút : "))
sec=int(input("Nhập giây : "))


if n==1:
  track_id=101
  name_cam="Cong"
elif n==2:
  track_id=201
  name_cam="Tret"
elif n==3:
  track_id=301
  name_cam="Tang_1"
elif n==4:
  track_id=401
  name_cam="Tang_2"
elif n==5:
  track_id=501
  name_cam="Tang_3"
elif n==6:
  track_id=601
  name_cam="Tang_4"

motion_time=str(year) + "-" +str(month) +'-'+ str(day) + "T" + str(hour) + ':' + str(min) + ':' + str(sec) + "Z"
name_video=str(year)+'_' + str(month) + '_' + str(day) + '_' + str(hour) + 'h' + str(min) + 'p' + str(sec) + 's'+ "_" + name_cam

def create_folder(name_cams):
    path = './'+name_cams
    if not os.path.exists(path):
      os.mkdir(path)
      print("Folder %s created!" % path)
    else:
      print("Folder %s already exists" % path)

payload = f'''
<?xml version: \"1.0\" encoding=\"utf-8\"?>\r\n
<CMSearchDescription>\r\n
    <searchID>484a3530-3939-3239-3038-240f9b2d60ab</searchID>\r\n
    <trackList>\r\n
        <trackID>{track_id}</trackID>
    </trackList>\r\n
    <timeSpanList>\r\n
        <timeSpan>\r\n
            <startTime>{motion_time}</startTime>\r\n
            <endTime>{motion_time}</endTime>\r\n
        </timeSpan>\r\n
    </timeSpanList>\r\n
    <maxResults>1</maxResults>\r\n
    <searchResultPostion>0</searchResultPostion>\r\n
    <metadataList>\r\n
        <metadataDescriptor>//recordType.meta.std-cgi.com/</metadataDescriptor>\r\n
    </metadataList>\r\n
</CMSearchDescription>\r\n'''
headers = {
  'Content-Type': 'application/xml'
}

response = requests.request("POST", url_api_logsearch_download, headers=headers, data=payload, auth=HTTPDigestAuth('admin', "Cozrum@321")).text

# print("Response:***** ",response.text)

new_data=response[40:]
import xml.etree.ElementTree as ET

root = ET.fromstring(new_data)

for child in root:
    for lop1 in child:
        # print(lop1.tag)
        # print(lop1.text)
        lst=[]
        for lop2 in lop1:
            # print(lop2.tag)
            if lop2.tag=='{http://www.hikvision.com/ver20/XMLSchema}trackID':
                lst.append(lop2.text)
            if lop2.tag=='{http://www.hikvision.com/ver20/XMLSchema}timeSpan':
                for lop3 in lop2:
                    if lop3.tag=='{http://www.hikvision.com/ver20/XMLSchema}startTime':
                        lst.append(lop3.text)
                    if lop3.tag=='{http://www.hikvision.com/ver20/XMLSchema}endTime':
                        lst.append(lop3.text)
            if lop2.tag=="{http://www.hikvision.com/ver20/XMLSchema}mediaSegmentDescriptor":
                for lop3 in lop2:
                    if lop3.tag=="{http://www.hikvision.com/ver20/XMLSchema}playbackURI":
                        lst.append(lop3.text)
        print(lst)
        url_playback=lst[3]
url_api_download_video = "http://172.16.0.2/ISAPI/ContentMgmt/download"

payload = f'''
<downloadRequest version=\"1.0\" xmlns=\"http://www.isapi.org/ver20/XMLSchema\">\r\n
    <playbackURI>{url_playback}\r\n</playbackURI>\r\n
</downloadRequest'''
headers = {
    'Content-Type': 'application/xml'
}
response_video = requests.request("POST", url_api_download_video, headers=headers, data=payload, auth=HTTPDigestAuth('admin', "Cozrum@321"))
print()
if response_video.status_code == 200:
    create_folder(name_cam)
    with open(f'{name_cam}/{name_video}.mp4', 'wb') as f:
        f.write(response_video.content)
        print("Record data saved to file.")