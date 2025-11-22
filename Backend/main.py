import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os
import requests
from models.finetune.generate_itinerary import generate_itinerary  # Renamed for clarity

from typing import Optional,TypedDict
from user_api import user_api
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db  # You need a get_db dependency for SQLAlchemy session
from models import user  # Your SQLAlchemy User model
from database import engine, get_db
# from models.user import User
import uvicorn

# Load environment variables from .env
load_dotenv()

# Set API keys from environment
API_KEY = os.getenv("API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create tables
from database import Base
Base.metadata.create_all(bind=engine)

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register user_api blueprint
# app.register_blueprint(user_api)

# Weather endpoint
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

# Chat endpoint
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
        return {"reply": f"Sorry, I couldn't process your request at the moment. {e}"}

# Trip itinerary endpoint
class TripRequest(BaseModel):
    destination: str
    budget: float
    days: int
    startDate: str
    endDate: str
    transport: str
    requirement: str
    child: bool

@app.post("/trip/itinerary")
async def create_trip_itinerary(trip: TripRequest):
    try:
        # Validate dates
        if trip.startDate > trip.endDate:
            raise HTTPException(status_code=400, detail="Start date cannot be after end date")
        
        # Validate days
        if trip.days <= 0:
            raise HTTPException(status_code=400, detail="Number of days must be positive")
            
        # Validate budget
        if trip.budget <= 0:
            raise HTTPException(status_code=400, detail="Budget must be positive")
            
        result = generate_itinerary(trip.model_dump())   
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return {"itinerary": result["itinerary"]}
    except HTTPException as he:
        raise he
    except Exception as e:
        print("Error creating itinerary:", e)
        raise HTTPException(status_code=500, detail=str(e))

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return {"message": "Welcome to the Trip Planner API!"}

@app.post("/api/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = User(name=user.name, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@app.post("/api/login")
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_req.email).first()
    if not user or not pwd_context.verify(login_req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Logged in", "user_id": user.id, "name": user.name, "email": user.email}

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
