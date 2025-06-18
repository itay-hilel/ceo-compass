import os
import logging
from ceo_compass.ceo_compass import CEOCompass
from ceo_compass.test_scenarios import run_ceo_compass_test

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    """CEO Compass - Organizational Communication Intelligence"""
    print("🎯 CEO COMPASS - AI-Powered Organizational Intelligence")
    print("Helping CEOs understand their teams through communication analysis")
    print("=" * 80)
    
    # Run comprehensive test scenarios
    success = run_ceo_compass_test()
    
    if success:
        print("\n🚀 CEO COMPASS READY FOR DEPLOYMENT!")
    else:
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Verify OPENAI_API_KEY is set correctly")
        print("2. Check internet connection for API calls") 
        print("3. Review error messages above")
        print("4. Ensure you have sufficient OpenAI API credits")

if __name__ == "__main__":
    main()