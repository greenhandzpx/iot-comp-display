from flask import Flask, render_template, request
import asyncio
import websockets
import threading
import copy
import json


ws_port1 = 12345
ws_port2 = 12346
USER_DIAGNOSE = None
HOSPITAL_DIAGNOSE = None
connected = False

STATE = 0
LOCK = threading.Lock()
USER_EVENT = threading.Event()
HOSPITAL_EVENT = threading.Event()


async def ws_handler(websocket, path):
    print("a new conncetion connected")
    global connected
    connected = True

    global USER_EVENT
    global USER_DIAGNOSE
    global HOSPITAL_EVENT
    global HOSPITAL_DIAGNOSE

    # LOCK.acquire()
    # global STATE
    # if STATE == 0:
    #     id = 0
    #     STATE = 1
    # else:
    #     id = 1
    # LOCK.release()

    client_type = await websocket.recv()
    print("handle a conn, client type", client_type)

    while True:
        # if id == 0:
        #     e = USER_EVENT
        # else:
        #     e = HOSPITAL_EVENT
        if client_type == "user":
            e = USER_EVENT
        else:
            e = HOSPITAL_EVENT
        print("wait for data...")
        e.wait()
        # if id == 0:
        #     print("user get data from main flask thread")
        #     diagnose = USER_DIAGNOSE
        # else:
        #     print("hospital get data from main flask thread")
        #     diagnose = HOSPITAL_DIAGNOSE
        if client_type == "user":
            print("user get data from main flask thread")
            diagnose = USER_DIAGNOSE
        else:
            print("hospital get data from main flask thread")
            diagnose = HOSPITAL_DIAGNOSE

        data = copy.deepcopy(diagnose)
        # data = copy.deepcopy(diagnose)
        e.clear()

        print("start to send data to client...")
        print("data:", data)
        await websocket.send(data)
        print("send data to client finished")

    # name = await websocket.recv()
    # print(f"< {name}")

    # greeting = f"Hello {name}!"

    # await websocket.send(greeting)
    # print(f"> {greeting}")

async def start_server(port):
    print("start server...")
    server = websockets.serve(ws_handler, "0.0.0.0", port)
    print("start server finished")
    await server


def ws_srv1():
    print("ws_srv1:start to send msg to frontend...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # start_server = websockets.serve(hello, 'localhost', 33342)
    loop.run_until_complete(start_server(ws_port1))
    loop.run_forever()

def ws_srv2():
    print("ws_srv2:start to send msg to frontend...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # start_server = websockets.serve(hello, 'localhost', 33342)
    loop.run_until_complete(start_server(ws_port2))
    loop.run_forever()



app = Flask(__name__)

@app.route('/get_hos', methods=['GET'])
def get_hos():
    data_str = '''
        {
            "hospital_name": "南方科技大学附属医院",
            "hospital_phone_number": 114514,
            "patient_info": {
                "level": 4,
                "text": [
                    "该人存在某些身体状况或健康问题。正常血氧饱和度应该在95％到100％之间，而正常心率通常在每分钟60到100次之间。如果血氧低于95％，心率高于100次/分钟，这可能表明有些问题。这些症状可能是氧气不足或其他疾病或情况的结果，例如COVID-19感染、肺炎、贫血、气道疾病以及心血管疾病等，需要进一步的检查来确定原因并接受适当的治疗"
                ],
                "location": "学校"
            }
        }
    '''
    if connected == False:
        return
    global HOSPITAL_DIAGNOSE
    while HOSPITAL_EVENT.is_set() == True:
        continue
    HOSPITAL_DIAGNOSE = data_str
    print("HOSPITAL DIAGNOSE:", HOSPITAL_DIAGNOSE)
    # inform the other thread
    HOSPITAL_EVENT.set()
    # return 'Hello, World!'
    # data = request.get_json()
    return render_template('index.html')



@app.route('/', methods=['GET'])
def hello_world():
    data_str = '''
        {
            "data": {
                "bpm": 78,
                "bo": 96
            },
            "level": 3,
            "location": "学校",
            "text": [
                "该人存在某些身体状况或健康问题。正常血氧饱和度应该在95％到100％之间，而正常心率通常在每分钟60到100次之间。如果血氧低于95％，心率高于100次/分钟，这可能表明有些问题。这些症状可能是氧气不足或其他疾病或情况的结果，例如COVID-19感染、肺炎、贫血、气道疾病以及心血管疾病等，需要进一步的检查来确定原因并接受适当的治疗"
            ],
            "advice": [
    "让患者放松和休息。通风良好的环境下呼吸新鲜空气。如果患者在户外，请尽可能前往海拔较低的地方。检查患者是否有慢性呼吸道疾病。确保患者足够饮水，以避免脱水引起的心率偏高。如果患者佩戴可穿戴设备并检测到血氧饱和度低，请咨询医生是否需要进一步评估。"
            ]
        }
    '''
    if connected == False:
        return
    global USER_DIAGNOSE
    while USER_EVENT.is_set() == True:
        continue
    USER_DIAGNOSE = data_str
    print("USER DIAGNOSE:", USER_DIAGNOSE)
    # inform the other thread
    USER_EVENT.set()

    hos_data_str = '''
        {
            "hospital_name": "南方科技大学医院",
            "hospital_phone_number": "114514",
            "patient_info": {
                "level": "3",
                "text": ["建议患者进行定期检查，以规避心脏疾病的风险"],
                "location": "home"
            }
        }
    '''
    print("hospital data str", hos_data_str)

    global HOSPITAL_DIAGNOSE
    while HOSPITAL_EVENT.is_set() == True:
        continue
    HOSPITAL_DIAGNOSE = hos_data_str
    HOSPITAL_EVENT.set()

    return render_template('index.html')


@app.route('/user', methods=['POST'])
def recv_from_user():

    print("recv data from /user")
    data = request.get_json()
    data_str = json.dumps(data)
    if connected == False:
        return
    global USER_DIAGNOSE 
    while USER_EVENT.is_set() == True:
        continue
    USER_DIAGNOSE = data_str
    # inform the other thread
    USER_EVENT.set()
    return render_template('index.html')

@app.route('/hospital', methods=['POST'])
def recv_from_hospital():

    print("recv data from /hospital")
    data = request.get_json()
    data_str = json.dumps(data)
    if connected == False:
        return
    global HOSPITAL_DIAGNOSE 
    while HOSPITAL_EVENT.is_set() == True:
        continue
    HOSPITAL_DIAGNOSE = data_str
    # inform the other thread
    HOSPITAL_EVENT.set()
    return render_template('index.html')


if __name__ == "__main__":

    ws1 = threading.Thread(target=ws_srv1)
    ws2 = threading.Thread(target=ws_srv2)
    ws1.start()
    ws2.start()

    app.run(host="0.0.0.0", debug=False, port=8080)

    ws1.join()
    ws2.join()
