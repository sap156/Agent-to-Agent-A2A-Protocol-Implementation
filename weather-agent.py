# Import required libraries
from python_a2a import A2AServer, Message, TextContent, MessageRole, run_server
import json
import os

class WeatherAgent(A2AServer):
    """
    Weather Agent class that handles weather information requests for various cities
    Inherits from A2AServer to implement the A2A protocol
    """
    def handle_message(self, message):
        # Check if the incoming message is a text message
        if message.content.type == "text":
            # Extract and clean the city name from the message
            city = message.content.text.strip()
          
            # Dictionary containing mock weather data for different cities
            # In a production environment, this would be replaced with real API calls
            weather_info = {
                "tokyo": "sunny, 25°C", 
                "new york": "cloudy, 18°C",
                "paris": "rainy, 15°C",
                "london": "foggy, 12°C",
                "sydney": "sunny, 28°C",
                "singapore": "humid, 32°C",
                "rome": "sunny, 22°C",
                "berlin": "partly cloudy, 16°C"
            }.get(city.lower(), "weather data not available")
            
            # Construct and return the response message
            # Uses the same conversation_id to maintain context
            # parent_message_id links the response to the original request
            return Message(
                content=TextContent(text=f"Weather in {city}: {weather_info}"),
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
        "name": "Weather Agent",
        "description": "Provides weather information for cities",
        "version": "1.0.0",
        "skills": [{"name": "getWeather", "description": "Get weather for a city"}]
    }
    # Create .well-known directory if it doesn't exist
    os.makedirs(".well-known", exist_ok=True)
    # Write the agent card to the specified JSON file
    with open(".well-known/agent.json", "w") as f:
        json.dump(card, f)

if __name__ == "__main__":
    # Initialize the agent when running the script directly
    create_agent_card()
    agent = WeatherAgent()
    print("Weather Agent running on port 5001...")
    # Start the server on all network interfaces (0.0.0.0) on port 5001
    run_server(agent, host="0.0.0.0", port=5001)