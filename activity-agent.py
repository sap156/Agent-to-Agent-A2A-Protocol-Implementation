from python_a2a import A2AServer, Message, TextContent, MessageRole, run_server
import json
import os

class ActivityAgent(A2AServer):
    def handle_message(self, message):
        if message.content.type == "text":
            query = message.content.text.strip().lower()
            
            # Activity database
            activities = {
                "tokyo": {
                    "sunny": ["Visit Tokyo Skytree", "Explore Meiji Shrine", "Shop in Ginza", "Picnic in Yoyogi Park"],
                    "rainy": ["Tokyo National Museum", "TeamLab Borderless digital art", "Shopping at underground malls", "Ramen tour in basement food courts"],
                    "default": ["Tokyo Disneyland", "Try local cuisine in Shinjuku", "Visit Akihabara electronics district"]
                },
                "new york": {
                    "sunny": ["Central Park walk", "Top of the Rock observation deck", "High Line park", "Staten Island Ferry for Statue of Liberty views"],
                    "rainy": ["Metropolitan Museum of Art", "American Museum of Natural History", "Broadway show", "Shopping in SoHo"],
                    "default": ["Times Square", "Empire State Building", "Statue of Liberty", "Brooklyn Bridge walk"]
                },
                "paris": {
                    "sunny": ["Luxembourg Gardens", "Seine River cruise", "Montmartre walking tour"],
                    "rainy": ["Louvre Museum", "Galeries Lafayette shopping", "Parisian cafés for hot chocolate"],
                    "default": ["Eiffel Tower", "Notre-Dame Cathedral", "Arc de Triomphe"]
                },
                "london": {
                    "sunny": ["Hyde Park boat ride", "London Eye", "Buckingham Palace changing of the guard"],
                    "rainy": ["British Museum", "National Gallery", "Shopping at Harrods", "Traditional afternoon tea"],
                    "default": ["Tower of London", "Westminster Abbey", "Thames River cruise"]
                }
            }
            
            # Extract city name from query
            city_key = None
            for city in activities.keys():
                if city in query:
                    city_key = city
                    break
            
            # Determine weather type from query
            weather_type = "default"
            if "sunny" in query:
                weather_type = "sunny"
            elif any(w in query for w in ["rainy", "cloudy", "foggy", "humid"]):
                weather_type = "rainy"
            
            if city_key and city_key in activities:
                city_activities = activities[city_key]
                activity_list = city_activities.get(weather_type, city_activities["default"])
                response_text = f"Recommended activities in {city_key.title()}: {', '.join(activity_list)}"
                
                # Add context-specific recommendations based on hotel location
                if "city center" in query or "central" in query:
                    response_text += "\n\nSince your hotel is centrally located, you can easily access most attractions by walking or short metro rides."
                elif "budget" in query or "economic" in query:
                    response_text += "\n\nFor budget travelers, consider purchasing a city pass for discounted admission to multiple attractions."
            else:
                response_text = "No activity recommendations available for this location. We currently have data for: Tokyo, New York, Paris, and London."
            
            return Message(
                content=TextContent(text=response_text),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )

# Create agent card
def create_agent_card():
    card = {
        "name": "Activity Recommendation Agent",
        "description": "Suggests activities based on location, weather, and accommodation",
        "version": "1.0.0",
        "skills": [{"name": "suggestActivities", "description": "Suggest activities for a location based on weather and preferences"}]
    }
    os.makedirs(".well-known", exist_ok=True)
    with open(".well-known/agent.json", "w") as f:
        json.dump(card, f)

if __name__ == "__main__":
    create_agent_card()
    agent = ActivityAgent()
    print("Activity Agent running on port 5003...")
    run_server(agent, host="0.0.0.0", port=5003)