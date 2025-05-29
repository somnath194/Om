import requests
import sys

WLED_IP = "192.168.1.5"


sys.path.append("D:\\programs\\Project Shunn\\Features")
import commands as cd
import helper_functions as hf



def set_segment_state(
    global_on=None,       # Default to None, indicating no change unless specified
    ps=None, 
    global_brightness=None,
    segment_id=None,
    color_rgb=None, 
    segment_brightness=None,
    effect=None,
    effect_speed=None,
    effect_intensity=None,
    palette=None,
    segment_on=None
):
    """
    Update a specific segment's color, brightness, effect, and other parameters on a WLED device.
    
    Parameters:
        segment_id (int): ID of the segment to update
        color_rgb (list): RGB color (e.g. [255, 0, 0])
        brightness (int): Brightness (0-255)
        effect (int): Effect index (0-200+)
        effect_speed (int): Effect speed (0-255)
        effect_intensity (int): Effect intensity (0-255)
        palette (int): Palette index (optional, 0-49+)
        on (bool): Turn segment on/off
    """
    url = f"http://{WLED_IP}/json/state"

    # Start with a base payload that includes only parameters that are being set
    payload = {}

    # Set parameters only if passed, otherwise leave unchanged
    if global_on is not None:
        payload["on"] = global_on
    if global_brightness is not None:
        payload["bri"] = global_brightness
    if ps is not None:
        payload["ps"] = ps
    if segment_id is not None:
        payload["seg"] = [{
            "id": segment_id,
            "on": segment_on if segment_on is not None else True,  # Ensure segment state is respected
            "bri": segment_brightness if segment_brightness is not None else 255,  # Default segment brightness
            "col": [color_rgb if color_rgb is not None else [255, 255, 255], [0, 0, 0], [0, 0, 0]],  # Default to white
            "fx": effect if effect is not None else 0,  # Default to no effect
            "sx": effect_speed if effect_speed is not None else 128,  # Default speed
            "ix": effect_intensity if effect_intensity is not None else 128,  # Default intensity
            "pal": palette if palette is not None else 0  # Default palette
        }]
    
    # Send the payload to the WLED device
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"✅ Segment {segment_id} updated successfully.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to update segment {segment_id}: {e}")

def set_wled_color(quary):
    result = ''
    for i in cd.wled_colour_commands:
        if i in quary:
            result = i
    return result
def set_shelf_color(quary):
    result = ''
    for i in cd.set_shelf_color:
        if i in quary:
            result = i
    return result


def wled_control(quary):
    wled_search_quary = set_wled_color(quary)
    shelf_search_quary = set_shelf_color(quary)
    if quary in cd.wled_on_commands:
        set_segment_state(global_on=True, global_brightness=200)
    elif quary in cd.wled_off_commands:
        set_segment_state(global_on=False)
    elif quary in cd.wled_music_sync_commands:
        set_segment_state(global_on=True, global_brightness=200,ps=-1,segment_id=0,segment_on=True,segment_brightness=255,effect=165,effect_speed=101,effect_intensity=148,palette=72)
    elif wled_search_quary in cd.wled_colour_commands:
        print('ok2')
        color_content = quary.replace(wled_search_quary,'')
        if 'red' in color_content:
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=0,segment_on=True,color_rgb=[255,0,0])
        elif 'green' in color_content:
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=0,segment_on=True,color_rgb=[0,255,0])
        elif 'blue' in color_content:
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=0,segment_on=True,color_rgb=[0,0,255])
        elif 'sayan' in color_content:
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=0,segment_on=True,color_rgb=[0,255,255])
        elif 'pink' in color_content:
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=0,segment_on=True,color_rgb=[255, 0, 255])
        elif 'yellow' in color_content:
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=0,segment_on=True,color_rgb=[255,255,0])
        elif 'white' in color_content:
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=0,segment_on=True,color_rgb=[255,255,255])

    elif shelf_search_quary in cd.set_shelf_color:
        print('ok3')
        color_content2 = quary.replace(shelf_search_quary,'')
        if 'red' in color_content2:
            set_segment_state(global_on=True,global_brightness=200,ps=4,segment_id=1,segment_on=True,color_rgb=[255,0,0])
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=1,segment_on=True,color_rgb=[255,0,0])
        elif 'green' in color_content2:
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=1,segment_on=True,color_rgb=[0,255,0])
        elif 'blue' in color_content2:
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=1,segment_on=True,color_rgb=[0,0,255])
        elif 'sayan' in color_content2:
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=1,segment_on=True,color_rgb=[0,255,255])
        elif 'pink' in color_content2:
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=1,segment_on=True,color_rgb=[255, 0, 255])
        elif 'yellow' in color_content2:
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=1,segment_on=True,color_rgb=[255,255,0])
        elif 'white' in color_content2:
            set_segment_state(global_on=True,global_brightness=200,ps=-1,segment_id=1,segment_on=True,color_rgb=[255,255,255])

# wled_control('activate party mode')
# print(set_wled_color('put wled color by red'))
# url = f"http://{WLED_IP}/json/state"


# state = requests.get(f"http://{WLED_IP}/json/state").json()
# print(state)
