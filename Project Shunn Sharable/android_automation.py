import requests
import sys

sys.path.append("D:\\programs\\Project Shunn\\Features")

import commands as cd


# # Your MacroDroid Webhook URL
whatsapp_open_url = ""
location_share_url = ""
take_photo_url = ""
volume_up_url = ''
call_my_sister_url = ""

# volume_down_url = ""

brightness_up_url = ""
# set_alarm_url = ""



# response = requests.get(set_alarm_url)
# # Print response from MacroDroid
# print("Status Code:", response.status_code)
# print("Response:", response.text)

def android_automation(quary):
    if quary in cd.take_picture_commands:
        requests.get(take_photo_url)
    elif quary in cd.call_from_phone_command:
        requests.get(call_my_sister_url)
    elif quary in cd.share_location_commands:
        requests.get(location_share_url)
        print("Location was sent to Gmail")
    elif quary in cd.increase_volume_commands:
        requests.get(volume_up_url)
    elif quary in cd.open_whatsapponphone_command:
        requests.get(whatsapp_open_url)
    elif quary in cd.increase_brightness_commands:
        requests.get(brightness_up_url)

# # Call this function from anywhere
# if __name__ == "__main__":
#      requests.get(brightness_up_url)