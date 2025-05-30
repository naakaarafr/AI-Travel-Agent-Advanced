from dotenv import load_dotenv
load_dotenv()
import os
import requests
import json
from typing import Optional, Dict, Any, List
from crewai_tools import tool, SerperDevTool
from pydantic import BaseModel, Field

# Set up API keys
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')

# Initialize the main search tool
search_tool = SerperDevTool(
    search_url="https://google.serper.dev/search",
    n_results=10
)

@tool("Calculate expenses and budget")
def calculator_tool(operation: str) -> str:
    """
    Useful to perform mathematical calculations for travel budgets, expenses, currency conversions, and cost estimations.
    
    Args:
        operation (str): The mathematical operation to perform (e.g., "100 * 7", "250 + 180", etc.)
    
    Returns:
        str: The result of the calculation
    """
    try:
        # Safety check to prevent code execution
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in operation):
            return "Error: Invalid characters in mathematical expression"
        
        # Evaluate the mathematical expression
        result = eval(operation)
        return f"Calculation: {operation} = {result}"
    except Exception as e:
        return f"Error in calculation: {str(e)}"

@tool("Get weather forecast")
def weather_tool(city: str, date_range: str = "") -> str:
    """
    Get weather forecast for a specific city and date range. Useful for travel planning and packing suggestions.
    
    Args:
        city (str): The city name for weather forecast
        date_range (str): The date range for the forecast
    
    Returns:
        str: Weather forecast information
    """
    try:
        # Use search tool to get weather information
        search_query = f"weather forecast {city} {date_range}"
        weather_info = search_tool.run(search_query)
        return f"Weather forecast for {city} during {date_range}:\n{weather_info}"
    except Exception as e:
        return f"Error getting weather forecast: {str(e)}"

@tool("Search flight prices")
def flight_tool(origin: str, destination: str, date_range: str) -> str:
    """
    Search for flight prices between origin and destination cities.
    
    Args:
        origin (str): Origin city/airport
        destination (str): Destination city/airport  
        date_range (str): Travel dates
    
    Returns:
        str: Flight pricing information
    """
    try:
        search_query = f"flights from {origin} to {destination} {date_range} prices"
        flight_info = search_tool.run(search_query)
        return f"Flight information from {origin} to {destination} for {date_range}:\n{flight_info}"
    except Exception as e:
        return f"Error searching flight prices: {str(e)}"

@tool("Search hotels")
def accommodation_tool(city: str, date_range: str, budget_range: str = "mid-range") -> str:
    """
    Search for hotels and accommodations in a specific city.
    
    Args:
        city (str): The destination city
        date_range (str): Check-in and check-out dates
        budget_range (str): Budget preference (budget, mid-range, luxury)
    
    Returns:
        str: Hotel recommendations and pricing
    """
    try:
        search_query = f"best {budget_range} hotels {city} {date_range} booking"
        hotel_info = search_tool.run(search_query)
        return f"Hotel recommendations in {city} for {date_range} ({budget_range}):\n{hotel_info}"
    except Exception as e:
        return f"Error searching hotels: {str(e)}"

@tool("Find restaurants")
def restaurant_tool(city: str, cuisine_type: str = "local", interests: str = "") -> str:
    """
    Find restaurant recommendations in a specific city.
    
    Args:
        city (str): The destination city
        cuisine_type (str): Type of cuisine (local, international, specific cuisine)
        interests (str): Traveler interests to match restaurant style
    
    Returns:
        str: Restaurant recommendations
    """
    try:
        search_query = f"best {cuisine_type} restaurants {city} {interests} recommendations"
        restaurant_info = search_tool.run(search_query)
        return f"Restaurant recommendations in {city} for {cuisine_type} cuisine:\n{restaurant_info}"
    except Exception as e:
        return f"Error finding restaurants: {str(e)}"

