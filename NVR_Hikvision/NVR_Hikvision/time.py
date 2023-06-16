from datetime import datetime
from requests.auth import HTTPDigestAuth
import requests
import time
import pyhik
import hikvision
url = "http://172.16.0.2/ISAPI/ContentMgmt/logSearch"

a=str(datetime.now())
time_z=a[:10]
b=a[11:17]
s=int(a[17:19])-10
if s<10:
    s='0'+str(s)

# print(time)
# print(b)
nt=time_z+'T'+b+str(s)+'Z'
print(type(nt))
print(nt)
# print(s)
id='484a3530-3939-3239-3038-240f9b2d60ab'
command=f'''<?xml version='1.0' encoding='utf-8'?>
<CMSearchDescription version='1.0' xmlns='http://www.hikvision.com/ver20/XMLSchema'>
    <searchID>484a3530-3939-3239-3038-240f9b2d60ab</searchID>
    <timeSpanList>
        <timeSpan>
            <startTime>2023-05-03T14:08:30Z</startTime>
            <endTime>2023-05-01T23:59:59Z</endTime>
        </timeSpan>
    </timeSpanList>
    <metaId>log.hikvision.com</metaId>
    <searchResultPostion>1</searchResultPostion>
    <maxResults>6</maxResults>
</CMSearchDescription>'''
print(command)
response=requests.post(url,command, auth=HTTPDigestAuth('admin', "Cozrum@321"))
if response:
    print(type(response))
    print("status ****************************************************************** :   ",response.text)
time.sleep(1)