from vosk import Model, KaldiRecognizer
import pyaudio
import json
import pyttsx3
import time
import paho.mqtt.client as paho
import sys

# Load model
model_path = "/home/somi/Documents/Vosk Stt/vosk-model-small-en-us-0.15"
model = Model(model_path)

# Keyword mode
keywords = '["light","fan","pc","speaker","main led","side led","soldering iron","raspberry pi","turn","on","off","camera","sleep","exit","wake up","outdoor","bathroom","siri"]'
recognizer = KaldiRecognizer(model, 16000, keywords)

# Initialize mic and TTS
mic = pyaudio.PyAudio()
engine = pyttsx3.init()

# Mqtt protocol parameters
client = paho.Client(paho.CallbackAPIVersion.VERSION2)
bedroom_controlTopic = ""
bedroom_statusTopic = ""
 
outside_controlTopic = ""
outside_statusTopic = ""

work_controlTopic = ""
work_statusTopic = ""


mqttServer = "broker.mqtt.cool"

def onMessage(client, userdata, msg):
    print(msg.topic + ": " + str(msg.payload.decode("utf-8")))

def mqtt_publish(command,topic):
    if client.connect(mqttServer,1883, 60) != 0:
        print("could not connect to MQTT Broker!")
        sys.exit(-1)
    
    client.publish(topic,command,0)
    time.sleep(1)

def mqtt_subscribe(time_in_sec):
    if client.connect(mqttServer,1883, 60) != 0:
        print("could not connect to MQTT Broker!")
        sys.exit(-1)
        
    client.loop_start()
    client.subscribe(bedroom_statusTopic)
    client.on_message = onMessage
    time.sleep(time_in_sec)
    client.loop_stop()



def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def get_command(timeout=120):
    stream = mic.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=16000,
                      input=True,
                      frames_per_buffer=4096)
    stream.start_stream()

    print("Listening...")
    start_time = time.time()

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            command = result_dict.get("text", "")
            stream.stop_stream()
            stream.close()
            return command.strip()
        elif time.time() - start_time > timeout:
            stream.stop_stream()
            stream.close()
            return None

# Main assistant loop
active = True

while True:
    if active:
        print("\n[Active Mode] Waiting for command...")
        command = get_command(timeout=120)  # 2 minute timeout

        if command is None:
            speak("No activity. Going to sleep.")
            active = False
            continue

        if "sleep" in command:
            speak("Going to sleep.")
            active = False
        elif "exit" in command:
            speak("Goodbye!")
            break
        else:
            # Process command here
            speak(f"You said: {command}")
            
            if "turn on light" in command or "light on" in command:
                speak("Turning on the light.")
                mqtt_publish("relay1_on", bedroom_controlTopic)

            elif "turn off light" in command or "light off" in command:
                speak("Turning off the light.")
                mqtt_publish("relay1_off", bedroom_controlTopic)

            elif "turn on fan" in command or "fan on" in command:
                speak("Turning on the fan.")
                mqtt_publish("relay4_on", bedroom_controlTopic)

            elif "turn off fan" in command or "fan off" in command:
                speak("Turning off the fan.")
                mqtt_publish("relay4_off", bedroom_controlTopic)

            elif "turn on pc" in command or "pc on" in command:
                speak("Turning on the PC.")
                mqtt_publish("relay2_on", work_controlTopic)

            elif "turn off pc" in command or "pc off" in command:
                speak("I don't have permission to turn off the pc")

            elif "turn on speaker" in command or "speaker on" in command:
                speak("Turning on the speaker.")
                mqtt_publish("relay1_on", work_controlTopic)

            elif "turn off speaker" in command or "speaker off" in command:
                speak("Turning off the speaker.")
                mqtt_publish("relay1_off", work_controlTopic)

            elif "turn on main led" in command or "main led on" in command:
                speak("Turning on the main LED.")
                mqtt_publish("relay4_on", work_controlTopic)

            elif "turn off main led" in command or "main led off" in command:
                speak("Turning off the main LED.")
                mqtt_publish("relay4_off", work_controlTopic)

            elif "turn on side led" in command or "side led on" in command:
                speak("Turning on the side LED.")
                mqtt_publish("relay2_on", bedroom_controlTopic)

            elif "turn off side led" in command or "side led off" in command:
                speak("Turning off the side LED.")
                mqtt_publish("relay2_off", bedroom_controlTopic)

            elif "turn on soldering iron" in command or "soldering iron on" in command:
                speak("Turning on the soldering iron.")
                mqtt_publish("relay3_on", work_controlTopic)

            elif "turn off soldering iron" in command or "soldering iron off" in command:
                speak("Turning off the soldering iron.")
                mqtt_publish("relay3_off", work_controlTopic)

            elif "turn on raspberry pi" in command or "raspberry pi on" in command:
                speak("Turning on the Raspberry Pi.")
                mqtt_publish("relay5_on", work_controlTopic)

            elif "turn off raspberry pi" in command or "raspberry pi off" in command:
                speak("I don't have permission to Turn off the Raspberry Pi")

            elif "turn on camera" in command or "camera on" in command:
                speak("Turning on the camera.")
                mqtt_publish("relay4_on", outside_controlTopic)

            elif "turn off camera" in command or "camera off" in command:
                speak("Turning off the camera.")
                mqtt_publish("relay4_off", outside_controlTopic)

            elif "turn on outdoor light" in command or "outdoor light on" in command:
                speak("Turning on the outdoor light.")
                mqtt_publish("relay2_on", outside_controlTopic)

            elif "turn off outdoor light" in command or "outdoor light off" in command:
                speak("Turning off the outdoor light.")
                mqtt_publish("relay2_off", outside_controlTopic)

            elif "turn on bathroom light" in command or "bathroom light on" in command:
                speak("Turning on the bathroom light.")
                mqtt_publish("relay3_on", outside_controlTopic)

            elif "turn off bathroom light" in command or "bathroom light off" in command:
                speak("Turning off the bathroom light.")
                mqtt_publish("relay3_off", outside_controlTopic)

            elif "turn on siri light" in command or "siri light on" in command:
                speak("Turning on the Siri light.")
                mqtt_publish("relay1_on", outside_controlTopic)

            elif "turn off siri light" in command or "siri light off" in command:
                speak("Turning off the Siri light.")
                mqtt_publish("relay1_off", outside_controlTopic)

    else:
        print("\n[Sleep Mode] Listening for wake word...")
        command = get_command(timeout=0)  # infinite listen

        if command and "wake up" in command:
            speak("I'm awake.")
            active = True
