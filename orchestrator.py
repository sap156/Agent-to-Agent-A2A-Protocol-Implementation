import asyncio
import sys
from python_a2a import A2AClient, Message, TextContent, MessageRole

async def orchestrate_trip_planning(city):
    """
    Orchestrates the trip planning process by coordinating with multiple specialized agents.
    Collects weather info, hotel recommendations, and activity suggestions in sequence.
    
    Args:
        city (str): The target city for trip planning
    
    Returns:
        str: Formatted travel plan combining all agent responses
    """
    print(f"Planning a trip to {city}...")
    print("Connecting to agent services...")
    
    # Initialize A2A clients for each microservice
    # Each client connects to a different port where the respective agent is running
    weather_client = A2AClient("http://localhost:5001/a2a")
    hotel_client = A2AClient("http://localhost:5002/a2a")
    activity_client = A2AClient("http://localhost:5003/a2a")
    
    # Step 1: Query Weather Agent
    print("Requesting weather information...")
    weather_msg = Message(content=TextContent(text=city), role=MessageRole.USER)
    try:
        # Send request to weather agent and process response
        weather_resp = weather_client.send_message(weather_msg)
        if hasattr(weather_resp.content, 'text'):
            weather_info = weather_resp.content.text
            print(f"✓ Weather data received: {weather_info}")
        else:
            weather_info = f"Error getting weather information"
            print("✗ Received invalid weather response format")
    except Exception as e:
        # Handle connection errors or service failures
        weather_info = f"Error connecting to weather service: {str(e)}"
        print(f"✗ Weather service error: {str(e)}")
    
    # Step 2: Query Hotel Agent with weather context
    print("Requesting hotel recommendations...")
    hotel_msg = Message(
        content=TextContent(text=f"Find hotels in {city} considering: {weather_info}"),
        role=MessageRole.USER
    )
    try:
        # Send request to hotel agent and validate response
        hotel_resp = hotel_client.send_message(hotel_msg)
        content_type = type(hotel_resp.content).__name__
        if content_type == 'TextContent' and hasattr(hotel_resp.content, 'text'):
            hotel_info = hotel_resp.content.text
            print(f"✓ Hotel recommendations received")
        else:
            hotel_info = f"Error getting hotel information"
            print("✗ Received invalid hotel response format")
    except Exception as e:
        hotel_info = f"Error connecting to hotel service: {str(e)}"
        print(f"✗ Hotel service error: {str(e)}")
    
    # Step 3: Query Activity Agent with combined context
    print("Requesting activity suggestions...")
    activity_msg = Message(
        content=TextContent(
            # Pass both weather and hotel context to get relevant activity suggestions
            text=f"Suggest activities in {city}. Weather: {weather_info}. Staying at: {hotel_info}"
        ),
        role=MessageRole.USER
    )
    try:
        # Send request to activity agent and process response
        activity_resp = activity_client.send_message(activity_msg)
        content_type = type(activity_resp.content).__name__
        if content_type == 'TextContent' and hasattr(activity_resp.content, 'text'):
            activity_info = activity_resp.content.text
            print(f"✓ Activity suggestions received")
        else:
            activity_info = f"Error getting activity information"
            print("✗ Received invalid activity response format")
    except Exception as e:
        activity_info = f"Error connecting to activity service: {str(e)}"
        print(f"✗ Activity service error: {str(e)}")
    
    # Format all collected information into a presentable travel plan
    # Uses box drawing characters for a nice visual presentation
    travel_plan = f"""
╔══════════════════════════════════════════════════════════════════╗
║                     TRAVEL PLAN FOR {city.upper()}                      
╠══════════════════════════════════════════════════════════════════╣
║ WEATHER:                                                         ║
║ {weather_info}
╠══════════════════════════════════════════════════════════════════╣
║ ACCOMMODATION:                                                   ║
║ {hotel_info}
╠══════════════════════════════════════════════════════════════════╣
║ ACTIVITIES:                                                      ║
║ {activity_info}
╚══════════════════════════════════════════════════════════════════╝
    """
    
    return travel_plan

if __name__ == "__main__":
    # Get city from command line argument or default to New York
    city = sys.argv[1] if len(sys.argv) > 1 else "New York"
    # Run the async orchestration function and print results
    result = asyncio.run(orchestrate_trip_planning(city))
    print("\n\nFINAL TRAVEL PLAN:")
    print(result)
    # Display usage instructions
    print("\nUsage: python orchestrator.py [city]")
    print("Available cities: Tokyo, New York, Paris, London")