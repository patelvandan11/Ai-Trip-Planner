from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from dotenv import load_dotenv
from pydantic import BaseModel
import openai
import os
from models.finetune.fine_final import ItineraryRequest
from typing import Optional
# Load environment variables
load_dotenv()
API_KEY = "WEATHER_API"  # Replace with your weather API key
model_id = ""
openai.api_key = "OPENAI_API_KEY"  # Replace with your OpenAI API key

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


 
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
            temperature=0.7,
        )
        reply = response.choices[0].message["content"].strip()
        return {"reply": reply}
    except Exception as e:
        print("OpenAI Error:", e)
        return {"reply": "Sorry, I couldn't process your request at the moment."}
# Define request model
class TripRequest(BaseModel):
    destination: str
    budget: int
    days: int
    startDate: str
    endDate: str
    transport: str
    requirement: str
    child: bool

@app.post("/generate")
async def generate_itinerary(req: TripRequest):
    try:
        # Create a detailed prompt for the AI
        prompt = f"""Create a detailed day-by-day itinerary for a {req.days}-day trip to {req.destination}.
        
Trip Details:
- Budget: ${req.budget}
- Transportation: {req.transport}
- Style: {req.requirement}
- Traveling with children: {"Yes" if req.child else "No"}
- Dates: {req.startDate} to {req.endDate}

Please provide a detailed itinerary with the following format for each day:
Day X: [Day Title]
- [Activity 1 with time and brief description]
- [Activity 2 with time and brief description]
- [Activity 3 with time and brief description]
- [Restaurant recommendations]
- [Transportation details between activities]

Make sure to:
1. Include specific times for activities
2. Consider the budget constraints
3. Account for travel time between locations
4. Include family-friendly activities if traveling with children
5. Suggest restaurants that match the budget and style
6. Provide practical transportation tips
7. Include some free or low-cost activities
8. Consider local customs and peak hours

Format the response with clear day-by-day sections separated by newlines."""

        # Generate the itinerary using OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional travel planner with extensive knowledge of destinations worldwide. Provide detailed, practical, and well-structured itineraries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        if not response.choices or not response.choices[0].message.content:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate itinerary: Empty response from OpenAI"
            )

        itinerary = response.choices[0].message.content.strip()
        
        if not itinerary:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate itinerary: Empty itinerary content"
            )

        return {"itinerary": itinerary, "status": "success"}

    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI API Error: {str(e)}"
        )
    except Exception as e:
        print(f"Error generating itinerary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate itinerary: {str(e)}"
        )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
