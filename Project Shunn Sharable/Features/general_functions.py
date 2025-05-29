import pygetwindow as gw
from time import sleep
import sys
import os
import subprocess
import webbrowser
import pyautogui
import socket

# sleep(2)
# data = print(gw.getAllTitles())
sys.path.append("D:\\programs\\Project Shunn\\Features")
import commands as cd
import lisent_speak as ls
import helper_functions as hf
import pywhatkit as kit


def is_application_open(app_name):
    t = 0
    data = gw.getAllTitles()
    for i in data:
        if app_name in i:
            t = t + 1
    if t >= 1:
        return True
    else:
        return False

def is_maximize(app_name):
    try:
        app_instance = gw.getWindowsWithTitle(app_name)[0]
        return app_instance.isMaximized
    except IndexError:
        print("App in not opened!")
        return False

def search_app_windows(app_name):
    l = []
    data = gw.getAllTitles()
    for i in data:
        if app_name in i:
            l.append(i)
    return l

def minimize_current_tab():
    data = gw.getAllTitles()
    current_tab = data[1]
    app_instance = gw.getWindowsWithTitle(current_tab)[0]
    app_instance.minimize()

def open_application(quary):
    if quary in cd.open_brave_commands:
        os.startfile(cd.brave_file_path)

    elif quary in cd.open_chrome_commands:
        os.startfile(cd.chrome_file_path)
        
    elif quary in cd.open_vscode_commands:
        os.startfile(cd.vscode_file_path)
        
    elif quary in cd.open_notepad_commands:
        os.startfile(cd.notepad_file_path)

    elif quary in cd.open_arduino_commands:
        with open(os.devnull, 'w') as null_file:
                process = subprocess.Popen([cd.arduino_file_path], stdout=null_file, stderr=null_file, shell=True)
        
    # elif quary in cd.open_eagle_commands:
    #     os.startfile(cd.eagle_file_path)
        
    elif quary in cd.open_paint_commands:
        os.startfile(cd.paint_file_path)
    
    else:
        ls.speak("No Application Found!")

def open_website(quary):
    if quary in cd.open_insta_commands:
        webbrowser.open("https://www.instagram.com")

    elif quary in cd.open_facebook_commands:
            webbrowser.open("https://www.facebook.com")

    elif quary in cd.open_amazon_commands:
        webbrowser.open("https://www.amazon.in/ref=nav_logo")

    elif quary in cd.open_gmail_commands:
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
        
    elif quary in cd.open_whatsapp_commands:
        webbrowser.open("https://web.whatsapp.com/")

    elif quary in cd.open_chatgpt_commands:
        webbrowser.open("https://chat.openai.com/")
        
    elif quary in cd.open_youtube_commands:
        webbrowser.open("https://www.youtube.com/")
        
    elif quary in cd.open_cricbuzz_commands:
        webbrowser.open("https://www.cricbuzz.com/")

    elif quary in cd.open_drive_commands:
        webbrowser.open("https://drive.google.com/drive/my-drive")
    
    elif quary in cd.open_amazon_pay_commands:
        webbrowser.open("https://www.amazon.in/gp/sva/dashboard?ref_=nav_cs_apay")
        
    elif quary in cd.open_amazon_prime_commands:
        webbrowser.open("https://www.primevideo.com/")

    elif quary in cd.open_blinkit_commands:
        webbrowser.open("https://blinkit.com/")

def open_internal_application(quary):
    if quary in cd.open_cmd_commands:
        os.system("start cmd")

    elif quary in cd.open_file_commands:
        subprocess.run(["explorer"])

    elif quary in cd.open_task_commands:
        sleep(.2)
        pyautogui.click(702,1079)
        sleep(.2)
        pyautogui.click(857,1054)
        pyautogui.typewrite("task manager")
        sleep(.2)
        pyautogui.press("enter")

    elif quary in cd.open_settings_commands:
        pyautogui.hotkey('winleft', 'i')
        sleep(1)

def system_configure(quary):
    if quary in cd.minimize_all_commands:
        pyautogui.hotkey('win', 'm')

    elif quary in cd.minimize_current_windows_commands:
        minimize_current_tab()

    # elif quary in cd.shutdown_commands:
    #     os.system("shutdown /s /t 5")
        
    # elif quary in cd.restart_commands:
    #     os.system("shutdown /r /t 5")
        
    elif quary in cd.pc_sleep_commands:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        
    elif quary in cd.switch_window_commands:
        pyautogui.hotkey('alt', 'tab')

    elif quary in cd.pause_commands:
        pyautogui.press("playpause")
    
    elif quary in cd.hit_enter_commands:
        pyautogui.press('enter')

    elif quary in cd.full_screen_commands:
        pyautogui.press('f')

    elif quary in cd.hit_space_commands:
        pyautogui.press('space')

