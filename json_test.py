import json

json_str = '''
    {
        "home": "hhh",
        "name": "ddd"
    }
'''


data = json.loads(json_str)
print(data)