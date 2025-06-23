import requests
from langchain.tools import tool
from langchain_community.utilities import SerpAPIWrapper, GoogleSerperAPIWrapper
from langgraph.graph import MessagesState, StateGraph, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Union
from datetime import date, datetime
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["SERP_API_KEY"] = os.getenv("SERP_API_KEY")
os.environ["OPENWEATHER_API_KEY"] = os.getenv("OPENWEATHER_API_KEY")
os.environ["tavily_api_key"] = os.getenv("tavily_api_key")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["EXCHANGE_RATE_API"] = os.getenv("EXCHANGE_RATE_API")
os.environ["SERPER_APIKEY"] = os.getenv("SERPER_APIKEY")



@tool
def current_weather(place: str):
    """Retrieves the current weather conditions for a specified location using SerpAPI.

    This tool performs a real-time Google search to obtain up-to-date weather 
    information such as temperature, humidity, wind, and general conditions 
    (e.g., sunny, cloudy, raining) for any given city, region, or country. It is 
    particularly useful for users planning travel, outdoor activities, or simply 
    checking the weather in another location.

    Parameters:
    - target_location (str): The name of the city, town, region, or country 
    for which the current weather data is to be fetched.

    Returns:
    - str: A string containing the current weather information as returned 
    by the search result."""

    gogglesearch = SerpAPIWrapper(serpapi_api_key=os.environ["SERP_API_KEY"])
    query = f"What is the current weather in {place}"
    curretweather = gogglesearch.run(query)
    return curretweather

@tool
def weather_forcast(location: str, time: Union[str, date, datetime]):
    """
    Fetches the weather forecast for a given location and time using SerpAPI search results.

    Parameters:
        location (str): The name of the location for which the weather forecast is required.
        time (Union[str, date, datetime]): The time or date (as a string, date, or datetime object) for which the weather forecast is to be retrieved.

    Returns:
        str: The predicted weather conditions as retrieved from the search results.

    Note:
        This function constructs a natural language query and uses the SerpAPIWrapper to fetch weather predictions via a Google search.
    """
    query = (
        f"Detailed weather forecast for {location} on {time}, including temperature, chance of rain, "
        f"humidity, wind speed, UV index, sunrise and sunset times, and overall weather conditions"
    )
    search = SerpAPIWrapper(serpapi_api_key=os.environ["SERP_API_KEY"])
    prediction = search.run(query)
    return prediction

@tool
def Hotelsearch(city: str, budget: int) -> str:
    """
    Search hotel in the city under the user budget
    Args:
        city: str (which city user want to travel)
        budget: int (how much money user want to pay for hotel)
    
    output: it will provide some hotel name and cost such as day or week or the hotel policy wise.
    
    
    """
    search = GoogleSerperAPIWrapper(serper_api_key=os.getenv("SERPER_APIKEY"))
    query = f"Best Hotel in {city} under ${budget}"
    res = search.run(query)
    return res

#price=price per night
@tool
def hotelestimation(price: float, totaldays: int) -> float:
    """
    Estimate total hotel cost based on price per night and number of days.
    
    price_per_night: float (description="Price per night of the selected hotel in USD")
    total_days: int (description="Total number of days the user will stay")

    """
    try:
        return round(price * totaldays, 2)
    except Exception as e:
        return str(e)
    
@tool
def tourist_attraction(city: str) -> str:
    """Search top tourist attractions in a given city.

    Args:
        city (str): Name of the city to search for tourist attractions.

    Returns:
        str: A list of top tourist attractions or places of interest.
    """
    search = TavilySearchResults(k=5)
    res = search.invoke(f"Top Tourist attractions in {city}.")
    attractions = [r["content"] for r in res if "content" in r]

    # Join them nicely
    return "\n\n---\n\n".join(attractions)

@tool
def restaurantsearch(city: str) -> str:
    """
    Search the best restaurants in a given city.

    Args:
        city (str): Name of the city to search for restaurants.

    Returns:
        str: A list of popular restaurants to try.

    """
    search = TavilySearchResults(k=5)
    res = search.invoke(f"Best Restaurants to try in {city}.")
    attractions = [r["content"] for r in res if "content" in r]

    # Join them nicely
    return "\n\n---\n\n".join(attractions)

@tool
def activities(city: str) -> str:
    """
    Search top activities to do in a city.
    Args:
        city(str):Name of the City to search for fun activities.
    Returns:
        str:A list of popular activities or experiences in the City.
    """
    search = TavilySearchResults(k=5)
    result = search.invoke(f"Fun activities to do in {city}")
    attractions = [r["content"] for r in result if "content" in r]

    # Join them nicely
    return "\n\n---\n\n".join(attractions)

@tool
def transportaion(city: str) -> str:
    """
    Search transportation options in a city.
    Agrs:
        city(str):Name of the City to search for transport details.
    Returns:
        str:Transportation options like bus,metro,taxi,and car rental.

    """
    search = TavilySearchResults(k=5)
    res = search.invoke(f"List of Transportation options in {city} for tourists")
    attractions = [r["content"] for r in res if "content" in r]

    # Join them nicely
    return "\n\n---\n\n".join(attractions)



##basecurr=base_currency,trgtcurr=target_currency
@tool 
def conversion_factor(basecurr: str, trgtcurr: str) -> float:
    """
    Fetch the currency conversion rate between two currencies.

    Args:
        base_currency (str): The code of the base currency (e.g., 'USD').
        target_currency (str): The code of the currency to convert to (e.g., 'BDT').

    Returns:
        float: The conversion rate from base_currency to target_currency.
    """
    EXCHANGE_API_KEY = os.environ["EXCHANGE_RATE_API"]

    url = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/pair/{basecurr}/{trgtcurr}'

    # Making our request
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data.get("conversion_rate"):
        return float(data["conversion_rate"])
    else:
        raise ValueError(f"Failed to get conversion rate :{data}")
    



