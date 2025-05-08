# Agent-to-Agent (A2A) Protocol Implementation

This repository demonstrates a practical implementation of Google's Agent-to-Agent (A2A) protocol using the python-a2a library. The system shows how specialized AI agents can communicate with each other through a standardized protocol to create a travel planning service.

![A2A_banner](https://github.com/user-attachments/assets/d33a431b-d940-4a0a-aa0c-9790f5e4c250)

## What is A2A?

Agent-to-Agent (A2A) is a protocol that standardizes how AI agents communicate with each other. Think of it as a "universal translator" that allows different AI systems to understand one another, regardless of which framework or platform they were built with.

Just as humans need a common language to collaborate effectively, AI agents need standardized communication protocols to work together. A2A provides this common language, enabling agents created with different technologies (LangChain, CrewAI, etc.) to cooperate seamlessly.

## Project Overview

This project implements a simple travel planning system with three specialized agents:

1. **Weather Agent**: Provides weather information for cities
2. **Hotel Agent**: Recommends hotels based on location and weather conditions
3. **Activity Agent**: Suggests activities based on location and weather

An orchestrator coordinates these agents, demonstrating how they can work together to create a comprehensive travel plan.

## How A2A Works: Visual Overview

![A2A](https://github.com/user-attachments/assets/de34f6a5-4e78-47a2-a5bf-5320332fe896)

The diagram above illustrates how the A2A protocol enables agent communication in our travel planning system:

1. The user initiates a request for a travel plan to a specific city
2. The orchestrator agent receives this request and coordinates the process
3. The orchestrator sends the city name to the Weather Agent
4. The Weather Agent responds with weather information
5. The orchestrator sends both city and weather info to the Hotel Agent
6. The Hotel Agent responds with accommodation recommendations
7. The orchestrator sends city, weather, and hotel info to the Activity Agent
8. The Activity Agent suggests appropriate activities
9. The orchestrator compiles all information into a comprehensive travel plan

Each agent has an associated Agent Card that defines its capabilities and how to interact with it. These standardized Agent Cards are a key part of the A2A protocol, allowing agents to discover and understand each other's abilities.


## Project Structure

```
a2a-implementation/
├── requirements.txt
├── weather_agent.py  # Weather information service (port 5001)
├── hotel_agent.py    # Hotel recommendation service (port 5002)
├── activity_agent.py # Activity suggestion service (port 5003)
├── orchestrator.py   # Coordinates the agents to create a travel plan
└── README.md
```

## Setup Instructions

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/a2a-implementation.git
   cd a2a-implementation
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run each agent in a separate terminal:
   ```
   python weather_agent.py
   python hotel_agent.py
   python activity_agent.py
   ```

4. Run the orchestrator in another terminal:
   ```
   python orchestrator.py [city]
   ```
   Where `[city]` is optional and defaults to "New York". Available cities include Tokyo, New York, Paris, and London.

## How It Works

1. Each agent server maintains an Agent Card (in `.well-known/agent.json`) that describes its capabilities.
2. The orchestrator sends a request to the Weather Agent to get weather information for a city.
3. Using the weather information, the orchestrator queries the Hotel Agent for suitable accommodations.
4. With both weather and hotel information, the orchestrator then asks the Activity Agent for things to do.
5. The orchestrator compiles all this information into a comprehensive travel plan.

Each agent runs as a separate service, and they communicate using the A2A protocol.

## Technical Implementation

- Each agent extends the `A2AServer` class from the python-a2a library
- Communication happens through standardized `Message` objects
- Content is transmitted as `TextContent`
- Each agent handles messages through a `handle_message` method

## Sample Output

```
Planning a trip to Tokyo...
Connecting to agent services...
Requesting weather information...
✓ Weather data received: Weather in Tokyo: sunny, 25°C
Requesting hotel recommendations...
✓ Hotel recommendations received
Requesting activity suggestions...
✓ Activity suggestions received

FINAL TRAVEL PLAN:

╔══════════════════════════════════════════════════════════════════╗
║                     TRAVEL PLAN FOR TOKYO                      
╠══════════════════════════════════════════════════════════════════╣
║ WEATHER:                                                         ║
║ Weather in Tokyo: sunny, 25°C
╠══════════════════════════════════════════════════════════════════╣
║ ACCOMMODATION:                                                   ║
║ Recommended hotels in Tokyo: Tokyo Bay Resort - Beachfront property with outdoor activities; Shinjuku Garden Hotel - Rooftop bar with city views
╠══════════════════════════════════════════════════════════════════╣
║ ACTIVITIES:                                                      ║
║ Recommended activities in Tokyo: Visit Tokyo Skytree, Explore Meiji Shrine, Shop in Ginza, Picnic in Yoyogi Park
╚══════════════════════════════════════════════════════════════════╝
```

## Future Enhancements

- Integrate with real weather APIs
- Add more cities and detailed information
- Implement date-based planning capabilities
- Create a web interface for user interaction
- Add more agent types (transportation, restaurants, etc.)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
