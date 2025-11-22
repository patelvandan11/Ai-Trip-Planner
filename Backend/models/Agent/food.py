import openai
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict, List, Dict, Any
import json

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Define State Schema ---
class TripPlannerState(TypedDict):
    destination: str
    budget: int
    days: int
    startDate: str
    endDate: str
    transport: str
    requirement: str
    child: bool
    itinerary: Dict[str, Any]
    user_feedback: str
    feedback_count: int
    is_approved: bool

# --- Step 1: Collect user input ---
def collect_preferences(state: TripPlannerState) -> TripPlannerState:
    try:
        print("\n🧳 Let's plan your trip!")
        state["destination"] = input("Enter destination (e.g., Paris): ").lower()
        state["budget"] = int(input("Enter budget (in USD): "))
        state["days"] = int(input("Enter trip duration (in days): "))
        state["startDate"] = input("Enter start date (YYYY-MM-DD): ")
        state["endDate"] = input("Enter end date (YYYY-MM-DD): ")
        state["transport"] = input("Enter preferred transport (Train/Car/Flight): ")
        state["requirement"] = input("Enter travel style/requirements: ")
        state["child"] = input("Traveling with children? (yes/no): ").lower() == "yes"
        state["feedback_count"] = 0
        state["is_approved"] = False
        return state
    except ValueError as e:
        print(f"⚠️ Error in input: {str(e)}")
        raise

