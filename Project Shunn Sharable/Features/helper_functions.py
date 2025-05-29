import sys
import datetime
import time
sys.path.append("D:\\programs\\Project Shunn\\Features")
import lisent_speak as ls
import re
import screen_brightness_control as sbc
import speedtest
import geocoder
from geopy.geocoders import Nominatim
import requests
from bs4 import BeautifulSoup 
import webbrowser
import commands as cd
import random



def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")
    greetings_index = random.randint(0, len(cd.greetings_response)-1)
    if hour>=0 and hour<12:
        ls.speak(f"Good morning boss, its {tt}")
    elif hour>=12 and hour<18:
        ls.speak(f"Good Afternoon boss, its {tt}")
    elif hour>=18 and hour<21:
        ls.speak(f"Good evening boss , its {tt}")
    else:
        ls.speak("Good night boss")
    ls.speak(cd.greetings_response[greetings_index])
  
def extract_int_from_text(text):
    l=[]
    match = re.search(r'(\d+)%', text)
    if match:
        l.append(float(match.group(1)))
    else:
        for t in text.split(' '):
            try:
                l.append(float(t))
            except ValueError:
                pass
    try:
        return float(l[0])
    except:
        return "No int in text!"

def set_brightness_lavel(b):
    sbc.set_brightness(b)

def remove_int_from_string(input_string):
    match = re.search(r'(\d+)%', input_string)
    if match:
        result_string = re.sub(r'\b\d+%|\b\d+\.\d+%', '', input_string)
    else:
        result_string = re.sub(r'\d+', '', input_string)
    return result_string

def real_time_take_command():
        while True:
            File = open("D:\\programs\\Project Shunn\\Features\\SpeechRecogonisition.txt","r")
            Data = File.read()
            File.close()

            FileHistory = open("D:\\programs\\Project Shunn\\Features\\ChatHistory.txt","r")
            DataHistory = FileHistory.read()
            FileHistory.close()

            if str(Data) == str(DataHistory):
                time.sleep(0.5)
                pass

            else:
                FileHistory = open("D:\\programs\\Project Shunn\\Features\\ChatHistory.txt","w")
                FileHistory.write(Data)
                FileHistory.close()
                return str(Data.strip().lower())

def check_internet_speed():
    try:
        st = speedtest.Speedtest()

        # Perform the speed test
        download_speed = st.download() / 10**6  # Convert to Mbps
        upload_speed = st.upload() / 10**6  # Convert to Mbps

        return round(download_speed), round(upload_speed)

    except Exception as e:
        print(f"Error: {e}")
        return None      

def get_location_details():
    try:
        # Get the current location using the IP address
        location = geocoder.ip('me')

        if location.latlng:
            # Reverse geocode to get city, state, and area details
            geolocator = Nominatim(user_agent="location_app")
            location_details = geolocator.reverse(location.latlng)
            
            city = location_details.raw.get('address', {}).get('city', '')
            state = location_details.raw.get('address', {}).get('state', '')
            
            return city, state
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def city_temperature():
    city,state = get_location_details()
    search = f"temperature in bengaluru"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div",class_="BNeawe").text
    return temp

def searchYt_command(quary):
    result = ''
    for i in cd.youtube_search_commands:
        if i in quary:
            result = i
    return result

def searchGoo_command(quary):
    result = ''
    for i in cd.google_search_commands:
        if i in quary:
            result = i
    return result


def google_search(query):
    try:
        # Construct the Google search URL
        search_url = f"https://www.google.com/search?q={query}"

        # Open the default web browser and perform the search
        webbrowser.open(search_url)

    except Exception as e:
        print(f"Error: {e}")

def searchType_command(quary):
    result = ''
    for i in cd.typing_commands:
        if i in quary:
            result = i
    return result
