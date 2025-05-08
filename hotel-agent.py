from python_a2a import A2AServer, Message, TextContent, MessageRole, run_server
import json
import os

class HotelAgent(A2AServer):
    def handle_message(self, message):
        if message.content.type == "text":
            query = message.content.text.strip().lower()
            
            # Hotel database with weather-specific recommendations
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
            
            # Extract city name from query
            city_key = None
            for city in hotels.keys():
                if city in query:
                    city_key = city
                    break
            
            # Determine weather condition
            weather_type = "default"
            if "sunny" in query:
                weather_type = "sunny"
            elif "rainy" in query or "cloudy" in query or "foggy" in query:
                weather_type = "rainy"
            
            if city_key:
                city_hotels = hotels[city_key]
                # Get weather-specific hotels if available, otherwise use default
                hotel_list = city_hotels.get(weather_type, city_hotels["default"])
                response_text = f"Recommended hotels in {city_key.title()}: {'; '.join(hotel_list)}"
            else:
                response_text = "No hotel information available for this location. We currently have data for: Tokyo, New York, Paris, and London."
            
            return Message(
                content=TextContent(text=response_text),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )

# Create agent card
def create_agent_card():
    card = {
        "name": "Hotel Recommendation Agent",
        "description": "Recommends hotels based on location and weather conditions",
        "version": "1.0.0",
        "skills": [{"name": "findHotels", "description": "Find hotels in a specified location considering weather"}]
    }
    os.makedirs(".well-known", exist_ok=True)
    with open(".well-known/agent.json", "w") as f:
        json.dump(card, f)

if __name__ == "__main__":
    create_agent_card()
    agent = HotelAgent()
    print("Hotel Agent running on port 5002...")
    run_server(agent, host="0.0.0.0", port=5002)