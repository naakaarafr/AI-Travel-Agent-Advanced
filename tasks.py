from crewai import Task
from textwrap import dedent
from agents import city_selection_agent, local_expert_agent, travel_concierge_agent

# Create tasks following the working pattern
city_selection_task = Task(
    description=dedent("""
        **CITY SELECTION ANALYSIS TASK**
        
        You need to analyze and select the best city for the trip based on multiple criteria:
        
        **Research Requirements:**
        1. Weather conditions and forecast for each city during the travel dates
        2. Seasonal events, festivals, and cultural activities happening during the trip
        3. Flight costs from origin to each destination city
        4. Average accommodation costs and availability
        5. Tourist crowd levels and peak season considerations
        6. Safety and travel advisories
        7. Alignment with traveler's specific interests
        
        **Analysis Process:**
        - Compare ALL provided city options systematically
        - Use current data for weather forecasts and flight prices
        - Consider both positive and negative aspects of each destination
        - Factor in the traveler's interests and preferences
        
        **Required Output:**
        Your final answer must be a comprehensive report that includes:
        - Clear recommendation of the BEST city choice with detailed reasoning
        - Weather forecast for the selected city during travel dates
        - Estimated flight costs from origin to destination
        - Brief overview of top 3-5 attractions that align with interests
        - Any important travel considerations or warnings
        
        **Trip Details:**
        - Traveling from: {origin}
        - City Options: {cities}
        - Travel Dates: {date_range}
        - Traveler Interests: {interests}
        
        Make sure to provide concrete, actionable information with current data.
    """),
    agent=city_selection_agent,
    expected_output="""A detailed city selection report with:
    - Recommended destination with clear reasoning
    - Weather forecast and flight cost estimates
    - Top attractions matching traveler interests
    - Important travel considerations"""
)

local_expert_task = Task(
    description=dedent("""
        **LOCAL EXPERT CITY GUIDE TASK**
        
        Create an in-depth, insider's guide for the selected city. You are the local expert
        who knows this destination better than anyone else.
        
        **Required Research Areas:**
        1. **Hidden Gems & Local Secrets:**
           - Off-the-beaten-path locations locals love
           - Secret viewpoints, quiet neighborhoods, unique experiences
           
        2. **Cultural Insights:**
           - Local customs, etiquette, and cultural norms
           - Best times to visit popular attractions (avoid crowds)
           - Local phrases or cultural tips
           
        3. **Food & Dining:**
           - Authentic local restaurants (not tourist traps)
           - Street food recommendations and food safety tips
           - Local specialties and dishes to try
           
        4. **Activities & Attractions:**
           - Must-see landmarks and their best visiting times
           - Activities that match the traveler's interests
           - Seasonal activities available during travel dates
           
        5. **Practical Information:**
           - Local transportation tips and best apps to use
           - Shopping areas and local markets
           - Safety tips and areas to avoid
           - Weather-appropriate activity suggestions
        
        **Trip Context:**
        - Travel Dates: {date_range}
        - Traveling from: {origin}
        - Traveler Interests: {interests}
        
        Provide specific, actionable recommendations with names, addresses, and practical details.
    """),
    agent=local_expert_agent,
    expected_output="""A comprehensive local expert guide including:
    - Hidden gems and local secrets
    - Cultural insights and etiquette tips
    - Authentic dining recommendations
    - Activity suggestions matching interests
    - Practical travel and safety information"""
)

itinerary_task = Task(
    description=dedent("""
        **COMPREHENSIVE 7-DAY ITINERARY CREATION TASK**
        
        Create a detailed, day-by-day travel itinerary that incorporates all previous research
        into a practical, exciting travel plan.
        
        **Itinerary Requirements:**
        
        **Daily Schedule (7 days):**
        - Day-by-day breakdown with morning, afternoon, and evening activities
        - Specific attractions, restaurants, and experiences with names and locations
        - Realistic timing and travel logistics between locations
        - Rest periods and flexibility for spontaneous exploration
        
        **Accommodations:**
        - Specific hotel recommendations with names, locations, and price ranges
        - Explanation of why each hotel was chosen (location, amenities, value)
        - Alternative options for different budgets
        
        **Dining Plan:**
        - Breakfast, lunch, and dinner recommendations for each day
        - Mix of local restaurants, cafes, and food experiences
        - Include specific dish recommendations and estimated costs
        
        **Budget Breakdown:**
        - Accommodation costs (per night and total)
        - Transportation (flights, local transport, airport transfers)
        - Food and dining (per day estimates)
        - Activities and attractions (entrance fees, tours)
        - Shopping and miscellaneous expenses
        - **Total trip cost with daily breakdown**
        
        **Packing Suggestions:**
        - Weather-appropriate clothing for each day
        - Special items needed for planned activities
        - Local considerations (cultural dress codes, etc.)
        
        **Logistics:**
        - Airport transfer recommendations
        - Local transportation options and costs
        - Important contact information and apps
        
        **Trip Context:**
        - Travel Dates: {date_range}
        - Traveling from: {origin}
        - Traveler Interests: {interests}
        
        **FORMAT:** Present as well-organized markdown with clear sections and subsections.
        
        **IMPORTANT:** Use REAL place names, actual restaurants, and specific hotels. 
        Provide reasoning for each recommendation and what makes each place special.
    """),
    agent=travel_concierge_agent,
    expected_output="""A complete 7-day travel itinerary in markdown format including:
    - Detailed daily schedules with specific venues and activities
    - Accommodation recommendations with names and pricing
    - Restaurant and dining suggestions for each meal
    - Comprehensive budget breakdown with total costs
    - Weather-appropriate packing list
    - Transportation and logistics information"""
)