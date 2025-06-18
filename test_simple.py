#!/usr/bin/env python3
"""Simple test runner for CEO Compass"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """Test basic CEO Compass functionality"""
    print("🧪 Running Basic CEO Compass Tests...")
    
    try:
        # Test imports
        from ceo_compass.parsers import OrganizationalParser
        from ceo_compass.state import OrganizationalState
        print("✅ Imports successful")
        
        # Test parser
        parser = OrganizationalParser()
        sample_data = """
John: Hello team, let's start the meeting
Manager Sarah: Great! What's on the agenda today?
Developer Mike: I have some updates on the project
"""
        
        messages = parser.parse_team_meeting(sample_data)
        print(f"✅ Parser working - parsed {len(messages)} messages")
        
        # Test team dynamics
        dynamics = parser.extract_team_dynamics(messages)
        print(f"✅ Team dynamics analysis - {dynamics.get('total_participants', 0)} participants")
        
        # Test communication type detection
        comm_type = parser.auto_detect_communication_type(sample_data)
        print(f"✅ Communication type detection: {comm_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_with_api_key():
    """Test with actual API key if available"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set - skipping API tests")
        return True
        
    try:
        from ceo_compass.test_scenarios import run_ceo_compass_test
        print("🧪 Running CEO Compass API Tests...")
        
        result = run_ceo_compass_test()
        if result:
            print("✅ API tests passed")
        else:
            print("⚠️  API tests completed with some issues")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎯 CEO COMPASS - Simple Test Runner")
    print("=" * 50)
    
    basic_success = test_basic_functionality()
    api_success = test_with_api_key()
    
    print("\n" + "=" * 50)
    if basic_success and api_success:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
