from requests.auth import HTTPDigestAuth
import requests
import xml.etree.ElementTree as ET
from fastapi import FastAPI

app = FastAPI()

@app.get("/get_cam_list/camlist")
def get_cam_list():
    url = "http://172.16.0.2/ISAPI/ContentMgmt/StreamingProxy/channels"

    response = requests.get(url, auth=HTTPDigestAuth('admin', "Cozrum@321")).text
    if response:
        root = ET.fromstring(response)
        res = []
        # Find the list of ID elements
        id_obj = root.findall(".//{http://www.isapi.org/ver20/XMLSchema}id")
        # Extract elements in list
        id_list = [str(item.text) for item in id_obj]
        cnt = 0
        for item in id_list:
            if item[-1] == '1':
                cnt += 1
                res.append({"cam " + str(cnt) : item})
        print(res)
        return res

@app.get("/get_cam_list/camconfig")
def get_cam_config():
    url = "http://172.16.0.2/ISAPI/ContentMgmt/StreamingProxy/channels"

    response = requests.get(url, auth=HTTPDigestAuth('admin', "Cozrum@321")).text
    if response:
        root = ET.fromstring(response)
        res = []
        # Find the list of elements
        streamingTransport = root.findall(".//{http://www.isapi.org/ver20/XMLSchema}streamingTransport")
        videoCodecType = root.findall(".//{http://www.isapi.org/ver20/XMLSchema}videoCodecType")
        videoResolutionWidth = root.findall(".//{http://www.isapi.org/ver20/XMLSchema}videoResolutionWidth")
        videoResolutionHeight = root.findall(".//{http://www.isapi.org/ver20/XMLSchema}videoResolutionHeight")
        videoQualityControlType = root.findall(".//{http://www.isapi.org/ver20/XMLSchema}videoQualityControlType")
        # Extract elements in list
        streamingTransport_list = [item.text for item in streamingTransport]
        videoCodecType_list = [item.text for item in videoCodecType]
        videoResolutionWidth_list = [item.text for item in videoResolutionWidth]
        videoResolutionHeight_list = [item.text for item in videoResolutionHeight]
        videoQualityControlType_list = [item.text for item in videoQualityControlType]

        for i in range(len(streamingTransport_list)):
            res.append({ "cam " + str(i + 1) :
            {
                "streamingTransport": streamingTransport_list[i],
                "videoCodecType": videoCodecType_list[i],
                "videoResolutionWidth": videoResolutionWidth_list[i],
                "videoResolutionHeight": videoResolutionHeight_list[i],
                "videoQualityControlType": videoQualityControlType_list[i]
            }})
        print(res)
        return res

