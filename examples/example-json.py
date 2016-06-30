import json
import requests
import time

def print_dict(v):
    if isinstance(v, dict):
        for a,b in v.items():
            if a in ('info','path','request','headers','cookie'):
                print a,print_dict(b)
    else:
        print v


response = requests.get('http://127.0.0.1/trace')
response = json.loads(response.content)
for info in response:
    print_dict(info)

'''

'''