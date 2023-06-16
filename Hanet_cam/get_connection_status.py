import requests

url = "https://partner.hanet.ai/device/getConnectionStatus"

payload={'token':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI0MDg1NzAwODAyMDkwMjcwNzIiLCJlbWFpbCI6InR1bmd1eWVuZGVsZXRlckBnbWFpbC5jb20iLCJjbGllbnRfaWQiOiJkMWY4YmZlNjY2YTg0NmFkMTdkMTU3OWExMDEyZWI2NyIsInR5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJpYXQiOjE2ODExMTg1MDUsImV4cCI6MTcxMjY1NDUwNX0.fB8hXeLYpiCGZmlC60PIenE2_jfLoGr3QxeBLyyowkM',
        "deviceID":"H2246HV0129"
         }
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
