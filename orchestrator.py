import asyncio
import sys
from python_a2a import A2AClient, Message, TextContent, MessageRole

async def orchestrate_trip_planning(city):
    print(f"Planning a trip to {city}...")
    print("Connecting to agent services...")
    
    # Create clients for each agent service
    weather_client = A2AClient("http://localhost:5001/a2a")
    hotel_client = A2AClient("http://localhost:5002/a2a")
    activity_client = A2AClient("http://localhost:5003/a2a")
    
    # Step 1: Get weather information
    print("Requesting weather information...")
    weather_msg = Message(content=TextContent(text=city), role=MessageRole.USER)
    try:
        weather_resp = weather_client.send_message(weather_msg)
        if hasattr(weather_resp.content, 'text'):
            weather_info = weather_resp.content.text
            print(f"✓ Weather data received: {weather_info}")
        else:
            weather_info = f"Error getting weather information"
            print("✗ Received invalid weather response format")
    except Exception as e:
        weather_info = f"Error connecting to weather service: {str(e)}"
        print(f"✗ Weather service error: {str(e)}")
    
    # Step 2: Get hotel information
    print("Requesting hotel recommendations...")
    hotel_msg = Message(
        content=TextContent(text=f"Find hotels in {city} considering: {weather_info}"),
        role=MessageRole.USER
    )
    try:
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
    
    # Step 3: Suggest activities
    print("Requesting activity suggestions...")
    activity_msg = Message(
        content=TextContent(
            text=f"Suggest activities in {city}. Weather: {weather_info}. Staying at: {hotel_info}"
        ),
        role=MessageRole.USER
    )
    try:
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
    
    # Create the final travel plan
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
    # Get city from command line argument or use default
    city = sys.argv[1] if len(sys.argv) > 1 else "Tokyo"
    result = asyncio.run(orchestrate_trip_planning(city))
    print("\n\nFINAL TRAVEL PLAN:")
    print(result)
    print("\nUsage: python orchestrator.py [city]")
    print("Available cities: Tokyo, New York, Paris, London")