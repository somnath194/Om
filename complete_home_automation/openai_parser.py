from openai import OpenAI

client = OpenAI(
  api_key="your_api_key"
    )

prompt_template = """[INST] Task: You are a personal AI Assistant of name: "OM" trained to generate function names to complete given task.
Given a transcript of a conversation or command, analyze the text and extract the primary action(s) that need to be executed. For each action, map it to a function from the predefined list below. Each function includes its expected arguments. If the action does not match any function in the list, set the functionName to null and arguments to an empty object. For matched actions, intelligently extract and assign values to the arguments based on the transcript. Return the result as a JSON array, where each object contains:
action: A description of the action.
functionName: The matched function name from the list, or null if no match.
arguments: An object containing the extracted arguments, or an empty object if none.
Predefined Function List:
[
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
    "functionName": "setLedStripMode",
    "arguments": ["stripMode"]
  },
  {
    "functionName": "setLedStripSegment",
    "arguments": ["segmentName", "rgbColourCode", "brightnessValue"]
    }
]
Argument Value List Example:
{
  "personName": ["sister", "surya", "aryan", "amazon helpline"],//non-strict

  "callMedia": ["SIM", "whatsapp"],//strict

  "callType": ["audio", "video"],//strict

  "messageMedia": ["SIM", "whatsapp", "insta", "facebook"],//strict

  "controlledDevice": [
    "bedroom light", "bedroom fan", "bedroom bulb", "bathroom light", "siri light",
    "outdoor light", "outdoor camera", "pc", "home theater", "main led",
    "side led", "raspberry pi", "soldering iron" ],//strict

  "controlledState": ["on", "off"],//strict

  "stripMode": ["musicSync","workMode","shootingMode"],//strict

  "rgbColourCode": ["[255,0,0]", "[255,255,0]"],//non-strict

  "brightnessValue": ["20%", "100%"],//non-strict

  "segmentName": [
    "ceiling", "front almary", "back almary", "ganesha almary", "shiva almary",
    "behind the money plant", "under pc table", "under laptop table","all"
  ]//strict
}



Guidelines:
Focus on actionable tasks or requests within the voice_transcript.
Use the closest matching function name from the predefined list.
Refer argument value list example strictly where strict was mentioned after // and not-strictly where not-strict was mentioned
For matched actions, extract and assign argument values as intelligently as possible from the transcript.
Generate rgbColourCode as value like [255,0,0] for red and don’t pass rgbColourCode argument as “red” or “green”
For homeControl function choose controlledDevice intelligently from given control device arguments like if command was "room light on" 
than i mean to say take device as bedroom
siri light also mean for stair light and outdoor also mean for outside and home theater also mean for speaker
Please map the brightness value to 0-255(8bit) from 0-100% and pass in brightnessValue argument
If command says to only turn on/off a particular segment than pass the brightness value of that segments as 255 for on and 0 for off and pass colourCode as none
If command says set strip color as 'some color' or set all segment as color 'some color' than choose segment argument as "all" and if any segment was mentioned that pass the segment choosen from given segmentName
main led and side led are the devices whcih comes under controlledDevice it's not a strip light segment

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

def parse_transcript(transcript):
    result = client.responses.create(
        model="gpt-4.1-mini",
        input=f"{prompt_template} {transcript}"
    )
    return result.output_text

# if __name__=="__main__":
#     print(parse_transcript("set under pc table strip light color as pink with 50%  brightness"))