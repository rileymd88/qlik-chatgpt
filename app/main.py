from typing import Union
from fastapi import Request, FastAPI
import requests
import pandas as pd
from datetime import datetime
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/insights")
async def insights(request: Request):
    data = await request.json()
    df = pd.DataFrame(data)
    prompt = df.iloc[0]['prompt']
    if len(prompt) > 0:
        prompt_text = prompt + ' Source data: \n'
        df.drop('prompt', axis=1, inplace=True)
        prompt_text = prompt_text + df.to_string()
        model_body = {
            "model": "text-davinci-003",
            "prompt": prompt_text,
            "max_tokens": 3000,
            "temperature": 0
        }
        headers = {
            'Authorization': f'Bearer {os.environ["CHAT_GPT_TOKEN"]}',
            'Content-Type': 'application/json'
        }
        request = requests.post('https://api.openai.com/v1/completions', headers=headers, json=model_body)
        print(request.status_code)
        chatgpt_data = request.json()

        return [{'insights_text': chatgpt_data['choices'][0]['text']}]
    else:
        return [{'insights_text': 'Please enter a prompt'}]  
    