import requests

url = "https://partner.hanet.ai/person/takeFacePicture"

payload={
  'token':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI0MDg1NzAwODAyMDkwMjcwNzIiLCJlbWFpbCI6InR1bmd1eWVuZGVsZXRlckBnbWFpbC5jb20iLCJjbGllbnRfaWQiOiJkMWY4YmZlNjY2YTg0NmFkMTdkMTU3OWExMDEyZWI2NyIsInR5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJpYXQiOjE2ODExODM4ODUsImV4cCI6MTcxMjcxOTg4NX0.m3uSqnSrQ2LJNlYMZqOSDn5eCMmNm0vaf-6CCB8zYbA',
  'deviceID':'H2246HV0129'
}
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