# --- Step 2: Generate itinerary using GPT ---
def generate_itinerary(state: TripPlannerState) -> TripPlannerState:
    """Generate itinerary using OpenAI API."""
    try:
        prompt = f"""
Create a detailed day-by-day itinerary for:
- Destination: {state['destination']}
- Budget: ${state['budget']}
- Duration: {state['days']} days
- Travel Dates: {state['startDate']} to {state['endDate']}
- Transportation: {state['transport']}
- Travel Style: {state['requirement']}
- Travelling with children: {'Yes' if state.get('child') else 'No'}

Please structure the response in the following format:

**{state['days']}-Day Itinerary for {state['destination']} ({state['startDate']} - {state['endDate']})**
**Budget:** ${state['budget']}
**Travel Style:** {state['requirement']}
**Traveling with Children:** {'Yes' if state.get('child') else 'No'}

### Day 1: [Date]

#### Morning
- **[Time]**: [Activity]
  - **Location**: [Place]
  - **Cost**: [Amount]
  - **Duration**: [Time needed]
  - **Transportation**: [Details]

#### Afternoon
- **[Time]**: [Activity]
  - **Location**: [Place]
  - **Cost**: [Amount]
  - **Duration**: [Time needed]
  - **Transportation**: [Details]

#### Evening
- **[Time]**: [Activity]
  - **Location**: [Place]
  - **Cost**: [Amount]
  - **Duration**: [Time needed]
  - **Transportation**: [Details]

[Repeat for each day]

### Overall Cost Breakdown
- **Accommodation**: [Total cost]
- **Transportation**: [Total cost]
- **Activities**: [Total cost]
- **Meals**: [Total cost]
- **Other**: [Total cost]
- **Total Estimated Cost**: [Total amount]

### Special Considerations
- [Important tip 1]
- [Important tip 2]
"""
        response = openai.ChatCompletion.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:ai-trip-planner-final:BTKhoUKU",
            messages=[
                {"role": "system", "content": "You are an AI travel assistant specializing in creating detailed, personalized travel itineraries. Always follow the exact format provided in the prompt."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        reply = response.choices[0].message["content"].strip()
        
        # Structure the response for frontend display
        structured_response = {
            "title": f"{state['days']}-Day Itinerary for {state['destination']}",
            "dates": f"{state['startDate']} - {state['endDate']}",
            "budget": f"${state['budget']}",
            "travelStyle": state['requirement'],
            "withChildren": state.get('child', False),
            "rawItinerary": reply,
            "formattedItinerary": {
                "days": [],
                "costBreakdown": {},
                "specialConsiderations": []
            }
        }
        
        # Parse the raw itinerary into structured format
        current_day = None
        current_section = None
        
        for line in reply.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('### Day'):
                current_day = {
                    "day": line.replace('### ', ''),
                    "sections": {
                        "morning": [],
                        "afternoon": [],
                        "evening": []
                    }
                }
                structured_response["formattedItinerary"]["days"].append(current_day)
            elif line.startswith('####'):
                current_section = line.replace('#### ', '').lower()
            elif line.startswith('- **'):
                if current_day and current_section:
                    activity = {
                        "time": line.split('**: ')[0].replace('- **', ''),
                        "description": line.split('**: ')[1],
                        "details": []
                    }
                    current_day["sections"][current_section].append(activity)
            elif line.startswith('  - **'):
                if current_day and current_section and current_day["sections"][current_section]:
                    detail = line.replace('  - **', '').split('**: ')
                    current_day["sections"][current_section][-1]["details"].append({
                        "type": detail[0],
                        "value": detail[1]
                    })
            elif line.startswith('### Overall Cost Breakdown'):
                current_section = "costBreakdown"
            elif line.startswith('### Special Considerations'):
                current_section = "specialConsiderations"
            elif current_section == "costBreakdown" and line.startswith('- **'):
                cost_item = line.replace('- **', '').split('**: ')
                structured_response["formattedItinerary"]["costBreakdown"][cost_item[0]] = cost_item[1]
            elif current_section == "specialConsiderations" and line.startswith('- '):
                structured_response["formattedItinerary"]["specialConsiderations"].append(line.replace('- ', ''))
        
        state["itinerary"] = structured_response
        return state
        
    except openai.error.AuthenticationError:
        raise ValueError("OpenAI API authentication failed. Please check your API key.")
    except openai.error.RateLimitError:
        raise ValueError("OpenAI API rate limit exceeded. Please try again later.")
    except Exception as e:
        raise ValueError(f"Failed to generate itinerary: {str(e)}")

# --- Step 3: Show itinerary & ask feedback ---
def ask_feedback(state: TripPlannerState) -> TripPlannerState:
    try:
        print("\n📅 Here's your suggested itinerary:")
        print(json.dumps(state["itinerary"], indent=2))
        state["user_feedback"] = input("Do you like this itinerary? (yes/no): ").strip().lower()
        return state
    except Exception as e:
        print(f"⚠️ Error displaying itinerary: {str(e)}")
        raise

# --- Step 4: Update state based on feedback ---
def update_feedback_state(state: TripPlannerState) -> TripPlannerState:
    try:
        if state["user_feedback"] == "yes":
            state["is_approved"] = True
        else:
            state["feedback_count"] += 1
        return state
    except Exception as e:
        print(f"⚠️ Error updating feedback state: {str(e)}")
        raise

# --- Step 5: Conditional branching logic ---
def itinerary_decision(state: TripPlannerState) -> str:
    try:
        if state["is_approved"]:
            return END
        elif state["feedback_count"] >= 2:
            print("❌ Too many rejections. Finalizing last itinerary.")
            return END
        else:
            return "generate"
    except Exception as e:
        print(f"⚠️ Error in decision logic: {str(e)}")
        raise

# --- Step 6: Define and build the graph ---
try:
    graph = StateGraph(TripPlannerState)
    graph.add_node("collect", collect_preferences)
    graph.add_node("generate", generate_itinerary)
    graph.add_node("feedback", ask_feedback)
    graph.add_node("update", update_feedback_state)

    graph.set_entry_point("collect")
    graph.add_edge("collect", "generate")
    graph.add_edge("generate", "feedback")
    graph.add_edge("feedback", "update")

    graph.add_conditional_edges(
        "update",
        itinerary_decision,
        {
            END: END,
            "generate": "generate"
        }
    )

    # --- Compile the graph ---
    app = graph.compile()
except Exception as e:
    print(f"⚠️ Error building graph: {str(e)}")
    raise

# --- Step 7: Run the App ---
if __name__ == "__main__":
    try:
        initial_state = {
            "destination": "",
            "budget": 0,
            "days": 0,
            "startDate": "",
            "endDate": "",
            "transport": "",
            "requirement": "",
            "child": False,
            "itinerary": {},
            "user_feedback": "",
            "feedback_count": 0,
            "is_approved": False
        }

        final_state = app.invoke(initial_state)

        print("\n✅ Final Approved Itinerary:")
        print(json.dumps(final_state["itinerary"], indent=2))
    except Exception as e:
        print(f"⚠️ Error running the application: {str(e)}")
        raise
