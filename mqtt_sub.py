import paho.mqtt.client as mqtt

broker = 'f292611f33.st1.iotda-app.cn-north-4.myhuaweicloud.com'
port = 8883
topic = "/python/mqtt"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
# client.connect("broker.hivemq.com", 1883, 60)

client.loop_forever()