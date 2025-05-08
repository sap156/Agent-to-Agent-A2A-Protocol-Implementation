# Import required A2A protocol components and utilities
from python_a2a import A2AServer, Message, TextContent, MessageRole, run_server
import json
import os

class ActivityAgent(A2AServer):
    """
    Activity Recommendation Agent that suggests activities based on location, weather, and user context
    Inherits from A2AServer to implement the A2A protocol
    """
    def handle_message(self, message):
        # Process only text-based messages
        if message.content.type == "text":
            # Clean and normalize the input query
            query = message.content.text.strip().lower()
            
            # Activity database structured as nested dictionaries
            # Primary key: city name
            # Secondary key: weather condition (sunny, rainy, default)
            # Values: Lists of recommended activities for each condition
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
            
            # Extract city name from query by checking if any supported city is mentioned
            city_key = None
            for city in activities.keys():
                if city in query:
                    city_key = city
                    break
            
            # Determine weather type from query keywords
            # Default to "default" if no weather condition is specified
            weather_type = "default"
            if "sunny" in query:
                weather_type = "sunny"
            elif any(w in query for w in ["rainy", "cloudy", "foggy", "humid"]):
                weather_type = "rainy"
            
            # Generate appropriate response based on available data
            if city_key and city_key in activities:
                city_activities = activities[city_key]
                # Try to get weather-specific activities, fall back to default if not available
                activity_list = city_activities.get(weather_type, city_activities["default"])
                response_text = f"Recommended activities in {city_key.title()}: {', '.join(activity_list)}"
                
                # Add contextual recommendations based on hotel location/type
                if "city center" in query or "central" in query:
                    response_text += "\n\nSince your hotel is centrally located, you can easily access most attractions by walking or short metro rides."
                elif "budget" in query or "economic" in query:
                    response_text += "\n\nFor budget travelers, consider purchasing a city pass for discounted admission to multiple attractions."
            else:
                # Return helpful message if city not found in database
                response_text = "No activity recommendations available for this location. We currently have data for: Tokyo, New York, Paris, and London."
            
            # Construct and return the response message
            # Maintains conversation context through conversation_id and parent_message_id
            return Message(
                content=TextContent(text=response_text),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )

def create_agent_card():
    """
    Creates an agent card in .well-known/agent.json
    This card describes the agent's capabilities and metadata
    following the A2A protocol specifications
    """
    card = {
        "name": "Activity Recommendation Agent",
        "description": "Suggests activities based on location, weather, and accommodation",
        "version": "1.0.0",
        "skills": [{"name": "suggestActivities", "description": "Suggest activities for a location based on weather and preferences"}]
    }
    # Ensure .well-known directory exists
    os.makedirs(".well-known", exist_ok=True)
    # Write agent card to JSON file
    with open(".well-known/agent.json", "w") as f:
        json.dump(card, f)

if __name__ == "__main__":
    # Initialize the agent when running the script directly
    create_agent_card()
    agent = ActivityAgent()
    print("Activity Agent running on port 5003...")
    # Start the server on all network interfaces (0.0.0.0) on port 5003
    run_server(agent, host="0.0.0.0", port=5003)