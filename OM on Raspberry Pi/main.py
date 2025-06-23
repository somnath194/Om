import requests
import threading
import time
import json
import sys

from flags import exit_event
from run_flask import run as run_flask
from command_executor import CommandExecutor
from openai_parser import parse_transcript
import general_functions as gf

sys.path.append("D:\\programs\\Project Shunn\\Features")
file_path = "D:\\programs\\Project Shunn\\Features\\SpeechRecogonisition.txt"
sleep_commands = ['sleep', 'it\'s time to sleep', 'you can rest now', 'bedtime', 
                  'initiate sleep mode', 'sleep well', 'go to sleep', 'go and take rest','rest','take rest', 'time to rest', 'you can sleep now']

wake_up_commands = ['wake up','wake up om','are you there', 'let\'s get back to work', 'you there', 'time to wake up', 'ready to start the day?',
                     'let\'s do some work', 'work time', 'awake and alert', 'hello, ready for the day']

exit_commands = ["bye",'by', 'byy',"good bye","see you later", "goodbye", "farewell", "take care", "until next time", "bye bye", 
                    "catch you later", "have a good one", "by krishna",'exit','okay exit','okay bye','bye Om','okay by']

# Constants for sleep/wake
SLEEP_TIMEOUT = 180  # 3 minutes in seconds

# States
is_awake = True
last_command_time = time.time()
executor = CommandExecutor()

def wait_and_shutdown():
    exit_event.wait()
    gf.close_application('close chrome')
    requests.post('http://localhost:5000/shutdown')

# Start Flask and Shutdown Watcher
threading.Thread(target=run_flask, daemon=True).start()
threading.Thread(target=wait_and_shutdown, daemon=True).start()

print("[OM] System is Ready to Take Commands.....")

last_transcript = ""

try:
    while not exit_event.is_set():
        time.sleep(1)
        with open(file_path, "r") as file:
            transcript = file.read().strip().lower()

        # Reset transcript file
        open(file_path, "w").close()

        # Skip empty transcript
        if not transcript or transcript == last_transcript:
            # Check for inactivity sleep
            if is_awake and time.time() - last_command_time > SLEEP_TIMEOUT:
                print("[OM] No command for 3 minutes. Going to sleep mode...")
                is_awake = False
            continue


        # Global exit
        if transcript in exit_commands:
            exit_event.set()
            print("[OM] Shutting down...")
            break

        # Manual sleep command
        if transcript in sleep_commands:
            if is_awake:
                is_awake = False
                print("[OM] Going to sleep...")
                continue
            else:
                print("[OM] I'm Already Sleeping!")
                continue

        # Wake up command
        if transcript in wake_up_commands:
            if not is_awake:
                is_awake = True
                last_command_time = time.time()
                print("[OM] I am awake now!")
                continue
            else:
                print("[OM] I'm Already Awake Ready for Your Commands......")
                continue

        # If awake, parse and execute command
        if is_awake and transcript != last_transcript:
            last_command_time = time.time()
            last_transcript = transcript
            output = parse_transcript(transcript)
            executor.execute(json.loads(output))
            print(output)

        if not is_awake:
            print("[OM] I'm Sleeping... Waiting for wake-up command.")

except KeyboardInterrupt:
    exit_event.set()
    print("[OM] Force shut down via KeyboardInterrupt.")
