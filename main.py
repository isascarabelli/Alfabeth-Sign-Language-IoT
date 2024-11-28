import cv2
import urllib.request
import numpy as np
import time
import paho.mqtt.client as mqtt
from inference_sdk import InferenceHTTPClient

## Broker Configuratios
BROKER = "test.mosquitto.org"           # Broker
PORT = 1883                             # Port MQTT
TOPIC1 = "signalLang/topic/sending1"    # Topic1 to subscribe
TOPIC2 = "signalLang/topic/sending2"    # Topic2 to subscribe

## URL with the IP camera's stream URL
url = 'http://192.168.0.17/cam-mid.jpg'

##Broker -----------------------------------------------------
# Creating MQTT client
client = mqtt.Client()

# Connecting to the broker
client.connect(BROKER, PORT, keepalive=60)

# Function to connect with the broker
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker com código:", rc)
    client.subscribe(TOPIC1)  # Subscribe on the topic1
    client.subscribe(TOPIC2)  # Subscribe on the topic2


# Associating callback functions
client.on_connect = on_connect

# ----------------------------------------------------------------
## Create a VideoCapture object
cap = cv2.VideoCapture(url)

## Check if the IP camera stream is opened successfully
if not cap.isOpened():
    print("Failed to open the IP camera stream")
    exit()

## Read and display video frames
while True:
    time.sleep(1)  # Pausa de segundo
    # Read a frame from the video stream
    img_resp=urllib.request.urlopen(url)
    img_jpg = img_resp.read()
    imgnp=np.array(bytearray(img_jpg),dtype=np.uint8)
    ret, frame = cap.read()
    im = cv2.imdecode(imgnp,-1)

    print(frame)

    cv2.imshow('live Cam Testing',im)
    key=cv2.waitKey(5)
    if key==ord('q'):
        break
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="NoRG4HIyuhZtYstoEPtE"
    )

    result = CLIENT.infer(url, model_id="american-sign-language-letters/6")
    print(result)
    print("Letra: ")

    # Verificar se há itens na lista predictions
    predictions = result.get("predictions", [])
    if result['predictions']:
        max_index = len(predictions) - 1

        if max_index == 0:
            letter = result['predictions'][0]['class']
            print(letter)
            client.publish(TOPIC1, letter)
            client.publish(TOPIC2, letter)
        elif max_index >= 1:
            letter = result['predictions'][0]['class']
            print(letter)
            letter1 = result['predictions'][1]['class']
            print(letter1)
            client.publish(TOPIC1, letter)
            client.publish(TOPIC2, letter1)
    else:
        client.publish(TOPIC1, " - ")
        client.publish(TOPIC2, " - ")
cap.release()
cv2.destroyAllWindows()
