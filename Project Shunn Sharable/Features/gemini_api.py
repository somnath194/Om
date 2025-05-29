# import google.generativeai as genai
# api_key = "AIzaSyDcIkpMorPJmaQfHN6wAIOAi1GNv4vEsoo"

# genai.configure(api_key="api_key")

# model = genai.GenerativeModel(model_name='gemini-1.5-flash')

# response = model.generate_content("Write a poem about the moon.")
# print(response.text)

api = "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"
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="<api>",
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="meta-llama/llama-3.3-70b-instruct:free",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)