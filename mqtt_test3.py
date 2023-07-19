import paho.mqtt.client as mqtt
import threading
import time

topic = "testtopic"
broker = 'broker.emqx.io'
port = 1883

# 连接成功回调
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe(topic)

# 消息接收回调
def on_message(client, userdata, msg):
    print("Recv msg", msg.topic+" "+str(msg.payload))


def subscribe():
    print("Start to subscribe...")
    # sub_client = mqtt.Client()
    # # 指定回调函数
    # sub_client.on_connect = on_connect
    # sub_client.on_message = on_message

    # # 建立连接
    # print("Start to connect...")
    # sub_client.connect(broker, port, 60)

    sub_client.loop_forever()


def publish():
    # sub_client = mqtt.Client()
    # sub_client.connect(broker, port, 60)
    # 发布消息
    while True:
        sub_client.publish(topic,payload='Hello World',qos=0)
        print("Publish msg")
        time.sleep(3)


sub_client = mqtt.Client()
# 指定回调函数
sub_client.on_connect = on_connect
sub_client.on_message = on_message

# 建立连接
print("Start to connect...")
sub_client.connect(broker, port, 60)

t = threading.Thread(target=subscribe)
t.start()
publish()
t.join()