import sys
import time
import pyautogui
import threading

import FaceRecognition as fr
import hand_mouce as hm

sys.path.append("D:\\programs\\Project Shunn\\Features")
import commands as cd

def cv_control(quary):
        
        if quary in cd.facerecognition_activate_command:
            t1 = threading.Thread(target=fr.faceRecognitionMode)
            t1.start()

        elif quary in cd.facerecognition_deactivate_command:
            pyautogui.typewrite("q")
        
        elif quary in cd.cctv_on_commands:
            t2 = threading.Thread(target=fr.cctv_camera)
            t2.start()
        
        elif quary in cd.cctv_off_commands:
            pyautogui.typewrite("q")
        
        elif quary in cd.activate_hand_mouse_commands:
            t3 = threading.Thread(target=hm.hand_mouse_mode)
            t3.start()
        
        elif quary in cd.deactivate_hand_mouse_commands:
            hm.stop_hand_mouse()
            
    
# # Call this function from anywhere
# if __name__ == "__main__":
#      cv_control('activate hand mouse mode')

