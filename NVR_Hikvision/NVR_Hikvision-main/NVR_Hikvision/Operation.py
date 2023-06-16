data='''<?xml version="1.0" encoding="UTF-8" ?>
<CMSearchResult version="1.0" xmlns="http://www.hikvision.com/ver20/XMLSchema">
<searchID>{484a3530-3939-3239-3038-240f9b2d60ab}</searchID>
<responseStatus>true</responseStatus>
<responseStatusStrg>MORE</responseStatusStrg>
<numOfMatches>2</numOfMatches>
<matchList>
<searchMatchItem>
<logDescriptor>
<metaId>log.hikvision.com/Operation/remoteDisArm</metaId>
<StartDateTime>2023-05-01T12:50:38Z</StartDateTime>
<paraType></paraType>
<userName>admin</userName>
<ipAddress>172.16.0.1</ipAddress>
</logDescriptor>
</searchMatchItem>
<searchMatchItem>
<logDescriptor>
<metaId>log.hikvision.com/Operation/remoteDisArm</metaId>
<StartDateTime>2023-05-01T12:50:38Z</StartDateTime>
<paraType></paraType>
<userName>admin</userName>
<ipAddress>172.16.0.1</ipAddress>
</logDescriptor>
</searchMatchItem>
</matchList>
</CMSearchResult>'''

new_data=data[40:]
# print(new_data)
# print(type(new_data))
import xml.etree.ElementTree as ET
root = ET.fromstring(new_data) #data
# print(root.tag)
# print(root[4][0][0][1].text)
# print(root[4][0][0][0].text)
# print(root[4])

for childs in root:  #country
     for child in childs:
         for lop1 in child:
             lst=[]
             for lop2 in lop1:
                # print(lop2.text)
                # print(lop2.tag)
                if lop2.tag=="{http://www.hikvision.com/ver20/XMLSchema}metaId":
                    lst.append(lop2.text)
                    # print(lop2.text)
                if lop2.tag=="{http://www.hikvision.com/ver20/XMLSchema}StartDateTime":
                    lst.append(lop2.text)
                    # print(lop2.text)
                if lop2.tag=="{http://www.hikvision.com/ver20/XMLSchema}userName":
                    lst.append(lop2.text)
                    # print(lop2.text)
                if lop2.tag=="{http://www.hikvision.com/ver20/XMLSchema}ipAddress":
                    lst.append(lop2.text)
                    # print(lop2.text)
             print(lst)
