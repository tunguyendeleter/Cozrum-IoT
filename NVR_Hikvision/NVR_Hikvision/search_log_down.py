import requests
from requests.auth import HTTPDigestAuth

url = "http://172.16.0.2/ISAPI/ContentMgmt/Search"

n=int(input("Nhập Camera cần check 1-6 : "))
#input start_time
year_start=int(input("Nhập năm : "))
month_start=int(input("Nhập tháng bắt đầu: "))
day_start=int(input("Nhập ngày bắt đầu : "))
hour_start=int(input("Nhập giờ bắt đầu : "))
min_start=int(input("Nhập phút bắt đầu : "))
sec_start=int(input("Nhập giây bắt đầu : "))
#input end_time
year_end=int(input("Nhập năm : "))
month_end=int(input("Nhập tháng kết thúc : "))
day_end=int(input("Nhập ngày kết thúc : "))
hour_end=int(input("Nhập giờ kết thúc : "))
min_end=int(input("Nhập phút kết thúc : "))
sec_end=int(input("Nhập giây kết thúc : "))

sum_result=int(input("Nhập số kết quả cần check: "))


start_time=str(year_start) + "-" +str(month_start) +'-'+ str(day_start) + "T" + str(hour_start) + ':' + str(min_start) + ':' + str(sec_start) + "Z"
end_time=str(year_end) + "-" +str(month_end) +'-'+ str(day_end) + "T" + str(hour_end) + ':' + str(min_end) + ':' + str(sec_end) + "Z"
print(start_time)
print(end_time)
if n==1:
  track_id=101
elif n==2:
  track_id=201
elif n==3:
  track_id=301
elif n==4:
  track_id=401
elif n==5:
  track_id=501
elif n==6:
  track_id=601

payload = f'''
<?xml version: \"1.0\" encoding=\"utf-8\"?>\r\n
<CMSearchDescription>\r\n
    <searchID>484a3530-3939-3239-3038-240f9b2d60ab</searchID>\r\n
    <trackList>\r\n
        <trackID>{track_id}</trackID>
    </trackList>\r\n
    <timeSpanList>\r\n
        <timeSpan>\r\n
            <startTime>{start_time}</startTime>\r\n
            <endTime>{end_time}</endTime>\r\n
        </timeSpan>\r\n
    </timeSpanList>\r\n
    <maxResults>{sum_result}</maxResults>\r\n
    <searchResultPostion>0</searchResultPostion>\r\n
    <metadataList>\r\n
        <metadataDescriptor>//recordType.meta.std-cgi.com</metadataDescriptor>\r\n
    </metadataList>\r\n
</CMSearchDescription>\r\n'''
headers = {
  'Content-Type': 'application/xml'
}

response = requests.request("POST", url, headers=headers, data=payload, auth=HTTPDigestAuth('admin', "Cozrum@321")).text
print(response)
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

