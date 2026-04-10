import urllib.request
import urllib.parse
import json

data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin', 'grant_type': 'password'}).encode('ascii')
req = urllib.request.Request('http://127.0.0.1:8000/api/auth/login', data=data)
try:
    with urllib.request.urlopen(req) as response:
        print("SUCCESS:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code)
    print("REASON:", e.read().decode('utf-8'))
except Exception as e:
    print("OTHER ERROR:", e)
