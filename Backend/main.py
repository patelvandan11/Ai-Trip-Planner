import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os
from models.finetune.fine_final import ItineraryRequest
from typing import Optional
# Load environment variables
API_KEY = "2"  # Replace with your weather API key
model_id = ""
load_dotenv()

# Load environment variables
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
openai.api_key="OPENAI_API_KEY"

 
@app.get("/weather/{city}")
async def get_weather(city: str):
    if not city:
        return {"error": "City name is required"}

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()  

        data = response.json()
        if "main" not in data or "weather" not in data:
            return {"error": "Unexpected response from weather API"}

        return {
            "city": data.get("name", city),
            "temperature": round(data["main"]["temp"], 1),
            "description": data["weather"][0]["description"]
        }

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": "City not found"}
        return {"error": "Weather API error"}
    except Exception as e:
        return {"error": str(e)}
class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(message: Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI travel assistant and customer support expert."},
                {"role": "user", "content": message.message}
            ],
            max_tokens=100,
            temperature=0.7
        )
        reply = response.choices[0].message["content"].strip()
        return {"reply": reply}
    except Exception as e:
        print("OpenAI Error:", e)
        return {"reply": f"Sorry, {e}I couldn't process your request at the moment."}
# Define request model
# class TripRequest(BaseModel):
    destination: str
    budget: int
    days: int
    startDate: str
    endDate: str
    transport: str
    requirement: str
    child: bool



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
