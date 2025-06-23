
import requests
import paho.mqtt.client as paho
import sys
import time
import ast


WLED_IP = "192.168.1.5"
BACK_WLED_IP = "192.168.1.6"

SEGMENT_MAP = {
    "front almary": 1,
    "behind the money plant": 2,
    "ceiling": 3,
    "under laptop table": 4,
    "under pc table": 5,
    "ganesha almary": 6,
    "shiva almary": 7,
    "all":8,
    "back almary": 9
}

class HomeController:
    def __init__(self, mqtt_server="broker.mqtt.cool"):
        self.client = paho.Client(paho.CallbackAPIVersion.VERSION2)
        self.mqtt_server = mqtt_server

        self.topic_map = {
            "bedroom": "your_mqtt_topic",
            "outside": "your_mqtt_topic",
            "work": "your_mqtt_topic"
        }

        self.device_relay_map = {
            "bedroom light":     ("bedroom", "relay1"),
            "bedroom fan":       ("bedroom", "relay4"),
            "bedroom bulb":      ("bedroom", "relay3"),
            "side led":          ("bedroom", "relay2"),

            "bathroom light":    ("outside", "relay3"),
            "siri light":        ("outside", "relay1"),  # stair light
            "outdoor light":     ("outside", "relay2"),
            "outdoor camera":    ("outside", "relay4"),

            "home theater":      ("work", "relay1"),
            "pc":                ("work", "relay2"),
            "soldering iron":    ("work", "relay3"),
            "main led":          ("work", "relay4"),
            "raspberry pi":      ("work", "relay5")
        }

        self.blocked_off = {"pc", "raspberry pi"}

    def mqtt_publish(self, command, topic):
        if self.client.connect(self.mqtt_server, 1883, 60) != 0:
            print("Could not connect to MQTT Broker!")
            sys.exit(-1)
        self.client.publish(topic, command, 0)
        time.sleep(1)

    def control_device(self, controlled_device, controlled_state):
        if controlled_device not in self.device_relay_map:
            print(f"Unknown device: {controlled_device}")
            return

        topic_key, relay_id = self.device_relay_map[controlled_device]
        topic = self.topic_map[topic_key]

        # Handle special case: restricted OFF permission
        if controlled_state == "off" and controlled_device in self.blocked_off:
            print(f"I don't have permission to turn off {controlled_device.title()}!")
            return

        command = f"{relay_id}_{controlled_state}"
        self.mqtt_publish(command, topic)
        print(f"Turned {controlled_state} {controlled_device}")

class LEDStripController:
    def set_led_segment(self, segment_name, rgb_colour_code, brightness_value=255):
        segment_id = SEGMENT_MAP.get(segment_name.lower())
        if isinstance(rgb_colour_code, str):
            try:
                rgb_colour_code = ast.literal_eval(rgb_colour_code)
            except Exception as e:
                print("❌ Invalid string format for RGB. Expected a list like '[255, 0, 0]'.")
                rgb_colour_code = [0,0,0]
        if segment_id is None:
            print(f"❌ Unknown segment: {segment_name}")
            return

        payload = {
            "on": True,
            "bri": 210,
            "ps": -1,
            "seg": []
        }

        if segment_id == 8:  # 'all'
            for name, sid in SEGMENT_MAP.items():
                if sid == 8 or sid == 9:
                    continue  # skip the 'all' alias
                payload["seg"].append({
                    "id": sid,
                    "col": [rgb_colour_code, [0, 0, 0], [0, 0, 0]],
                    "bri": brightness_value
                })
            self.send_wled_request(payload,WLED_IP)
            payload2 = {
            "on": True,
            "bri": brightness_value,
            "seg": [{
                "id": 0,
                "col": [rgb_colour_code, [0, 0, 0], [0, 0, 0]],
            }]}
            self.send_wled_request(payload2,BACK_WLED_IP)
            print("🎨 Applying color to ALL segments.")

        elif segment_id == 9:
            payload = {
            "on": True,
            "bri": brightness_value,
            "seg": [{
                "id": 0,
                "col": [rgb_colour_code, [0, 0, 0], [0, 0, 0]],
            }]}
            self.send_wled_request(payload,BACK_WLED_IP)

        else:
            payload["seg"].append({
                "id": segment_id,
                "col": [rgb_colour_code, [0, 0, 0], [0, 0, 0]],
                "bri": brightness_value
            })
            print(f"🎯 Applying color to segment: {segment_name} (ID: {segment_id})")
            self.send_wled_request(payload,WLED_IP)
            
    def set_segment_mode(self,strip_mode):
        if strip_mode == "musicSync":
            payload = {
            "on": True,
            "bri": 200,
            "ps": -1,
            "seg": [{
                "id": 0,
                "on": True,
                "bri": 255,
                "col": [[255, 255, 255], [0, 0, 0], [0, 0, 0]],
                "fx": 165,
                "sx": 101,
                "ix": 148,
                "pal": 72
            }]
        }
        elif strip_mode == "workMode":
            payload = {
                "on": True,
                "bri": 200,
                "ps": 3
            }
        elif strip_mode == "shootingMode":
            payload = {
                "on": True,
                "bri": 200,
                "ps": 5
            }

        self.send_wled_request(payload,WLED_IP)

    def send_wled_request(self, payload, IP):
        url = f"http://{IP}/json/state"
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print("✅ WLED command sent successfully.")
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to send WLED command: {e}")

class CommandExecutor:
    def __init__(self):
        self.home_controller = HomeController()
        self.led_controller = LEDStripController()

        self.function_map = {
            "homeControl": self.execute_home_control,
            "setLedStripSegment": self.execute_set_led_strip,
            "setLedStripMode": self.execute_led_strip_mode
        }

    def execute(self, actions: list):
        for action_obj in actions:
            function_name = action_obj.get("functionName")
            arguments = action_obj.get("arguments", {})

            handler = self.function_map.get(function_name)
            if handler:
                handler(arguments)
            else:
                print(f"No handler found for function: {function_name}")

    def execute_home_control(self, args: dict):
        formatted_args = {
            "controlled_device": args["controlledDevice"],
            "controlled_state": args["controlledState"]
        }
        self.home_controller.control_device(**formatted_args)

    def execute_set_led_strip(self, args: dict):
        formatted_args = {
            "segment_name": args["segmentName"],
            "rgb_colour_code": args["rgbColourCode"],
            "brightness_value": args["brightnessValue"]
        }
        self.led_controller.set_led_segment(**formatted_args)

    def execute_led_strip_mode(self, args: dict):
        formatted_args = {
            "strip_mode": args["stripMode"]
        }
        self.led_controller.set_segment_mode(**formatted_args)




# rgb_colour_code = [255,0,255]
# payload = {
#             "on": True,
#             "bri": 155,
#             "seg": [{
#                 "id": 0,
#                 "col": [rgb_colour_code, [0, 0, 0], [0, 0, 0]],
#             }]}


# url = f"http://{BACK_WLED_IP}/json/state"
# response = requests.post(url, json=payload)

# state = requests.get(f"http://{WLED_IP}/json/state").json()
# print(state)
