from openai import OpenAI

client = OpenAI(
  api_key=""
    )

tools = [
    {
        "type": "function",
        "name": "applicationControl",
        "description": "Control an application on a specific device, such as opening, closing, minimizing, or maximizing it.",
        "parameters": {
            "type": "object",
            "properties": {
                "applicationName": {
                    "type": "string",
                    "description": "The name of the application to control. E.g., chrome, vscode, notepad"
                },
                "device": {
                    "type": "string",
                    "description": "The device to perform the action on. E.g., pc, laptop, phone, tab"
                },
                "controlType": {
                    "type": "string",
                    "description": "The type of control action to perform. E.g., open, close"
                }
            },
            "required": ["applicationName", "device", "controlType"]
        }
    },
    {
        "type": "function",
        "name": "openWebsite",
        "description": "Open a specified website URL on a device.",
        "parameters": {
            "type": "object",
            "properties": {
                "websiteUrl": {
                    "type": "string",
                    "description": "The URL of the website to open."
                },
                "device": {
                    "type": "string",
                    "description": "The device to open the website on.E.g., pc, laptop, phone, tab"
                }
            },
            "required": ["websiteUrl", "device"]
        }
    },
    {
        "type": "function",
        "name": "openInternalApplication",
        "description": "Open internal system applications like File Explorer or Task Manager.",
        "parameters": {
            "type": "object",
            "properties": {
                "applicationName": {
                    "type": "string",
                    "description": "The name of the internal application to open.e.g-cmd, file_explorer, task manager, settings"
                },
                "device": {
                    "type": "string",
                    "description": "The device to open the application on."
                }
            },
            "required": ["applicationName", "device"]
        }
    },
    {
        "type": "function",
        "name": "systemConfigure",
        "description": "Perform a system configuration action such as shutdown, minimize all windows, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "System configuration action to perform.E.g- minimize all window, minimize current window,shutdown,sleep, restart switch window,pause,hit enter, full screen,hit space, close browser tab,select all,copy,paste."
                },
                "device": {
                    "type": "string",
                    "description": "The device to perform the action on."
                }
            },
            "required": ["action", "device"]
        }
    },
    {
        "type": "function",
        "name": "checkInfo",
        "description": "Check information from devices  such as IP address or internet speed from pc or phone.",
        "parameters": {
            "type": "object",
            "properties": {
                "informationType": {
                    "type": "string",
                    "description": "Type of information to check.e.g-ip address,location,internet speed"
                },
                "device": {
                    "type": "string",
                    "description": "The device to fetch information from."
                }
            },
            "required": ["informationType", "device"]
        }
    },
    {
        "type": "function",
        "name": "setSystemValue",
        "description": "Set system values like brightness or volume.",
        "parameters": {
            "type": "object",
            "properties": {
                "valueType": {
                    "type": "string",
                    "description": "Type of value to set (e.g., brightness, volume)."
                },
                "value": {
                    "type": "string",
                    "description": "Value to be set (e.g., 90%)."
                },
                "device": {
                    "type": "string",
                    "description": "Device on which to set the value."
                }
            },
            "required": ["valueType", "value", "device"]
        }
    },
    {
        "type": "function",
        "name": "search",
        "description": "Perform a search on a platform such as Google or YouTube.",
        "parameters": {
            "type": "object",
            "properties": {
                "searchPlatform": {
                    "type": "string",
                    "description": "Platform to search on (e.g., google, youtube)."
                },
                "searchContent": {
                    "type": "string",
                    "description": "Content to search for."
                },
                "device": {
                    "type": "string",
                    "description": "Device to perform the search on."
                }
            },
            "required": ["searchPlatform", "searchContent", "device"]
        }
    },
    {
        "type": "function",
        "name": "type",
        "description": "Type a string into the device as if input from a keyboard.",
        "parameters": {
            "type": "object",
            "properties": {
                "typingContent": {
                    "type": "string",
                    "description": "The content to type."
                },
                "device": {
                    "type": "string",
                    "description": "The target device."
                }
            },
            "required": ["typingContent", "device"]
        }
    },
    {
        "type": "function",
        "name": "call",
        "description": "Initiate a call to a contact via a specific media and call type.",
        "parameters": {
            "type": "object",
            "properties": {
                "personName": {
                    "type": "string",
                    "description": "Name of the contact to call."
                },
                "device": {
                    "type": "string",
                    "description": "The device to initiate the call from."
                },
                "callMedia": {
                    "type": "string",
                    "description": "The medium for the call (e.g., SIM, WhatsApp)."
                },
                "callType": {
                    "type": "string",
                    "description": "The type of call (audio or video)."
                }
            },
            "required": ["personName", "device", "callMedia", "callType"]
        }
    },
        {
        "type": "function",
        "name": "message",
        "description": "Send a message to contact via a messaging platform.",
        "parameters": {
            "type": "object",
            "properties": {
                "personName": {
                    "type": "string",
                    "description": "Recipient of the message."
                },
                "device": {
                    "type": "string",
                    "description": "Device to send the message from."
                },
                "messageMedia": {
                    "type": "string",
                    "description": "Messaging platform to use.e.g- internal sim, whatsapp, insta"
                },
                   "messageContent": {
                    "type": "string",
                    "description": "Message content to send for"
                }
            },
            "required": ["personName", "device", "messageMedia", "messageContent"]
        }
    },
    {
        "type": "function",
        "name": "homeControl",
        "description": "Control smart home devices like lights or fans.",
        "parameters": {
            "type": "object",
            "properties": {
                "controlledDevice": {
                    "type": "string",
                    "description": "The smart device to control.e.g - bedroom light, outdoor light,  bedroom fan, pc, home theater"
                },
                "controlledState": {
                    "type": "string",
                    "description": "The state to set (e.g., on, off)."
                }
            },
            "required": ["controlledDevice", "controlledState"]
        }
    },
    {
        "type": "function",
        "name": "ledStripMusicSync",
        "description": "Synchronize LED strip lights with music.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "type": "function",
        "name": "setLedStripLightColour",
        "description": "Set the color and brightness of the entire LED strip light.",
        "parameters": {
            "type": "object",
            "properties": {
                "rgbColourCode": {
                    "type": "string",
                    "description": "RGB color code in string format strictly, e.g. [255,0,0]."
                },
                "brightnessValue": {
                    "type": "string",
                    "description": "Brightness level as a percentage."
                }
            },
            "required": ["rgbColourCode", "brightnessValue"]
        }
    },
    {
        "type": "function",
        "name": "setLedStripLightSegmentColour",
        "description": "Set color and brightness for a specific segment of the LED strip.",
        "parameters": {
            "type": "object",
            "properties": {
                "segmentName": {
                    "type": "string",
                    "description": "Name of the segment."
                },
                "rgbColourCode": {
                    "type": "string",
                    "description": "RGB color code in string format.strictly e.g - [255,0,0]"
                },
                "brightnessValue": {
                    "type": "string",
                    "description": "Brightness level as a percentage."
                }
            },
            "required": ["segmentName", "rgbColourCode", "brightnessValue"]
        }
    },
    {
        "type": "function",
        "name": "computerVisionActivation",
        "description": "Activate or deactivate a computer vision feature such as face recognition,object detection.",
        "parameters": {
            "type": "object",
            "properties": {
                "feature": {
                    "type": "string",
                    "description": "Computer vision feature to control."
                },
                "state": {
                    "type": "string",
                    "description": "Desired state: activate or deactivate."
                }
            },
            "required": ["feature", "state"]
        }
    }
]


response = client.responses.create(
    model="gpt-4.1",
    input=[{"role": "user", "content": "turn on room light"}],
    tools=tools
)

print(response.output)
