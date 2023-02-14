from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from pydantic import BaseModel
import uvicorn
import AFSignalProcessing
import predict_ecg
import json


app = FastAPI(title='Rezki')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

class PayloadECG(BaseModel):
    Lines_ECG: List
    Status: int

@app.get('/')
def welcome_():
    return {'greetings': 'welcome to my api'}

@app.post('/predict_ecg')
def fcreate_item(item: PayloadECG):
    data = json.loads(item.json())
    return predict_ecg.predict(data['Lines_ECG'], data['Status'])