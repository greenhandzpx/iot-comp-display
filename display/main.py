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
                "will die",
                "bpm exception",
                "I'm sorry"
            ],
            "advice": [
                "study",
                "play",
                "sleep"
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
    # return 'Hello, World!'
    # data = request.get_json()
    return render_template('index.html')


@app.route('/user', methods=['POST'])
def recv_from_user():

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
