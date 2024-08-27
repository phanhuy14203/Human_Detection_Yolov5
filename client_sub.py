import os
import cv2
from datetime import datetime
from paho.mqtt.client import Client
import numpy as np
import base64

broker = '192.168.216.54'  # Địa chỉ IP của broker
port = 1883
now = datetime.now()
year, month, day = str(now.year), str(now.month), str(now.day)
topic_today = day + "-" + month + "-" + year

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload
    print(topic)
    image_data = base64.b64decode(payload)
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    global year,month,day,hour,minute,second,now
    now = datetime.now()
    year, month, day, hour, minute, second = (
        str(now.year),
        str(now.month),
        str(now.day),
        str(now.hour),
        str(now.minute),
        str(now.second),
    )
    file_path = ".\\receive" 
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_path += "\\" + day + "-" + month + "-" + year 
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    image_name = (
        file_path
        + "\\"
        + hour
        + "h"
        + minute
        + "m"
        + second
        + "s "
        + ".jpg"
    )
    is_saved = cv2.imwrite(image_name, img)
    if is_saved:
        print("ảnh đã được lưu")
    else:
        print("ERROR")
def subscribe(client: Client):
    global topic_today
    topic_today = day + "-" + month + "-" + year
    client.subscribe("detected/"+topic_today+"/#")
    client.on_message = on_message
def connect_mqtt() -> Client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    username = "nhom10"  
    password = "12345"
    client = Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
if __name__ == '__main__':
    run()