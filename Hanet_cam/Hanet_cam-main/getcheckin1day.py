import requests
import json

url = "https://partner.hanet.ai/person/getCheckinByPlaceIdInDay"

day=int(input("Ngày bạn muốn check thông tin : "))
mon=int(input("Tháng bạn muốn check thông tin : "))
year=int(input("Năm bạn muốn lấy thông tin check in : "))
num=int(input("Số lượng bạn cần check : "))
type_people=int(input("0: nhân viên, 1: khách hàng, 2: người lạ : "))

if day<10:
    day=f'0{day}'
if mon<11:
    mon=f'0{mon}'
date=f'{year}-{mon}-{day}'

payload={'token':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI0MDg1NzAwODAyMDkwMjcwNzIiLCJlbWFpbCI6InR1bmd1eWVuZGVsZXRlckBnbWFpbC5jb20iLCJjbGllbnRfaWQiOiJkMWY4YmZlNjY2YTg0NmFkMTdkMTU3OWExMDEyZWI2NyIsInR5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJpYXQiOjE2ODExMTUxMzUsImV4cCI6MTcxMjY1MTEzNX0.X4cxio46ySWsmMbLm3aFaq4d3jUNztBbXbmHoAsc0QE',
        'placeID':'16653',
        'date':'2023-04-10',
        'exType':'',
        'devices':'H2246HV0129' ,
        'exDevices':'',
        'type':'' ,
        'aliasID':'' ,
        'personID':'',
        'personIDs':'',
        'aliasIDs':'' ,
        'page':'1' ,
        'size':'100'
}

payload['date']=date
payload['size']=num

if type_people==0:
        payload['type']='0'
elif type_people==1:
        payload['type']='1'
elif type_people==2:
        payload['type']=''

headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload).text
respone_text=json.loads(response)
if respone_text['data']== None :
        print(f"Chưa có dữ liệu check in vào ngày {date}")
else:
        print(respone_text)
#print(type(response))
#print(type(respone_text))
