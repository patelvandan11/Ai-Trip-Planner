import openai
import os
from dotenv import load_dotenv
from typing import Dict, Annotated, Optional, Literal
from pydantic import BaseModel, Field
# Load environment variables from .env
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Use fine-tuned model or fallback
# fine_tune_model = os.getenv("FINE_TUNE_MODEL")

class ItineraryRequest(BaseModel):
    days: int = Field(..., ge=1, description="Number of days for the trip")
    

def generate_itinerary(data: Dict) -> Dict:
    """
    Generate an itinerary using OpenAI ChatCompletion API.

    Args:
        data (dict): Input data including destination, budget, days, etc.

    Returns:
        dict: A response containing the itinerary or an error message.
    """
    try:
        # Validate required fields
        required_fields = ['destination', 'budget', 'days', 'startDate', 'endDate', 'transport', 'requirement']
        for field in required_fields:
            if not data.get(field):
                return {"error": f"Missing required field: {field}"}

        prompt = f"""
Create a detailed day-by-day itinerary for:
- Destination: {data.get('destination')}
- Budget: ${data.get('budget')}
- Duration: {data.get('days')} days
- Travel Dates: {data.get('startDate')} to {data.get('endDate')}
- Transportation: {data.get('transport')}
- Travel Style: {data.get('requirement')}
- Travelling with children: {'Yes' if data.get('child') else 'No'}

Please include:
1. Daily schedule with timings
2. Recommended attractions and activities
3. Estimated costs for each activity
4. Transportation details between locations
5. Dining recommendations
6. Any special considerations based on the travel style and children status
"""
        response = openai.ChatCompletion.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:ai-trip-planner-final:BTKhoUKU",
            messages=[
                {"role": "system", "content": "You are an AI travel assistant specializing in creating detailed, personalized travel itineraries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        reply = response.choices[0].message["content"].strip()
        
        
        return {"itinerary": reply}
    except openai.error.AuthenticationError:
        return {"error": "OpenAI API authentication failed. Please check your API key."}
    except openai.error.RateLimitError:
        return {"error": "OpenAI API rate limit exceeded. Please try again later."}
    except Exception as e:
        print("OpenAI Error:", e)
        return {"error": f"Failed to generate itinerary: {str(e)}"}


# print(generate_itinerary({
#     "destination": "Manali",
#     "budget": 25000,
#     "days": 4,
#     "startDate": "2025-06-01",
#     "endDate": "2025-06-04",
#     "transport": "Train",
#     "requirement": "Include adventure sports and nature spots",
#     "child": False
# }))