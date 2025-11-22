from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

# Initialize the model
model = ChatOpenAI(model="gpt-4o-mini-2024-07-18")

# Define schema compatible with OpenAI's structured output
class Review(BaseModel):
    day1_date: str = Field(..., description="Date for Day 1 in YYYY-MM-DD format")
    day1_activities: List[str] = Field(..., description="List of all activities for Day 1")
    
    day2_date: str = Field(..., description="Date for Day 2 in YYYY-MM-DD format") 
    day2_activities: List[str] = Field(..., description="List of all activities for Day 2")
    
    day3_date: str = Field(..., description="Date for Day 3 in YYYY-MM-DD format")
    day3_activities: List[str] = Field(..., description="List of all activities for Day 3")

# Apply structured output with function_calling method
structured_model = model.with_structured_output(Review, method="function_calling")

# Enhanced prompt to ensure better day-wise grouping
enhanced_prompt = """
Please extract the itinerary information and organize it by days. For each day, group ALL activities that happen on that specific day together.

Structure the response as:
- Day1: All activities happening on the first day 
- Day2: All activities happening on the second day 
- Day3: All activities happening on the third day 
so on

Make sure each activity is listed under the correct day, regardless of what time of day it occurs.

Here's the itinerary data:
"""

# Input data
data = """
Sure! Here’s a detailed day-by-day itinerary for your trip to Manali, keeping in mind your budget of $2500 for 3 days, traveling by train, and your travel style.

### Day 1: Arrival in Manali
**Date: 2025-05-28**

#### Morning:
- **6:00 AM**: Depart from your location by train (check the nearest station and schedule).
- **Travel cost**: Approximately $50-100 for a round trip, depending on your departure city.

#### Afternoon:
- **11:00 AM**: Arrive in Manali. Head to your hotel.
- **Accommodation**: Check into a budget hotel (e.g., Hotel Hilltop or similar).
  - **Cost**: Approximately $50-80 per night.

#### Lunch:
- **1:00 PM**: Lunch at **The Lazy Dog** (local cuisine).
  - **Cost**: $10-15 per person.

#### Afternoon Activities:
- **2:30 PM**: Visit **Hadimba Devi Temple**.
  - **Cost**: Free entry.
  - **Duration**: 1 hour.
- **3:30 PM**: Explore the **Manu Temple**.
  - **Cost**: Free entry.
  - **Duration**: 1 hour.

#### Evening:
- **5:00 PM**: Stroll through **Mall Road**, shop for souvenirs.
  - **Cost**: Variable; budget $20-30 for shopping.
- **7:00 PM**: Dinner at **Johnson’s Lodge** (great local dishes).
  - **Cost**: $15-20 per person.

#### Night:
- **9:00 PM**: Return to the hotel and rest.

### Day 2: Adventure and Sightseeing
**Date: 2025-05-29**

#### Morning:
- **8:00 AM**: Breakfast at the hotel.
- **Cost**: Included in accommodation.
- **9:00 AM**: Head to **Solang Valley** for adventure activities (paragliding, zorbing).
  - **Transportation**: Hire a taxi or shared cab.
  - **Cost**: Approximately $20-30 round trip.

#### Activities:
- **10:00 AM**: Arrive at Solang Valley.
  - **Cost for activities**: Paragliding ($40) + Zorbing ($15).
  - **Total duration**: 3 hours.

#### Lunch:
- **1:30 PM**: Lunch at **Solang Valley Café**.
  - **Cost**: $10-15 per person.

#### Afternoon:
- **3:00 PM**: Head to **Gulmarg** or **Rohtang Pass** (check road conditions).
  - **Cost**: Transportation $30-50.
  - **Activities**: Explore scenic views and take photos.
  - **Duration**: 3 hours.

#### Evening:
- **6:00 PM**: Return to Manali.
- **8:00 PM**: Dinner at **The Corner House**.
  - **Cost**: $15-20 per person.

#### Night:
- **9:30 PM**: Return to the hotel and rest.

### Day 3: Local Culture and Departure
**Date: 2025-05-30**

#### Morning:
- **8:00 AM**: Breakfast at the hotel.
- **Cost**: Included.
- **9:00 AM**: Visit the **Vashisht Village** and soak in the hot springs.
  - **Cost**: Free entry.
  - **Duration**: 2 hours.

#### Lunch:
- **12:00 PM**: Lunch at **Vashisht Café**.
  - **Cost**: $10-15 per person.

#### Afternoon:
- **1:30 PM**: Visit **Manali Sanctuary** for a nature walk.
  - **Cost**: $5 for entry.
  - **Duration**: 1.5 hours.

#### Evening:
- **3:00 PM**: Head to **Old Manali** for some quiet time and scenic views.
  - **Cost**: Free.
- **5:00 PM**: Prepare for departure.
- **6:00 PM**: Early dinner at **The Café 1947**.
  - **Cost**: $15-20 per person.

#### Departure:
- **7:30 PM**: Head to the train station for your departure.
- **8:30 PM**: Train back to your original location.
- **Travel cost**: Included in the initial round trip.

### Estimated Costs Summary:
- **Accommodation**: $150-240 for 3 nights.
- **Food**: $120-180 for 3 days.
- **Transportation**: $100-150 (local).
- **Activities**: $100-150.
- **Shopping and Miscellaneous**: $50-100.
- **Total Estimated Cost**: $620-1020, well within your $2500 budget.

### Special Considerations:
- Ensure to check the weather in advance and pack accordingly.
- Book accommodation and major activities in advance to avoid last-minute issues.
- Always have cash on hand for small expenses, as not all locations accept credit cards.
- Since you are not traveling with children, you can enjoy more adventurous activities at your leisure.

Enjoy your trip to Manali!
"""

# Combine prompt and data
full_input = enhanced_prompt + data

# 🛠️ Pass the input to `.invoke()`
result = structured_model.invoke(full_input)
result_json = result.model_dump_json(indent=2)

# Print the structured output
print("Structured Output:")
print(result_json)

# Convert to your desired format
import json
result_dict = json.loads(result_json)

# Transform to day-wise dictionary format
formatted_output = {
    "days": {
        "Day1": {
            "date": result_dict["day1_date"],
            "activities": result_dict["day1_activities"]
        },
        "Day2": {
            "date": result_dict["day2_date"], 
            "activities": result_dict["day2_activities"]
        },
        "Day3": {
            "date": result_dict["day3_date"],
            "activities": result_dict["day3_activities"]
        }
    }
}

print("\n" + "="*50)
print("Formatted Output:")
print(json.dumps(formatted_output, indent=2))