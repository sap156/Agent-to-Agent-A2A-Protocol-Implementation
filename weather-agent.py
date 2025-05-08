from python_a2a import A2AServer, Message, TextContent, MessageRole, run_server
import json
import os

class WeatherAgent(A2AServer):
    def handle_message(self, message):
        if message.content.type == "text":
            city = message.content.text.strip()
          
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
            
            return Message(
                content=TextContent(text=f"Weather in {city}: {weather_info}"),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )

# Create agent card
def create_agent_card():
    card = {
        "name": "Weather Agent",
        "description": "Provides weather information for cities",
        "version": "1.0.0",
        "skills": [{"name": "getWeather", "description": "Get weather for a city"}]
    }
    os.makedirs(".well-known", exist_ok=True)
    with open(".well-known/agent.json", "w") as f:
        json.dump(card, f)

if __name__ == "__main__":
    create_agent_card()
    agent = WeatherAgent()
    print("Weather Agent running on port 5001...")
    run_server(agent, host="0.0.0.0", port=5001)