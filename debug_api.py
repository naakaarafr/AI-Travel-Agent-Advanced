"""
Debug script to test API connections and identify issues
Run this first before running your main crew.py
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_internet_connection():
    """Test basic internet connectivity"""
    print("🌐 Testing internet connection...")
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            print("✅ Internet connection: OK")
            return True
        else:
            print(f"❌ Internet connection issue: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Internet connection failed: {e}")
        return False

def test_google_api_key():
    """Test Google API key validity"""
    print("\n🔑 Testing Google API key...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment")
        return False
    
    if len(api_key) < 30:
        print(f"❌ API key seems too short: {len(api_key)} characters")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...{api_key[-5:]} ({len(api_key)} chars)")
    
    # Test the API key with a simple request
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # Use basic model for testing
            google_api_key=api_key,
            temperature=0.1
        )
        
        # Simple test message
        response = llm.invoke("Hello, respond with just 'API Working'")
        print(f"✅ Google API test successful: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Google API test failed: {e}")
        return False

def test_serper_api_key():
    """Test Serper API key validity"""
    print("\n🔍 Testing Serper API key...")
    
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        print("❌ SERPER_API_KEY not found in environment")
        return False
    
    print(f"✅ Serper API key found: {api_key[:8]}...{api_key[-4:]} ({len(api_key)} chars)")
    
    # Test Serper API
    try:
        url = "https://google.serper.dev/search"
        payload = {"q": "test query"}
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Serper API test successful")
            return True
        else:
            print(f"❌ Serper API test failed: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Serper API test failed: {e}")
        return False

def test_crewai_gemini():
    """Test CrewAI with Gemini integration"""
    print("\n🤖 Testing CrewAI with Gemini...")
    
    try:
        # Set environment to avoid OpenAI
        os.environ["OPENAI_API_KEY"] = ""
        os.environ["OPENAI_MODEL_NAME"] = ""
        
        from crewai import Agent
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.1
        )
        
        # Create a simple test agent
        test_agent = Agent(
            role="Test Agent",
            goal="Test if CrewAI works with Gemini",
            backstory="I am a test agent to verify the setup",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        
        print("✅ CrewAI with Gemini setup successful")
        return True
        
    except Exception as e:
        print(f"❌ CrewAI with Gemini test failed: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("🔧 API Connection Diagnostic Tool")
    print("=" * 50)
    
    tests = [
        ("Internet Connection", test_internet_connection),
        ("Google API Key", test_google_api_key),
        ("Serper API Key", test_serper_api_key),
        ("CrewAI + Gemini", test_crewai_gemini)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    if all(results.values()):
        print("\n🎉 All tests passed! Your setup should work.")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before running your main script.")
        
        # Provide specific guidance
        if not results.get("Internet Connection"):
            print("\n💡 Fix: Check your internet connection")
        
        if not results.get("Google API Key"):
            print("\n💡 Fix: Check your Google API key:")
            print("   1. Go to https://console.cloud.google.com/")
            print("   2. Enable the Generative AI API")
            print("   3. Create an API key")
            print("   4. Add it to your .env file as GOOGLE_API_KEY=your_key_here")
        
        if not results.get("Serper API Key"):
            print("\n💡 Fix: Check your Serper API key:")
            print("   1. Go to https://serper.dev/")
            print("   2. Sign up and get an API key")
            print("   3. Add it to your .env file as SERPER_API_KEY=your_key_here")

if __name__ == "__main__":
    main()