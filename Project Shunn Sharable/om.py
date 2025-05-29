import pywhatkit as kit
import sys
import pyautogui
import random
from time import sleep


########################ALL CUSTOME MODULE########################
sys.path.append("D:\\programs\\Project Shunn\\Features")
sys.path.append("D:\\programs\\Project Shunn\\Home Automation codes")
sys.path.append("D:\\programs\\Project Shunn\\Computer Vision Code")


import lisent_speak as ls
import helper_functions as hf
import general_functions as gf
import VolumeControl as vc
import RelayDeviceAutomate as home 
import commands as cd
import cv_control as cvc
import android_automation as aa
import wled_control as wc
###################################################################

def taskexection():
    while True:
        print('listening for commands.....')
        # quary = ls.takecommand()
        quary = hf.real_time_take_command()
        quary_without_int = hf.remove_int_from_string(quary)
        yt_search_quary = hf.searchYt_command(quary)
        goo_search_quary = hf.searchGoo_command(quary)
        typing_search_quary = hf.searchType_command(quary)
        wled_color_quary = wc.set_wled_color(quary)
        shelf_color_quary = wc.set_shelf_color(quary)


        if quary in cd.sleep_commands:
            sleep_response = random.choice(cd.sleep_responses)
            ls.speak(sleep_response)
            break 

        elif quary in cd.greetings_commands:
            res = random.choice(cd.greetings_response)
            ls.speak(res)
        
        elif quary in cd.thankyou_commands:
            res = random.choice(cd.thankyou_response)
            ls.speak(res)
        
        elif quary in cd.open_applicatioin_commands:
            gf.open_application(quary)

        elif quary in cd.close_applicatioin_commands:
            gf.close_application(quary)

        elif quary in cd.minimize_applicatioin_commands:
            gf.minimise_application(quary)

        elif quary in cd.maximize_applicatioin_commands:
            gf.maximize_application(quary)

        elif quary in cd.open_website_commands:
            gf.open_website(quary)
        
        elif quary in cd.open_internal_application_commands:
            gf.open_internal_application(quary)
        
        elif quary in cd.system_configure_commands:
            gf.system_configure(quary)

        elif quary_without_int in cd.brightness_control_commands:
            br = hf.extract_int_from_text(quary)
            if isinstance(br, float):
                if br < 100:
                    hf.set_brightness_lavel(br)
            else:
                ls.speak("Please speak clearly the brightness value")
        
        elif quary_without_int in cd.volume_control_commands:
            #########PROBLEM#####################
            vol = hf.extract_int_from_text(quary)
            if isinstance(vol, float):    
                vc.set_volume(vol)
            else:
                ls.speak("Please speak clearly the volume level")

        elif goo_search_quary in cd.google_search_commands:
            search_content = quary.replace(goo_search_quary,'')
            hf.google_search(search_content)
        
        elif yt_search_quary in cd.youtube_search_commands:
            search_content = quary.replace(yt_search_quary,'')
            kit.playonyt(search_content)

        elif typing_search_quary in cd.typing_commands:
            type_content = quary.replace(typing_search_quary,'')
            sleep(3)
            pyautogui.typewrite(type_content)
        
        elif quary in cd.check_pc_commands:
            gf.check_pc(quary)

        elif quary in cd.home_automation_commands:
            home.RoomControl(quary)

        elif quary in cd.computer_vision_commands:
            cvc.cv_control(quary)
        
        elif quary in cd.android_automation_commands:
            aa.android_automation(quary)

        elif quary in cd.wled_automation_commands:
            wc.wled_control(quary)

        elif wled_color_quary in cd.wled_colour_commands:
            wc.wled_control(quary)

        elif shelf_color_quary in cd.set_shelf_color:
            wc.wled_control(quary)

        elif quary in cd.goodbye_commands:
            goodbyy_response = random.choice(cd.goodbyy_responses)
            ls.speak(goodbyy_response)
            sys.exit()

# if __name__ == "__main__":
#     taskexection()
