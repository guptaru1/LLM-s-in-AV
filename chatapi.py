import time

import vertexai
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.language_models import ChatModel

# for ChatGPT
import openai
from openai import OpenAI
import anthropic


class ChatBot():

    def __init__(self, model, max_attempts = 20):
        self.model = model
        self.max_attempts = max_attempts

    def chat(self, system_prompt, user_prompt):
        if "gpt" in self.model.lower():
            return self.chat_gpt(system_prompt, user_prompt)
        elif "claude" in self.model.lower():
            return self.chat_claude(system_prompt, user_prompt)
        
    def chat_gpt(self, system_prompt, user_prompt):
        attempt = 0
        while attempt < self.max_attempts:
                try:
                     print("trying to work")
                     message = client.chat.completions.create(
                          model="gpt-4",
                          messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                     )
                     print("message successful", message)
                     response = message['choices'][0]['message']['content']
                     print("my response was succesful", response)
                     return response
                except openai.APIError as e:
                    print("Error encoruntered", e)
                    time.sleep(5)
                    attempt = attempt + 1

        return None
    
    def chat_claude(self, system_prompt, user_prompt):
        attempt = 0
        while attempt < self.max_attempts:
            try:
                time.sleep(1)
                response = client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    temperature=0,
                    system=system_prompt,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": user_prompt
                                }
                            ]
                        }
                    ]
                )
                response_text = response.content[0].text
                print("my response", response_text)
                return response_text

            except Exception as e:
                attempt = attempt + 1
                if "rate_limit_error" in str(e):
                    raise ValueError("rate limit error")
                else:
                    print(str(e))
                    time.sleep(5)
        
        return None
    
                     
