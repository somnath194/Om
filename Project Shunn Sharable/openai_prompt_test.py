from openai import OpenAI
client = OpenAI(
  api_key="" )

prompt_template = """[INST] Task: You are a personal AI Assistant of name: "OM" trained to generate function names to complete given task.
Given a transcript of a conversation or command, analyze the text and extract the primary action(s) that need to be executed. For each action, map it to a function from the predefined list below. Each function includes its expected arguments. If the action does not match any function in the list, set the functionName to null and arguments to an empty object. For matched actions, intelligently extract and assign values to the arguments based on the transcript. Return the result as a JSON array, where each object contains:
action: A description of the action.
functionName: The matched function name from the list, or null if no match.
arguments: An object containing the extracted arguments, or an empty object if none.
Predefined Function List:
[
  {
    "functionName": "applicationControl",
    "arguments": ["applicationName", "device", "controlType"]
  },
  {
    "functionName": "openWebsite",
    "arguments": ["websiteUrl", "device"]
  },
  {
    "functionName": "openInternalApplication",
    "arguments": ["applicationName", "device"]
  },
  {
    "functionName": "systemConfigure",
    "arguments": ["action", "device"]
  },
  {
    "functionName": "checkInfo",
    "arguments": ["informationType", "device"]
  },
  {
    "functionName": "setValue",
    "arguments": ["valueType", "value", "device"]
  },
  {
    "functionName": "search",
    "arguments": ["searchPlatform", "searchContent", "device"]
  },
  {
    "functionName": "type",
    "arguments": ["typingString", "device"]
  },
  {
    "functionName": "call",
    "arguments": ["personName", "device", "callMedia", "callType"]
  },
  {
    "functionName": "message",
    "arguments": ["personName", "device", "messageMedia", "messageContent"]
  },
  {
    "functionName": "homeControl",
    "arguments": ["controlledDevice", "controlledState"]
  },
  {
    "functionName": "ledStripMusicSync",
    "arguments": []
  },
  {
    "functionName": "setLedStripLightColour",
    "arguments": ["rgbColourCode", "brightnessValue"]
  },
  {
    "functionName": "setLedStripLightSegmentColour",
    "arguments": ["segmentName", "rgbColourCode", "brightnessValue"]
  },
  {
    "functionName": "computerVisionActivation",
    "arguments": ["feature", "state"]
  }
]
Argument Value List Example:
{
  "device": ["pc", "laptop", "phone", "tab"],

  "applicationName (applicationControl)": [
    "brave", "chrome", "vscode", "notepad", "Arduino", "paint", "davinci resolve", "glindex"
  ],

  "controlType": ["open", "close", "minimize", "maximize"],

  "websiteUrl": [
    "https://www.instagram.com",
    "https://chat.openai.com/",
    "https://www.amazon.in/gp/sva/dashboard?ref_=nav_cs_apay"
  ],

  "applicationName (openInternalApplication)": [
    "cmd", "file_explorer", "task manager", "settings"
  ],

  "action(system configure)": [
    "minimize all window", "minimize current window", "shutdown", "sleep", "restart",
    "switch window", "pause", "hit enter", "full screen", "hit space", "close browser tab",
    "select all", "copy", "paste"
  ],

  "informationType": ["ip address", "location", "internet speed"],

  "valueType": ["brightness", "volume"],

  "value": ["20%", "90%"],

  "searchPlatform": ["google", "youtube", "inside device"],

  "searchContent": ["who is the president of india"],

  "typingString": ["search on google who is president of india"],

  "personName": ["sister", "surya", "aryan", "amazon helpline"],

  "callMedia": ["SIM", "whatsapp"],

  "callType": ["audio", "video"],

  "messageMedia": ["SIM", "whatsapp", "insta", "facebook"],

  "controlledDevice": [
    "bedroom light", "bedroom fan", "bedroom bulb", "bathroom light", "stair light",
    "outdoor light", "outdoor camera", "pc", "home theater", "main led strip light",
    "back almary strip light", "raspberry pi", "soldering iron"
  ],

  "controlledState": ["on", "off"],

  "rgbColourCode": ["[255,0,0]", "[255,255,0]"],

  "brightnessValue": ["20%", "100%"],

  "segmentName": [
    "main ceiling", "front almary", "back almary", "ganesha almary", "shiva almary",
    "behind the money plant", "under pc table", "under laptop table"
  ],

  "rgbColourCode": ["[255,0,0]"],

  "feature(computer vision)": [
    "face recognition", "cctv feed", "pc camera feed", "phone camera feed",
    "tab camera feed", "hand mouse mode", "objection detection mode", "ocr detection mode"
  ],

  "state(comuter)": ["activate", "deactivate"]
}



Guidelines:
Focus on actionable tasks or requests within the voice_transcript.
Use the closest matching function name from the predefined list.
Refer argument value list example not strictly but provide for better understanding
For matched actions, extract and assign argument values as intelligently as possible from the transcript.
Generate rgbColourCode as value like [255,0,0] for red and don’t pass rgbColourCode argument as “red” or “green”
LedStripMusicSync is the function to activate wled strip light sync with music its not relate playing music or searching music

Ignore small talk or non-actionable statements.

## Output Format (Strict JSON, Do Not Exceed This Format):
[
  {
    "action": "<Action description>",
    "functionName": "<function_name or null>",
    "arguments": {
      // key-value pairs of arguments, or empty if none
    }
  }
  // ...additional actions
]

[/INST] Input :
"""

voice_transcript = "activate face detection mode and than turn on bedroom light"

response = client.responses.create(
    model="gpt-4.1-mini",
    input=f"{prompt_template} {voice_transcript}"
)

print(response.output_text)

# from openai import OpenAI

# client = OpenAI(
#   api_key="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"
# )

# completion = client.chat.completions.create(
#   model="gpt-4o-mini",
#   store=True,
#   messages=[
#     {"role": "user", "content": "write a haiku about ai"}
#   ]
# )

# print(completion.choices[0].message)
