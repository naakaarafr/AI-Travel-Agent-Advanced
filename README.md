# AI Travel Agent - Advanced 🌍✈️

An intelligent, multi-agent travel planning system powered by Google's Gemini AI and CrewAI framework. This advanced travel planner uses specialized AI agents to analyze destinations, provide local expertise, and create comprehensive travel itineraries.

## 🚀 Features

### Multi-Agent Architecture
- **🎯 Destination Analyst Agent**: Analyzes weather, costs, activities, and safety for optimal city selection
- **🏛️ Local Expert Agent**: Provides insider knowledge, hidden gems, and cultural insights
- **🗓️ Travel Concierge Agent**: Creates detailed itineraries with accommodations, dining, and budget planning

### Intelligent Analysis
- Real-time weather forecasting for travel dates
- Flight price analysis and cost optimization  
- Accommodation recommendations across all budget ranges
- Cultural insights and local etiquette guidance
- Hidden gems and off-the-beaten-path recommendations
- Comprehensive budget breakdowns with realistic estimates

### Comprehensive Planning
- Day-by-day detailed itineraries
- Restaurant recommendations for every meal
- Transportation logistics and local navigation tips
- Weather-appropriate packing suggestions
- Safety information and travel advisories
- Cultural events and seasonal activities

## 🛠️ Technology Stack

- **AI Framework**: CrewAI for multi-agent orchestration
- **Language Model**: Google Gemini 2.0 Flash
- **Web Search**: Serper API for real-time information
- **Environment**: Python 3.8+
- **Data Processing**: Pandas, JSON handling
- **Configuration**: python-dotenv for environment management

## 📋 Prerequisites

Before setting up the project, ensure you have:

1. **Python 3.8 or higher** installed
2. **Google AI API Key**:
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the Generative AI API
   - Create an API key
3. **Serper API Key**:
   - Sign up at [Serper.dev](https://serper.dev/)
   - Get your free API key

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/naakaarafr/AI-Travel-Agent-Advanced.git
   cd AI-Travel-Agent-Advanced
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv travel_agent_env
   source travel_agent_env/bin/activate  # On Windows: travel_agent_env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   ```

## 🚦 Quick Start

### 1. Test Your Setup
Before running the main application, verify your API connections:

```bash
python debug_api.py
```

This diagnostic tool will test:
- Internet connectivity
- Google API key validity
- Serper API key functionality
- CrewAI + Gemini integration

### 2. Run the Travel Planner
Start the interactive travel planning interface:

```bash
python crew.py
```

### 3. Follow the Interactive Prompts
The system will guide you through:
- Origin and destination selection
- Travel dates and duration
- Budget preferences (budget/mid-range/luxury)
- Travel style (relaxed/adventure/cultural/romantic/business)
- Personal interests and activities
- Group size and special requirements

## 📁 Project Structure

```
AI-Travel-Agent-Advanced/
├── crew.py                 # Main application with CLI interface
├── config.py              # Configuration management
├── debug_api.py           # API diagnostic and testing tool
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── reports/               # Generated travel plans (auto-created)
└── README.md             # This file
```

## 🤖 Agent Workflow

### 1. Destination Analysis Phase
The **Destination Analyst Agent** evaluates each potential destination by:
- Analyzing weather conditions and forecasts
- Comparing flight costs and availability
- Assessing accommodation options and pricing
- Checking seasonal events and festivals
- Reviewing safety conditions and travel advisories
- Matching destinations to traveler interests

### 2. Local Expertise Phase  
The **Local Expert Agent** provides insider knowledge including:
- Hidden gems and local secrets
- Cultural customs and etiquette tips
- Authentic dining recommendations
- Transportation insights and apps
- Safety tips and areas to avoid
- Best times to visit popular attractions

### 3. Itinerary Creation Phase
The **Travel Concierge Agent** creates comprehensive plans featuring:
- Detailed daily schedules with specific venues
- Hotel recommendations with pricing tiers
- Restaurant suggestions for every meal
- Transportation logistics and costs
- Complete budget breakdown
- Weather-appropriate packing lists

## 🔧 Configuration Options

### Custom Agent Behavior
Modify agent personalities and capabilities in `agents.py`:
- Adjust temperature settings for creativity vs. precision
- Customize agent backstories and specializations  
- Add new tools or modify existing ones

### Tool Customization
Extend functionality in `tools.py`:
- Add new search capabilities
- Integrate additional APIs
- Create specialized calculation tools
- Implement custom data processing

## 📊 Output Examples

### Sample Travel Plan Structure
```markdown
# Travel Plan for Tokyo, Japan

## Trip Summary
- **Origin:** New York, NY
- **Destination:** Tokyo, Japan  
- **Travel Dates:** 2024-03-15 to 2024-03-22
- **Duration:** 7 days
- **Budget:** Mid-range ($2,500 total)

## Daily Itinerary

### Day 1: Arrival & Shibuya Exploration
**Morning:**
- Arrive at Narita Airport (Flight: $780)
- Airport Express to Shibuya ($12)
- Check-in: Hotel Century Southern Tower ($120/night)

**Afternoon:** 
- Shibuya Crossing experience
- Hachiko Statue visit
- Shibuya Sky observation deck ($15)

[... detailed daily plans continue ...]

## Budget Breakdown
- **Flights:** $780
- **Accommodation:** $840 (7 nights)
- **Food:** $350 ($50/day)
- **Transportation:** $150
- **Activities:** $200
- **Miscellaneous:** $180
- **Total:** $2,500
```

## 🛠️ Troubleshooting

### Common Issues

**1. API Key Errors**
```bash
❌ Error: GOOGLE_API_KEY not found
```
- Verify your `.env` file contains valid API keys
- Run `python debug_api.py` to test connections

**2. Import Errors**
```bash
ModuleNotFoundError: No module named 'crewai'
```
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**3. Search Tool Failures**
```bash
❌ Serper API test failed
```
- Check your Serper API key validity
- Verify internet connection
- Ensure API key has sufficient quota

### Debug Mode
Enable verbose logging for troubleshooting:
```python
# In crew.py, set verbose=True for agents
verbose=True
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** and test thoroughly
4. **Commit with clear messages**:
   ```bash
   git commit -m "Add amazing feature for better itinerary generation"
   ```
5. **Push to your branch**:
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Contribution Ideas
- Add new specialized agents (visa assistance, travel insurance)
- Integrate additional APIs (booking platforms, review sites)
- Improve user interface with web frontend
- Add multi-language support
- Implement user preference learning
- Create mobile app integration

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CrewAI** - Multi-agent framework that powers our intelligent agents
- **Google Gemini** - Advanced language model for natural conversation
- **Serper** - Real-time web search capabilities
- **Travel Community** - Inspiration for comprehensive travel planning

## 📞 Support

Having issues or questions? Here's how to get help:

1. **Check the troubleshooting section** above
2. **Run the diagnostic tool**: `python debug_api.py`  
3. **Open an issue** on GitHub with:
   - Error messages and logs
   - Your system information
   - Steps to reproduce the problem
4. **Join the discussion** in GitHub Discussions

## 🔮 Roadmap

### Upcoming Features
- [ ] Web-based user interface
- [ ] Integration with booking platforms
- [ ] Multi-destination trip planning
- [ ] Group travel coordination
- [ ] Expense tracking during travel
- [ ] Real-time itinerary adjustments
- [ ] Travel document management
- [ ] Social sharing capabilities

### Long-term Vision
- AI-powered travel companion mobile app
- Integration with IoT devices for seamless travel
- Predictive travel planning based on user behavior  
- Community-driven destination insights
- Sustainable travel recommendations
