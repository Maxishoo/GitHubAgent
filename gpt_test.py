from dotenv import load_dotenv
load_dotenv()
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.environ.get("OPENAI_API_BASE"),
    api_key=os.environ.get("OPENROUTER_API_KEY")
)
MODEL = os.environ.get("OPENAI_MODEL")

response = client.chat.completions.create(
  model=MODEL,
  messages=[
          {
            "role": "user",
            "content": "How many r's are in the word 'strawberry'?"
          }
        ],
  extra_body={"reasoning": {"enabled": True}}
)

response = response.choices[0].message

messages = [
  {"role": "user", "content": "How many r's are in the word 'strawberry'?"},
  {
    "role": "assistant",
    "content": response.content,
    "reasoning_details": response.reasoning_details
  },
  {"role": "user", "content": "Are you sure? Think carefully."}
]

response2 = client.chat.completions.create(
  model="openai/gpt-oss-120b:free",
  messages=messages,
  extra_body={"reasoning": {"enabled": True}}
)
print(response2)