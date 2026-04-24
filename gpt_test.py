# from openai import OpenAI

# client = OpenAI(
#     base_url="https://aiapiv2.pekpik.com/v1",
#     api_key="sk-OjGyrUJPJUoIkgvCtpgV5KQ3Ym0HBIyCAms0SO1Vl5NkrHjJ"
# )

# response = client.chat.completions.create(
#     model="smart-chat",
#     messages=[{"role": "user", "content": "напиши код на питоне для сложения двух чисел"}]
# )
# print(response.choices[0].message.content)

# Please install OpenAI SDK first: `pip3 install openai`
from dotenv import load_dotenv
load_dotenv()
import os

from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

# First API call with reasoning
response = client.chat.completions.create(
  model="openai/gpt-oss-120b:free",
  messages=[
          {
            "role": "user",
            "content": "How many r's are in the word 'strawberry'?"
          }
        ],
  extra_body={"reasoning": {"enabled": True}}
)

# Extract the assistant message with reasoning_details
response = response.choices[0].message

# Preserve the assistant message with reasoning_details
messages = [
  {"role": "user", "content": "How many r's are in the word 'strawberry'?"},
  {
    "role": "assistant",
    "content": response.content,
    "reasoning_details": response.reasoning_details  # Pass back unmodified
  },
  {"role": "user", "content": "Are you sure? Think carefully."}
]

# Second API call - model continues reasoning from where it left off
response2 = client.chat.completions.create(
  model="openai/gpt-oss-120b:free",
  messages=messages,
  extra_body={"reasoning": {"enabled": True}}
)
print(response2)