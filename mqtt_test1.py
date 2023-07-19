import paho.mqtt.client as mqtt


topic = "testtopic"
# 连接成功回调
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe(topic)

# 消息接收回调
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()

# 指定回调函数
client.on_connect = on_connect
client.on_message = on_message

# 建立连接
client.connect('broker.emqx.io', 1883, 60)
# 发布消息
client.publish(topic,payload='Hello World',qos=0)

# client.loop_forever()