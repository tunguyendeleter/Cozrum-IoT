import requests
from requests.auth import HTTPDigestAuth

url = "http://172.16.0.2/ISAPI/ContentMgmt/download"

payload = '''
<downloadRequest version=\"1.0\" xmlns=\"http://www.isapi.org/ver20/XMLSchema\">\r\n
    <playbackURI>rtsp://172.16.0.2/Streaming/tracks/101/?starttime=20230503T124513Z&amp;endtime=20230503T125842Z&amp;name=00000001195000100&amp;size=206011232\r\n</playbackURI>\r\n
</downloadRequest'''
headers = {
    'Content-Type': 'application/xml'
}

response = requests.request("POST", url, headers=headers, data=payload, auth=HTTPDigestAuth('admin', "Cozrum@321"))
print()
if response.status_code == 200:
    with open('record_data.mp4', 'wb') as f:
        f.write(response.content)
        print("Record data saved to file.")