def check_pc(quary):
    if quary in cd.ip_address_commands:
        local_ip = socket.gethostbyname(socket.gethostname())
        ls.speak(local_ip)
        
    elif quary in cd.location_commands:
        city,state = hf.get_location_details()
        ls.speak(f"sir we are in {city} city of {state} state")
        
    elif quary in cd.internet_speed_commands:
        ls.speak("Checking your internet speed please wait............")
        down,up = hf.check_internet_speed()
        ls.speak(f"Your download speed is {down} Mbps and your upload speed is {up} Mbps")

def close_application(quary):
    if quary in cd.close_arduino_commands:
        ard = search_app_windows(cd.arduino_name)
        for i in ard:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.close()

    elif quary in cd.close_brave_commands:
        brv = search_app_windows(cd.brave_browser_name)
        for i in brv:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.close()

    elif quary in cd.close_chrome_commands:
        chr = search_app_windows(cd.google_chrome_name)
        for i in chr:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.close()

    elif quary in cd.close_eagle_commands:
        eag = search_app_windows(cd.eagle_pcb_name)
        for i in eag:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.close()

    elif quary in cd.close_notepad_commands:
        note = search_app_windows(cd.notepad_name)
        for i in note:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.close()
    
    elif quary in cd.close_paint_commands:
        paint = search_app_windows(cd.paint_name)
        for i in paint:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.close()
    
    elif quary in cd.close_vscode_commands:
        vs = search_app_windows(cd.vscode_name)
        for i in vs:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.close()

    elif quary in cd.close_file_commands:
        fl = search_app_windows(cd.file_name)
        for i in fl:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.close()

    elif quary in cd.close_settings_commands:
        st = search_app_windows(cd.settings_name)
        for i in st:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.close()

    elif quary in cd.close_cmd_commands:
        cm = search_app_windows(cd.cmd_name)
        for i in cm:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.close()
    
    elif quary in cd.close_file_commands:
        fl = search_app_windows(cd.file_name)
        for i in fl:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.close()
    
    elif quary in cd.close_tab_commands:
        pyautogui.hotkey('ctrl', 'w')
        sleep(1)

def minimise_application(quary):
    if quary in cd.minimize_arduino_commands:
        ard = search_app_windows(cd.arduino_name)
        for i in ard:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.minimize()

    elif quary in cd.minimize_brave_commands:
        brv = search_app_windows(cd.brave_browser_name)
        for i in brv:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.minimize()

    elif quary in cd.minimize_chrome_commands:
        chr = search_app_windows(cd.google_chrome_name)
        for i in chr:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.minimize()

    elif quary in cd.minimize_eagle_commands:
        eag = search_app_windows(cd.eagle_pcb_name)
        for i in eag:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.minimize()

    elif quary in cd.minimize_notepad_commands:
        note = search_app_windows(cd.notepad_name)
        for i in note:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.minimize()
    
    elif quary in cd.minimize_paint_commands:
        paint = search_app_windows(cd.paint_name)
        for i in paint:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.minimize()

    elif quary in cd.minimize_vscode_commands:
        vs = search_app_windows(cd.vscode_name)
        for i in vs:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.minimize()
    
def maximize_application(quary):
    if quary in cd.maximize_arduino_commands:
        ard = search_app_windows(cd.arduino_name)
        for i in ard:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.maximize()

    elif quary in cd.maximize_brave_commands:
        brv = search_app_windows(cd.brave_browser_name)
        for i in brv:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.maximize()

    elif quary in cd.maximize_chrome_commands:
        chr = search_app_windows(cd.google_chrome_name)
        for i in chr:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.maximize()

    elif quary in cd.maximize_eagle_commands:
        eag = search_app_windows(cd.eagle_pcb_name)
        for i in eag:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.maximize()

    elif quary in cd.maximize_notepad_commands:
        note = search_app_windows(cd.notepad_name)
        for i in note:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.maximize()
    
    elif quary in cd.maximize_paint_commands:
        paint = search_app_windows(cd.paint_name)
        for i in paint:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.maximize()
    
    elif quary in cd.maximize_vscode_commands:
        vs = search_app_windows(cd.vscode_name)
        for i in vs:
            app_instance = gw.getWindowsWithTitle(i)[0]
            app_instance.maximize()