@tool("Find attractions")
def attraction_tool(city: str, interests: str, date_range: str = "") -> str:
    """
    Find tourist attractions and activities in a city based on interests.
    
    Args:
        city (str): The destination city
        interests (str): Traveler's interests and hobbies
        date_range (str): Travel dates for seasonal activities
    
    Returns:
        str: Attraction and activity recommendations
    """
    try:
        search_query = f"best attractions activities {city} {interests} {date_range} things to do"
        attraction_info = search_tool.run(search_query)
        return f"Attractions and activities in {city} matching interests '{interests}':\n{attraction_info}"
    except Exception as e:
        return f"Error finding attractions: {str(e)}"

@tool("Find hidden gems")
def hidden_gems_tool(city: str, interests: str) -> str:
    """
    Find hidden gems and local secrets in a city.
    
    Args:
        city (str): The destination city
        interests (str): Traveler's interests
    
    Returns:
        str: Hidden gems and local recommendations
    """
    try:
        search_query = f"hidden gems secret places {city} locals recommend off beaten path {interests}"
        hidden_gems_info = search_tool.run(search_query)
        return f"Hidden gems and local secrets in {city}:\n{hidden_gems_info}"
    except Exception as e:
        return f"Error finding hidden gems: {str(e)}"

@tool("Get local culture tips")
def culture_tool(city: str) -> str:
    """
    Get local culture, customs, and etiquette tips for a city.
    
    Args:
        city (str): The destination city
    
    Returns:
        str: Cultural insights and tips
    """
    try:
        search_query = f"{city} local culture customs etiquette tips travelers should know"
        culture_info = search_tool.run(search_query)
        return f"Cultural tips and customs for {city}:\n{culture_info}"
    except Exception as e:
        return f"Error getting culture tips: {str(e)}"

@tool("Find transportation")
def transportation_tool(city: str) -> str:
    """
    Find local transportation options and tips for a city.
    
    Args:
        city (str): The destination city
    
    Returns:
        str: Local transportation information
    """
    try:
        search_query = f"{city} local transportation public transport taxi uber apps getting around"
        transport_info = search_tool.run(search_query)
        return f"Local transportation options in {city}:\n{transport_info}"
    except Exception as e:
        return f"Error finding transportation info: {str(e)}"

@tool("Find events")
def events_tool(city: str, date_range: str) -> str:
    """
    Find events, festivals, and seasonal activities in a city.
    
    Args:
        city (str): The destination city
        date_range (str): Travel dates
    
    Returns:
        str: Events and seasonal activities information
    """
    try:
        search_query = f"{city} events festivals activities {date_range} what's happening"
        events_info = search_tool.run(search_query)
        return f"Events and activities in {city} during {date_range}:\n{events_info}"
    except Exception as e:
        return f"Error finding events: {str(e)}"

@tool("Check safety")
def safety_tool(city: str) -> str:
    """
    Check safety information and travel advisories for a city.
    
    Args:
        city (str): The destination city
    
    Returns:
        str: Safety information and travel tips
    """
    try:
        search_query = f"{city} safety travel advisory areas to avoid crime rate tourists"
        safety_info = search_tool.run(search_query)
        return f"Safety information for {city}:\n{safety_info}"
    except Exception as e:
        return f"Error checking safety info: {str(e)}"

# List of all available tools for agents
ALL_TOOLS = [
    search_tool,
    calculator_tool,
    weather_tool,
    flight_tool,
    accommodation_tool,
    restaurant_tool,
    attraction_tool,
    hidden_gems_tool,
    culture_tool,
    transportation_tool,
    events_tool,
    safety_tool
]

# Specialized tool sets for different agents
CITY_SELECTION_TOOLS = [
    search_tool,
    weather_tool,
    flight_tool,
    accommodation_tool,
    events_tool,
    safety_tool,
    calculator_tool
]

LOCAL_EXPERT_TOOLS = [
    search_tool,
    attraction_tool,
    restaurant_tool,
    hidden_gems_tool,
    culture_tool,
    transportation_tool,
    events_tool,
    safety_tool
]

TRAVEL_CONCIERGE_TOOLS = [
    search_tool,
    calculator_tool,
    accommodation_tool,
    restaurant_tool,
    attraction_tool,
    transportation_tool,
    weather_tool
]