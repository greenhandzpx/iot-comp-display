import random
from paho.mqtt import client as mqtt_client

broker = 'f292611f33.st1.iotda-app.cn-north-4.myhuaweicloud.com'
port = 5671
topic = "hello"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'


# def connect_mqtt():
#     def on_connect(client, userdata, flags, rc):
#         if rc == 0:
#             print("Connected to MQTT Broker!")
#         else:
#             print("Failed to connect, return code %d\n", rc)

#     client = mqtt_client.Client(client_id)
#     client.on_connect = on_connect
#     client.connect(broker, port)
#     return client


# def publish(client):
#     msg_count = 0
#     while True:
#         # time.sleep(1)
#         msg = f"messages: {msg_count}"
#         result = client.publish(topic, msg)
#         # result: [0, 1]
#         status = result[0]
#         if status == 0:
#             print(f"Send `{msg}` to topic `{topic}`")
#         else:
#             print(f"Failed to send message to topic {topic}")
#         msg_count += 1
#         break


# def run():
#     client = connect_mqtt()
#     client.loop_start()
#     publish(client)

# if __name__ == '__main__':
#     run()

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.publish(topic, "Wowwwwwwwwwwwwww")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)
# client.connect(broker, port, 60)
client.loop_forever()

# client.publish("test/topic", "Hello, World!")