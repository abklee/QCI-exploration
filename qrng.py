import requests
json_data = {
"access_token": f"",
}
headers = {
"accept": "application/json",
"Content-Type": "application/json",
}
response=requests.post(
f"https://api.qci-next.com/authorize",
headers=headers,
json=json_data)
response_json = response.json()
print(response_json)
print(response.status_code)
access_token = response.json().get("access_token")
print(access_token)
