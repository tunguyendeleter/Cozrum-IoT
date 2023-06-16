import requests
from requests.auth import HTTPDigestAuth
import json

def record_video_log(cam,year_start,month_start,day_start,hour_start,min_start,sec_start,year_end,month_end,day_end,hour_end,min_end,sec_end,sum_result):
    lst_dict=[]
    url = "http://172.16.0.2/ISAPI/ContentMgmt/Search"
    start_time=str(year_start) + "-" +str(month_start) +'-'+ str(day_start) + "T" + str(hour_start) + ':' + str(min_start) + ':' + str(sec_start) + "Z"
    end_time=str(year_end) + "-" +str(month_end) +'-'+ str(day_end) + "T" + str(hour_end) + ':' + str(min_end) + ':' + str(sec_end) + "Z"
    print(start_time)
    print(end_time)
    if cam==1:
      track_id=101
    elif cam==2:
      track_id=201
    elif cam==3:
      track_id=301
    elif cam==4:
      track_id=401
    elif cam==5:
      track_id=501
    elif cam==6:
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
    # print(response)

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
            my_dict={"Cam":lst[0],
                     "Start_time":lst[1],
                     "End_time":lst[2],
                     "url":lst[3]
                     }
            # print(lst)
            # print(my_dict)
            lst_dict.append(my_dict)
    return lst_dict.json
a=record_video_log(1,2023,5,19,0,0,0,2023,5,19,23,59,59,10)
print(a)