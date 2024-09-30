from openai import OpenAI
import os
os.getenv("OPENAI_API_KEY") # check to see if there
### Quick start
client = OpenAI()
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "write a haiku about ai"}
    ]
)
