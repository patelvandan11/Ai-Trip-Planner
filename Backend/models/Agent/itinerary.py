import openai
import os
from dotenv import load_dotenv
from typing import Dict, Optional, TypedDict
from langgraph.graph import StateGraph, END

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ItineraryState(TypedDict, total=False):
    destination: str
    budget: int
    days: int
    startDate: str
    endDate: str
    transport: str
    requirement: str
    child: Optional[bool]
    prompt: Optional[str]
    itinerary: Optional[str]
    error: Optional[str]

def validate_input(state: ItineraryState) -> ItineraryState:
    required_fields = ['destination', 'budget', 'days', 'startDate', 'endDate', 'transport', 'requirement']
    for field in required_fields:
        if not state.get(field):
            return {"error": f"Missing required field: {field}"}
    return state

def create_prompt(state: ItineraryState) -> ItineraryState:
    prompt = f"""
Create a detailed day-by-day itinerary for:
- Destination: {state['destination']}
- Budget: ${state['budget']}
- Duration: {state['days']} days
- Travel Dates: {state['startDate']} to {state['endDate']}
- Transportation: {state['transport']}
- Travel Style: {state['requirement']}
- Travelling with children: {'Yes' if state.get('child') else 'No'}

Please include:
1. Daily schedule with timings
2. Recommended attractions and activities
3. Estimated costs for each activity
4. Transportation details between locations
5. Dining recommendations
6. Any special considerations based on the travel style and children status
"""
    state["prompt"] = prompt
    return state

def call_openai(state: ItineraryState) -> ItineraryState:
    
        response = openai.ChatCompletion.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:ai-trip-planner-final:BTKhoUKU",
            messages=[
                {"role": "system", "content": "You are an AI travel assistant specializing in creating detailed, personalized travel itineraries."},
                {"role": "user", "content": state["prompt"]}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        state["itinerary"] = response.choices[0].message["content"].strip()
        return state
    

def return_result(state: ItineraryState) -> Dict:
    if "error" in state:
        return {"error": state["error"]}
    return {"itinerary": state["itinerary"]}


graph = StateGraph(state_schema=ItineraryState)
graph.add_node("validate", validate_input)
graph.add_node("create_prompt", create_prompt)
graph.add_node("call_openai", call_openai)
graph.add_node("return_result", return_result)

graph.set_entry_point("validate")
graph.add_edge("validate", "create_prompt")
graph.add_edge("create_prompt", "call_openai")
graph.add_edge("call_openai", "return_result")
graph.add_edge("return_result", END)

graph = graph.compile()

if __name__ == "__main__":
    result = graph.invoke({
        "destination": "Manali",
        "budget": 25000,
        "days": 4,
        "startDate": "2025-06-01",
        "endDate": "2025-06-04",
        "transport": "Train",
        "requirement": "Include adventure sports and nature spots",
        "child": False
    })
    print(result)
    