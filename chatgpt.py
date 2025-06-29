# kkey things
# make sure there is money in the account
# make sure you spell the model right. it isn't chatgpt...it's gpt
from openai import OpenAI
import os
# a=os.getenv("OPENAI_API_KEY") # check to see if there
# print(a)
### Quick start
client = OpenAI()
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "write a haiku about ai"}
    ]
)
print(completion.choices[0].message.content)
