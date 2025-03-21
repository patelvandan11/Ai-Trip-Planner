from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "20d8311b774127e9b4e2bec6fb727de2"

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
