# Import required A2A protocol components and utilities
from python_a2a import A2AServer, Message, TextContent, MessageRole, run_server
import json
import os

class HotelAgent(A2AServer):
    """
    Hotel Recommendation Agent that suggests hotels based on location and weather conditions
    Inherits from A2AServer to implement the A2A protocol
    """
    def handle_message(self, message):
        # Process only text-based messages
        if message.content.type == "text":
            # Clean and normalize the input query
            query = message.content.text.strip().lower()
            
            # Hotel database structured as nested dictionaries
            # Primary key: city name
            # Secondary key: weather condition (default, sunny, rainy)
            # Values: Lists of hotel recommendations with descriptions
            hotels = {
                "tokyo": {
                    "default": [
                        "Grand Tokyo Hotel - Near city center, indoor pool, 5-star",
                        "Budget Inn Tokyo - Economic option with free breakfast"
                    ],
                    "sunny": [
                        "Tokyo Bay Resort - Beachfront property with outdoor activities",
                        "Shinjuku Garden Hotel - Rooftop bar with city views"
                    ],
                    "rainy": [
                        "Tokyo Dome Hotel - Connected to shopping mall and entertainment",
                        "Asakusa Ryokan - Traditional Japanese inn with indoor onsen"
                    ]
                },
                "new york": {
                    "default": [
                        "Manhattan Suites - Central location, luxury accommodations",
                        "Brooklyn Boutique Hotel - Hip neighborhood, rooftop bar"
                    ],
                    "sunny": [
                        "Central Park View Hotel - Rooms overlooking the park",
                        "SoHo Loft Hotel - Outdoor terrace and walking distance to shops"
                    ],
                    "rainy": [
                        "Times Square Mega Hotel - Indoor entertainment and dining",
                        "Museum Mile Lodge - Near major museums and indoor attractions"
                    ]
                },
                "paris": {
                    "default": [
                        "Seine River Hotel - Classic Parisian views",
                        "Montmartre Boutique - Artistic neighborhood and charm"
                    ]
                },
                "london": {
                    "default": [
                        "Kensington Luxury Hotel - Elegant rooms with afternoon tea service",
                        "Shoreditch Urban Lodge - Modern design in trendy area"
                    ]
                }
            }
            
            # Parse the query to identify the requested city
            city_key = None
            for city in hotels.keys():
                if city in query:
                    city_key = city
                    break
            
            # Determine weather condition from the query
            # Default to "default" if no weather condition is specified
            weather_type = "default"
            if "sunny" in query:
                weather_type = "sunny"
            elif "rainy" in query or "cloudy" in query or "foggy" in query:
                weather_type = "rainy"
            
            # Generate appropriate response based on available data
            if city_key:
                city_hotels = hotels[city_key]
                # Try to get weather-specific recommendations, fall back to default if not available
                hotel_list = city_hotels.get(weather_type, city_hotels["default"])
                response_text = f"Recommended hotels in {city_key.title()}: {'; '.join(hotel_list)}"
            else:
                # Return helpful message if city not found in database
                response_text = "No hotel information available for this location. We currently have data for: Tokyo, New York, Paris, and London."
            
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
        "name": "Hotel Recommendation Agent",
        "description": "Recommends hotels based on location and weather conditions",
        "version": "1.0.0",
        "skills": [{"name": "findHotels", "description": "Find hotels in a specified location considering weather"}]
    }
    # Ensure .well-known directory exists
    os.makedirs(".well-known", exist_ok=True)
    # Write agent card to JSON file
    with open(".well-known/agent.json", "w") as f:
        json.dump(card, f)

if __name__ == "__main__":
    # Initialize the agent when running the script directly
    create_agent_card()
    agent = HotelAgent()
    print("Hotel Agent running on port 5002...")
    # Start the server on all network interfaces (0.0.0.0) on port 5002
    run_server(agent, host="0.0.0.0", port=5002)