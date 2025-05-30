"""
Configuration file to force CrewAI to use Gemini exclusively
Import this BEFORE importing any CrewAI modules
"""
import os
from dotenv import load_dotenv

load_dotenv()

# FORCE CrewAI to avoid OpenAI completely
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_MODEL_NAME"] = ""
os.environ["OPENAI_API_BASE"] = ""

# Ensure Gemini is properly set up
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please add it to your .env file.")

print("✅ Configuration loaded - CrewAI will use Gemini exclusively")
print(f"✅ Google API Key loaded: {'Yes' if os.getenv('GOOGLE_API_KEY') else 'No'}")
print(f"✅ Serper API Key loaded: {'Yes' if os.getenv('SERPER_API_KEY') else 'No'}")