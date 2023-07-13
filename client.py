import requests


header = {
    'Content-Type': "application/json"
}

body = '''{
    "type": 1,
    "data": {
        "id": 295,
        "bo": 90,
        "thalach": 115,
        "lo": "school"
    }
}'''

url = "http://a7c389ffc8a04661ae26a6671e343d2f.apig.cn-north-4.huaweicloudapis.com/fg/invoke"
# curl -X POST -H 'Content-Type: application/json' -d '{"type":1,"data":{"id":295,"bo":90,"thalach":115,"lo":"school"}}' http://a7c389ffc8a04661ae26a6671e343d2f.apig.cn-north-4.huaweicloudapis.com/fg/invoke
respone = requests.post(url, data=body, headers=header)

print(respone.json())