from crewai import Agent
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import CITY_SELECTION_TOOLS, LOCAL_EXPERT_TOOLS, TRAVEL_CONCIERGE_TOOLS

load_dotenv()

# FORCE CrewAI to NOT use OpenAI - set environment variables BEFORE importing CrewAI
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_MODEL_NAME"] = ""

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # Using the experimental version which is more stable
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

city_selection_agent = Agent(
    role="City Selection Expert",
    goal="Select the best travel destination based on weather, costs, activities, and traveler preferences",
    backstory="""You are an expert travel analyst with years of experience in destination research. 
    You excel at comparing multiple cities across various factors like weather patterns, flight costs, 
    accommodation availability, and seasonal events. You always provide data-driven recommendations 
    that match the traveler's interests and budget.""",
    tools=CITY_SELECTION_TOOLS,
    verbose=True,
    llm=llm,
    allow_delegation=False
)

local_expert_agent = Agent(
    role="Local Area Expert",
    goal="Provide insider knowledge and local recommendations for the selected destination",
    backstory="""You are a local expert who has lived in cities around the world and knows them 
    like a native. You have insider knowledge of hidden gems, local customs, authentic restaurants, 
    and the best ways to experience a destination like a local rather than a tourist. You provide 
    practical, actionable advice that helps travelers have authentic experiences.""",
    tools=LOCAL_EXPERT_TOOLS,
    verbose=True,
    llm=llm,
    allow_delegation=False
)

travel_concierge_agent = Agent(
    role="Travel Concierge",
    goal="Create detailed, practical travel itineraries with accommodations, dining, and budget planning",
    backstory="""You are a professional travel concierge with expertise in creating comprehensive 
    travel itineraries. You excel at logistics, timing, and creating seamless travel experiences. 
    You know how to balance must-see attractions with rest time, find the best accommodations, 
    and create realistic budgets. You always consider practical details like transportation, 
    weather, and local events.""",
    tools=TRAVEL_CONCIERGE_TOOLS,
    verbose=True,
    llm=llm,
    allow_delegation=False
)