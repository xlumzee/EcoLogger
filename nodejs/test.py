import requests

url = "http://10.150.241.8:5000/"
headers = {"Content-Type": "application/json"}
data = {"Time": "12:00", "Temperature": "22.2"}

response = requests.post(url, json=data, headers=headers)
#response = requests.get("https://google.com"/)
print(response.status_code)
print(response.text)