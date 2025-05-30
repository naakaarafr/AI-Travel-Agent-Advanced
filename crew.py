#!/usr/bin/env python3
"""
AI Travel Planner - Fixed Version
A simplified but functional multi-agent travel planning system
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# Third-party imports
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import SerperDevTool, tool

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ensure required directories exist
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

@dataclass
class TravelRequest:
    """Travel request data structure"""
    origin: str
    destinations: List[str]
    start_date: str
    end_date: str
    duration: int
    budget_range: str
    travel_style: str
    interests: List[str]
    group_size: int
    special_requirements: List[str] = None
    
    def __post_init__(self):
        if self.special_requirements is None:
            self.special_requirements = []
    
    def to_dict(self) -> Dict:
        return asdict(self)

class TravelTools:
    """Consolidated travel planning tools"""
    
    def __init__(self):
        self.search_tool = SerperDevTool(n_results=10)
    
    @tool("Search for travel information")
    def search_travel_info(self, query: str) -> str:
        """Search for travel-related information using web search"""
        try:
            result = self.search_tool.run(query)
            return str(result)
        except Exception as e:
            return f"Search error: {str(e)}"
    
    @tool("Calculate travel expenses")
    def calculate_expenses(self, operation: str) -> str:
        """Calculate travel expenses and budgets"""
        try:
            # Safety check for mathematical expressions
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in operation):
                return "Error: Invalid characters in expression"
            
            result = eval(operation)
            return f"Calculation: {operation} = {result:,.2f}"
        except Exception as e:
            return f"Calculation error: {str(e)}"

class TravelPlannerAgents:
    """Travel planning agent system"""
    
    def __init__(self):
        self.llm = self._initialize_llm()
        self.tools = TravelTools()
        self.agents = self._create_agents()
    
    def _initialize_llm(self) -> ChatGoogleGenerativeAI:
        """Initialize the language model"""
        try:
            # Force disable OpenAI
            os.environ["OPENAI_API_KEY"] = ""
            os.environ["OPENAI_MODEL_NAME"] = ""
            
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if not google_api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=google_api_key,
                temperature=0.3,
                verbose=False
            )
            
            # Test the connection
            test_response = llm.invoke("Hello")
            logger.info("LLM initialized successfully")
            return llm
            
        except Exception as e:
            logger.error(f"LLM initialization failed: {e}")
            raise
    
    def _create_agents(self) -> Dict[str, Agent]:
        """Create the travel planning agents"""
        agents = {}
        
        # Destination Analyst Agent
        agents['destination_analyst'] = Agent(
            role="Travel Destination Analyst",
            goal="Analyze and recommend the best travel destination based on weather, costs, activities, and preferences",
            backstory="""You are an expert travel analyst with extensive knowledge of global destinations. 
            You excel at comparing cities based on weather patterns, flight costs, accommodation options, 
            seasonal events, and matching destinations to traveler preferences. You provide data-driven 
            recommendations with clear reasoning.""",
            tools=[self.tools.search_travel_info, self.tools.calculate_expenses],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Local Expert Agent
        agents['local_expert'] = Agent(
            role="Local Travel Expert",
            goal="Provide insider knowledge and authentic local recommendations for the chosen destination",
            backstory="""You are a seasoned local travel expert who has extensive knowledge of cities 
            worldwide. You know the hidden gems, local customs, authentic restaurants, cultural insights, 
            and practical tips that help travelers experience destinations like locals rather than tourists. 
            You provide actionable, insider advice.""",
            tools=[self.tools.search_travel_info],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Travel Concierge Agent
        agents['travel_concierge'] = Agent(
            role="Travel Concierge Specialist",
            goal="Create comprehensive travel itineraries with detailed logistics, accommodations, and budget planning",
            backstory="""You are a professional travel concierge with expertise in creating detailed, 
            practical travel itineraries. You excel at logistics coordination, timing optimization, 
            accommodation selection, restaurant recommendations, and budget planning. You ensure 
            every aspect of the trip is well-organized and memorable.""",
            tools=[self.tools.search_travel_info, self.tools.calculate_expenses],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        logger.info(f"Created {len(agents)} travel planning agents")
        return agents
    
    def create_tasks(self, request: TravelRequest) -> List[Task]:
        """Create tasks for the travel planning workflow"""
        
        # Task 1: Destination Analysis
        destination_analysis = Task(
            description=f"""
            **DESTINATION ANALYSIS TASK**
            
            Analyze and select the best destination from the provided options based on comprehensive criteria:
            
            **Analysis Requirements:**
            1. **Weather Analysis**: Current weather conditions and forecast for travel dates
            2. **Cost Analysis**: Flight prices from origin, accommodation costs, overall budget fit
            3. **Activities & Attractions**: Alignment with traveler interests and available activities
            4. **Seasonal Considerations**: Events, festivals, peak/off-season factors
            5. **Safety & Logistics**: Travel advisories, ease of travel, infrastructure
            
            **Travel Details:**
            - Origin: {request.origin}
            - Destination Options: {', '.join(request.destinations)}
            - Travel Dates: {request.start_date} to {request.end_date} ({request.duration} days)
            - Budget Range: {request.budget_range}
            - Group Size: {request.group_size} people
            - Interests: {', '.join(request.interests)}
            - Travel Style: {request.travel_style}
            
            **Required Output:**
            - Clear recommendation of the BEST destination with detailed reasoning
            - Weather forecast for recommended destination during travel period
            - Estimated flight costs and budget considerations
            - Top attractions/activities matching traveler interests
            - Any important considerations or warnings
            
            Provide specific, actionable information with current data and clear justification for your recommendation.
            """,
            agent=self.agents['destination_analyst'],
            expected_output="Comprehensive destination analysis with clear recommendation, weather forecast, cost estimates, and activity suggestions"
        )
        
        # Task 2: Local Expert Insights
        local_expert_insights = Task(
            description=f"""
            **LOCAL EXPERT INSIGHTS TASK**
            
            Based on the destination analysis, provide in-depth local expertise and insider recommendations:
            
            **Required Insights:**
            1. **Hidden Gems**: Off-the-beaten-path locations and experiences locals recommend
            2. **Cultural Intelligence**: Local customs, etiquette, cultural norms, and social tips
            3. **Authentic Dining**: Local restaurants, street food, traditional dishes to try
            4. **Insider Tips**: Best times to visit attractions, how to avoid crowds, local secrets
            5. **Practical Advice**: Transportation tips, local apps, shopping areas, safety considerations
            
            **Context:**
            - Travel Dates: {request.start_date} to {request.end_date}
            - Traveler Interests: {', '.join(request.interests)}
            - Travel Style: {request.travel_style}
            - Group Size: {request.group_size}
            
            **Output Requirements:**
            Provide specific recommendations with names, addresses, and practical details. Focus on 
            authentic experiences that match the traveler's interests and help them experience the 
            destination like a local.
            """,
            agent=self.agents['local_expert'],
            expected_output="Detailed local expert guide with hidden gems, cultural insights, authentic dining recommendations, and practical local tips",
            dependencies=[destination_analysis]
        )
        
        # Task 3: Complete Itinerary
        complete_itinerary = Task(
            description=f"""
            **COMPREHENSIVE ITINERARY CREATION TASK**
            
            Create a detailed, day-by-day travel itinerary incorporating all previous research:
            
            **Itinerary Components:**
            
            **Daily Schedule ({request.duration} days):**
            - Morning, afternoon, and evening activities for each day
            - Specific venues, attractions, and experiences with names and locations
            - Realistic timing and logistics between activities
            - Balance of activities with rest time
            
            **Accommodation Plan:**
            - Specific hotel/accommodation recommendations with names and locations
            - Reasoning for each choice (location, amenities, value, style match)
            - Price estimates and booking considerations
            
            **Dining Recommendations:**
            - Restaurant suggestions for breakfast, lunch, and dinner each day
            - Mix of local cuisine and international options
            - Specific dishes to try and estimated meal costs
            
            **Transportation & Logistics:**
            - Airport transfers and local transportation options
            - Getting between activities and attractions
            - Transportation costs and practical tips
            
            **Budget Breakdown:**
            - Accommodation costs (per night and total)
            - Transportation (flights, local transport)
            - Food and dining (daily estimates)
            - Activities and attractions (entrance fees, tours)
            - Miscellaneous expenses and shopping
            - **TOTAL ESTIMATED TRIP COST**
            
            **Practical Information:**
            - Weather-appropriate packing suggestions
            - Important contacts and emergency information
            - Cultural considerations and etiquette reminders
            
            **Travel Context:**
            - Origin: {request.origin}
            - Travel Dates: {request.start_date} to {request.end_date} ({request.duration} days)
            - Budget Range: {request.budget_range}
            - Interests: {', '.join(request.interests)}
            - Group Size: {request.group_size}
            
            **Format Requirements:**
            Present as well-organized markdown with clear sections. Use REAL place names, 
            actual businesses, and specific recommendations with reasoning.
            """,
            agent=self.agents['travel_concierge'],
            expected_output="Complete day-by-day travel itinerary in markdown format with accommodations, dining, activities, transportation, and detailed budget breakdown",
            dependencies=[destination_analysis, local_expert_insights]
        )
        
        return [destination_analysis, local_expert_insights, complete_itinerary]
    
    def plan_trip(self, request: TravelRequest) -> str:
        """Execute the travel planning workflow"""
        try:
            logger.info("Starting travel planning workflow")
            
            # Create tasks
            tasks = self.create_tasks(request)
            
            # Create crew
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            # Execute the workflow
            logger.info("Executing travel planning workflow...")
            result = crew.kickoff(inputs=request.to_dict())
            
            logger.info("Travel planning completed successfully")
            return str(result)
            
        except Exception as e:
            logger.error(f"Travel planning failed: {e}")
            return f"Error during travel planning: {str(e)}"

class TravelPlannerApp:
    """Main application class"""
    
    def __init__(self):
        self.planner = TravelPlannerAgents()
    
    def run_cli(self):
        """Run the command-line interface"""
        print("🌟" + "="*60 + "🌟")
        print("        AI TRAVEL PLANNER")
        print("🌟" + "="*60 + "🌟")
        
        try:
            # Get user input
            request = self._get_user_input()
            
            print(f"\n🚀 Planning your trip with AI specialists...")
            print(f"📊 Analyzing {len(request.destinations)} destinations for your {request.duration}-day trip")
            
            # Plan the trip
            result = self.planner.plan_trip(request)
            
            # Display results
            self._display_results(result)
            
            # Save the plan
            self._save_plan(result, request)
            
        except KeyboardInterrupt:
            print("\n❌ Planning cancelled by user")
        except Exception as e:
            logger.error(f"Application error: {e}")
            print(f"\n❌ Error: {e}")
    
    def _get_user_input(self) -> TravelRequest:
        """Get travel planning input from user"""
        print("\n📝 Let's plan your perfect trip:")
        
        # Basic information
        origin = input("\n🏠 Where are you traveling from? ").strip()
        
        destinations_input = input("🎯 What destinations are you considering? (comma-separated): ").strip()
        destinations = [d.strip() for d in destinations_input.split(',')]
        
        start_date = input("📅 Start date (YYYY-MM-DD): ").strip()
        end_date = input("📅 End date (YYYY-MM-DD): ").strip()
        
        # Calculate duration
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            duration = (end - start).days
            if duration <= 0:
                duration = 7  # Default to 7 days
        except:
            duration = 7
            print("⚠️  Invalid date format, defaulting to 7 days")
        
        group_size = input("👥 Number of travelers (default 1): ").strip()
        try:
            group_size = int(group_size) if group_size else 1
        except:
            group_size = 1
        
        # Preferences
        budget_options = ["budget", "mid-range", "luxury"]
        print(f"\n💰 Budget options: {', '.join(budget_options)}")
        budget_range = input("💰 Budget range (default mid-range): ").strip().lower()
        if budget_range not in budget_options:
            budget_range = "mid-range"
        
        style_options = ["relaxed", "adventure", "cultural", "romantic", "business"]
        print(f"🎭 Travel style options: {', '.join(style_options)}")
        travel_style = input("🎭 Travel style (default relaxed): ").strip().lower()
        if travel_style not in style_options:
            travel_style = "relaxed"
        
        interests_input = input("🎨 Your interests (comma-separated): ").strip()
        interests = [i.strip() for i in interests_input.split(',') if i.strip()]
        if not interests:
            interests = ["sightseeing", "local culture"]
        
        # Optional requirements
        special_req = input("♿ Any special requirements (optional): ").strip()
        special_requirements = [special_req] if special_req else []
        
        return TravelRequest(
            origin=origin,
            destinations=destinations,
            start_date=start_date,
            end_date=end_date,
            duration=duration,
            budget_range=budget_range,
            travel_style=travel_style,
            interests=interests,
            group_size=group_size,
            special_requirements=special_requirements
        )
    
    def _display_results(self, result: str):
        """Display the travel plan results"""
        print("\n" + "🎉" + "="*60 + "🎉")
        print("       YOUR TRAVEL PLAN IS READY!")
        print("🎉" + "="*60 + "🎉")
        
        print("\n" + result)
        
        print("\n" + "✈️" + "="*60 + "✈️")
        print("Have an amazing trip! 🌍")
        print("✈️" + "="*60 + "✈️")
    
    def _save_plan(self, result: str, request: TravelRequest):
        """Save the travel plan to a file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"travel_plan_{timestamp}.md"
            filepath = REPORTS_DIR / filename
            
            # Create markdown content
            content = f"""# Travel Plan
**Generated on:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Trip Summary
- **Origin:** {request.origin}
- **Destinations:** {', '.join(request.destinations)}
- **Travel Dates:** {request.start_date} to {request.end_date}
- **Duration:** {request.duration} days
- **Group Size:** {request.group_size}
- **Budget:** {request.budget_range}
- **Travel Style:** {request.travel_style}
- **Interests:** {', '.join(request.interests)}

## Travel Plan

{result}

---
*Generated by AI Travel Planner*
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"\n💾 Travel plan saved to: {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save travel plan: {e}")
            print(f"⚠️  Could not save travel plan: {e}")

def main():
    """Main function"""
    try:
        # Check for required environment variables
        if not os.getenv("GOOGLE_API_KEY"):
            print("❌ Error: GOOGLE_API_KEY not found in environment variables")
            print("Please add your Google API key to your .env file")
            return
        
        if not os.getenv("SERPER_API_KEY"):
            print("❌ Error: SERPER_API_KEY not found in environment variables")
            print("Please add your Serper API key to your .env file")
            return
        
        # Run the application
        app = TravelPlannerApp()
        app.run_cli()
        
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        print(f"❌ Startup error: {e}")

if __name__ == "__main__":
    main()