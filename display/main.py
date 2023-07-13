from flask import Flask, render_template, request
import asyncio
import websockets
import threading
import copy
import json


ws_port = 12345
diagnose = None
connected = False


async def ws_handler(websocket, path):
    print("a new conncetion connected")
    global connected
    connected = True

    while True:
        event.wait()
        print("get data from main flask thread")
        data = copy.deepcopy(diagnose)
        event.clear()

        print("start to send data to client...")
        print("data:", data)
        await websocket.send(data)
        print("send data to client finished")

    # name = await websocket.recv()
    # print(f"< {name}")

    # greeting = f"Hello {name}!"

    # await websocket.send(greeting)
    # print(f"> {greeting}")

async def start_server():
    print("start server...")
    server = websockets.serve(ws_handler, "0.0.0.0", ws_port)
    print("start server finished")
    await server


def ws_srv():
    print("start to send msg to frontend...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # start_server = websockets.serve(hello, 'localhost', 33342)
    loop.run_until_complete(start_server())
    loop.run_forever()


app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    data_str = '''
        {
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
    global diagnose 
    while event.is_set() == True:
        continue
    diagnose = data_str
    # inform the other thread
    event.set()
    # return 'Hello, World!'
    # data = request.get_json()
    return render_template('index.html')


@app.route('/user', methods=['POST'])
def recv_message():

    data = request.get_json()
    data_str = json.dumps(data)
    if connected == False:
        return
    global diagnose 
    while event.is_set() == True:
        continue
    diagnose = data_str
    # inform the other thread
    event.set()

    # level = data['level']
    # conlusions = data['text']
    # loc = data['location']
    # return render_template('index.html', level=level, conclusions=conlusions, loc=loc)


if __name__ == "__main__":

    event = threading.Event()

    ws = threading.Thread(target=ws_srv)
    ws.start()

    app.run(host="0.0.0.0", debug=False, port=8080)

    ws.join()