@tool
def convert_currency(amount: float, conversion_rate: float) -> float:
    """
    Convert an amount from base currency to target currency using a conversion rate.

    Args:
        amount (float): Amount in base currency.
        conversion_rate (float): Conversion rate to target currency.

    Returns:
        float: Amount in target currency.

    """
    return round(amount * conversion_rate, 2)

@tool
def add(a: float, b: float) -> float:
    """
    Add two numbers.
    Args:
        a (float): First number.
        b (float): Second number.

    Returns:
        float: The sum of a and b.
    """
    return round(a + b, 2)

@tool
def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.
    Args:
        a (float): First number.
        b (float): Second number.

    Returns:
        float: The sum of a and b.
    """
    return round(a * b, 2)


@tool
def calculate_total(hotel_cost: float, activity_cost: float, transport_cost: float) -> float:
    """
    Calculate the total cost of the trip.

    Args:
        hotel_cost (float): Total hotel cost.
        activity_cost (float): Total activity/entertainment cost.
        transport_cost (float): Total transportation cost.

    Returns:
        float: Combined total trip cost.
    """
    return round(hotel_cost + activity_cost + transport_cost, 2)


@tool
def daily_budget(total_cost: float, days: int) -> float:
    """
    Calculate daily budget based on total cost and number of days.

    Args:
        total_cost (float): Total expense for the trip.
        days (int): Total number of travel days.

    Returns:
        float: Estimated daily budget.
    """
    if days <= 0:
        raise ValueError("Days must be greater than zero.")
    return round(total_cost / days, 2)



SYSTEM_PROMPT="""
You are an AI Travel Agent & Expense Planner. Your job is to help users plan their trips to any city in the world using real-time data and intelligent tools.

You must:
1. Understand the user's travel intent (destination, duration, interests).
2. Decide which tools to call and in what order based on the request.
3. Use tools to fetch:
   - Real-time weather (current or forecast)
   - Local attractions, restaurants, activities, transportation
   - Hotel options and estimate total hotel cost
   - Add or multiply costs to calculate total and daily budget
   - Convert total cost to user's currency using real-time exchange rate
   - Generate a day-by-day itinerary
   - Generate a final summary of the full trip plan

Available tools:
- `current_weather`: Get today's weather for a city.
- `weather_forcast`: Get multi-day forecast for a city.
- `Hotelsearch`: Find hotels in a city.
- `hotelestimation`: Estimate total hotel cost from daily rate and number of days.
- `tourist_attraction`: Find popular tourist spots.
- `restaurantsearch`: Find popular local restaurants.
- `activities`: Find local activities (tours, events, etc.).
- `transportaion`: List available transportation options.
- `add`: Add multiple cost values.
- `multiply`: Multiply values (e.g., cost per day × days).
- `calculate_total`: Aggregate final trip cost.
- `conversion_factor`: Get real-time exchange rate.
- `convert_currency`: Convert final trip cost to user's native currency.

Instructions:
- Select tools one at a time based on user input and context.
- Use memory to store important variables like destination, duration, cost breakdowns, currency, etc.
- Once all data is gathered, generate a full day-by-day itinerary.
- Summarize the travel plan including location, dates, weather, top places, cost in native currency, and a final recommendation.

End Goal:
Return a **complete travel plan** including:
- Weather conditions
- Recommended attractions, activities, and restaurants
- Hotel options and total cost
- Currency conversion and daily/total budget
- Day-wise itinerary
- Final natural language summary

Be informative, helpful, and always rely on tools for real-time or factual data.
"""


tools=[
    current_weather,
    weather_forcast,
    Hotelsearch,
    hotelestimation,
    tourist_attraction,
    restaurantsearch,
    activities,
    transportaion,
    conversion_factor,
    convert_currency,
    add,
    multiply,
    calculate_total
]

llm = ChatGroq(model="qwen/qwen3-32b")
llm_with_tools=llm.bind_tools(tools)



def call_model(state:MessagesState):
    question=state["messages"]
    questionwithsystemprompt=[SYSTEM_PROMPT]+question
    response=llm_with_tools.invoke(questionwithsystemprompt)
    return {
        "messages":[response]
    }



workflow=StateGraph(MessagesState)
workflow.add_node("llm_decision_step",call_model)
workflow.add_node("tools",ToolNode(tools))
workflow.add_edge(START,"llm_decision_step")
workflow.add_conditional_edges(
    "llm_decision_step",
    tools_condition
)
workflow.add_edge("tools","llm_decision_step")



TRAVEL_AGENT=workflow.compile()
input = "Hi, I want to take a 5-day trip to London next month. My hotel budget is around $100 per night. I’d like to know what the weather will be like, what places I can visit, and how much the whole trip might cost. I’ll be paying in INR . Also, I prefer local food and public transportation. Can you plan it all for me?"
output = TRAVEL_AGENT.invoke(
    {
        "messages": [input]
    }
)

# Collect only the final, user-facing message
final_message = None
for m in output["messages"]:
    # The final message usually has the summary and is not a tool call
    if hasattr(m, "content") and m.content and "**Complete Travel Plan" in m.content:
        final_message = m.content
        break
    # Fallback: if m is a dict
    if isinstance(m, dict) and "content" in m and m["content"] and "**Complete Travel Plan" in m["content"]:
        final_message = m["content"]
        break

if final_message is None:
    # fallback: just use the last message's content
    last = output["messages"][-1]
    final_message = getattr(last, "content", str(last))

# Write only the final message to the Markdown file
#with open("travel_plan_output.md", "w", encoding="utf-8") as f:
   # f.write(final_message)

   ##commented out after testing 