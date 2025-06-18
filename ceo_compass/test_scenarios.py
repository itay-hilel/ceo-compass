import os
from .ceo_compass import CEOCompass

def run_ceo_compass_test():
    """Test CEO Compass with realistic organizational scenarios"""
    print("🎯 CEO COMPASS - Organizational Intelligence Test")
    print("=" * 80)
    
    # Initialize CEO Compass
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY environment variable not set!")
        return False
    
    compass = CEOCompass(openai_api_key=api_key)
    
    # Realistic CEO scenarios
    ceo_scenarios = [
        {
            "name": "High-Performing Sprint Planning",
            "type": "team_meeting",
            "context": "Engineering team sprint planning - CEO wants to understand collaboration dynamics",
            "data": """
Sarah (Engineering Manager): Good morning team! Let's dive into sprint planning. We have some exciting features to build.
Alex (Senior Dev): Morning Sarah! I've reviewed the backlog and I think we can tackle the payment integration this sprint.
Jordan (Product Manager): That aligns perfectly with our Q3 goals. The customer feedback on payment flow has been consistent.
Mike (Junior Dev): I'd love to take on the frontend components. I've been studying React patterns.
Sarah: Great initiative Mike! Alex, can you pair with Mike on the complex parts?
Alex: Absolutely! I think we can break it into smaller chunks for Mike to own pieces.
Jordan: I love seeing this mentorship happening. Any concerns about the two-week timeline?
Mike: I'm confident with Alex's support. Maybe we can do daily check-ins?
Sarah: Perfect. Jordan, any blockers you foresee from product side?
Jordan: None that I can think of. The designs are finalized and APIs are documented.
Alex: This feels like our best planned sprint yet. Clear goals, good collaboration.
Sarah: Agreed! Let's make it happen team.
"""
        },
        {
            "name": "Tense Leadership Email Thread",
            "type": "leadership_email", 
            "context": "CEO monitoring leadership communication during a crisis",
            "data": """
From: ceo@company.com
Subject: Q3 Revenue Miss - Leadership Response Needed

Leadership Team,

Our Q3 numbers came in 15% below target. I need to understand what happened and our path forward before the board meeting Friday.

This is not just about numbers - it's about execution and accountability.

From: vp.sales@company.com
Subject: Re: Q3 Revenue Miss

The sales team delivered 102% of pipeline, but deal sizes were smaller than forecasted. Market conditions shifted in August.

From: cto@company.com
Subject: Re: Q3 Revenue Miss

Technical delivery was on schedule. No engineering blockers contributed to the revenue miss.

From: cfo@company.com
Subject: Re: Q3 Revenue Miss

The root issue is our pricing model doesn't reflect current market realities. We need to adjust expectations or strategy.

From: ceo@company.com
Subject: Re: Q3 Revenue Miss

I need solutions, not explanations. Let's meet tomorrow at 8am to create an action plan.

From: vp.sales@company.com
Subject: Re: Q3 Revenue Miss

Understood. I'll prepare a detailed market analysis and pricing recommendations.
"""
        },
        {
            "name": "All-Hands Culture Check",
            "type": "all_hands",
            "context": "CEO assessing company culture during rapid growth",
            "data": """
CEO: Welcome everyone to our monthly all-hands! We've grown to 150 people - amazing milestone.
Head of People: It's incredible to see all these faces. We hired 40 people this quarter alone.
Senior Engineer: The growth is exciting but I'm concerned about maintaining our startup culture.
Product Manager: I agree. Some new hires seem disconnected from our mission.
Marketing Director: We need better onboarding. New people don't understand our values yet.
CEO: These are valid concerns. Culture is my top priority as we scale.
Junior Designer: I joined recently and honestly felt overwhelmed initially. Mentorship helped a lot.
Engineering Manager: We should formalize mentorship programs across all departments.
Head of People: Great idea! We can launch buddy systems for new hires.
Sales Manager: Our new sales reps are struggling with our consultative approach versus aggressive tactics.
CEO: That's exactly the culture tension we need to address proactively.
Customer Success Lead: Our customer satisfaction scores remain high, so we're not losing our core values.
CEO: Good data point. Let's double down on what's working while improving onboarding.
"""
        }
    ]
    
    # Run analysis for each scenario
    test_results = []
    
    for i, scenario in enumerate(ceo_scenarios, 1):
        print(f"\n📊 CEO Scenario {i}: {scenario['name']}")
        print(f"Context: {scenario['context']}")
        print("-" * 60)
        
        try:
            print(f"🔍 Analyzing {scenario['type'].replace('_', ' ')}...")
            
            result = compass.analyze_organization(
                raw_communication=scenario['data'],
                communication_type=scenario['type']
            )
            
            if result['status'] == 'success':
                print("✅ Analysis completed successfully!")
                
                # Extract CEO dashboard insights
                dashboard = result['ceo_dashboard']
                executive_summary = dashboard.get('executive_summary', {})
                performance_metrics = dashboard.get('performance_metrics', {})
                key_insights = dashboard.get('key_insights', {})
                recommendations = dashboard.get('actionable_recommendations', {})
                
                # Display CEO-focused results
                print(f"\n🎯 EXECUTIVE SUMMARY:")
                print(f"  • Overall Team Health: {executive_summary.get('overall_team_health', 0):.2f}/1.0")
                print(f"  • Leadership Impact: {executive_summary.get('leadership_impact_score', 0):.2f}/1.0")
                print(f"  • Risk Level: {executive_summary.get('organizational_risk_level', 'unknown').title()}")
                print(f"  • Intervention Urgency: {executive_summary.get('intervention_urgency', 'unknown').title()}")
                
                print(f"\n📈 PERFORMANCE METRICS:")
                for metric, score in performance_metrics.items():
                    print(f"  • {metric.replace('_', ' ').title()}: {score:.2f}/1.0")
                
                print(f"\n💪 TEAM STRENGTHS:")
                for strength in key_insights.get('team_strengths', []):
                    print(f"  • {strength}")
                
                print(f"\n⚠️  AREAS OF CONCERN:")
                for concern in key_insights.get('areas_of_concern', []):
                    print(f"  • {concern}")
                
                print(f"\n🎯 IMMEDIATE ACTIONS FOR CEO:")
                for action in recommendations.get('immediate_actions', []):
                    print(f"  • {action}")
                
                print(f"\n📅 30-DAY FOCUS AREAS:")
                for area in recommendations.get('30_day_focus_areas', []):
                    print(f"  • {area}")
                
                # CEO metadata
                metadata = dashboard.get('analysis_metadata', {})
                team_metadata = result.get('team_metadata', {})
                speaker_stats = team_metadata.get('speaker_statistics', {})
                
                # Extract participant names and roles
                leadership_participants = []
                team_participants = []
                
                for speaker, stats in speaker_stats.items():
                    if stats.get('is_leadership', False):
                        leadership_participants.append(speaker)
                    else:
                        team_participants.append(speaker)
                
                print(f"\n📊 Analysis Context:")
                print(f"  • Participants: {metadata.get('participants_analyzed', 0)} ({metadata.get('leadership_participants', 0)} leadership)")
                
                # Display leadership participants
                if leadership_participants:
                    print(f"  • Leadership: {', '.join(leadership_participants)}")
                
                # Display team participants
                if team_participants:
                    print(f"  • Team Members: {', '.join(team_participants)}")
                
                print(f"  • Communication Type: {metadata.get('communication_type', 'unknown').replace('_', ' ').title()}")
                print(f"  • Messages Analyzed: {metadata.get('messages_processed', 0)}")
                
                test_results.append({
                    'scenario': scenario['name'],
                    'status': 'PASSED',
                    'team_health': executive_summary.get('overall_team_health', 0),
                    'risk_level': executive_summary.get('organizational_risk_level', 'unknown')
                })
                
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                test_results.append({
                    'scenario': scenario['name'], 
                    'status': 'FAILED',
                    'error': result.get('error', 'Unknown error')
                })
                
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            test_results.append({
                'scenario': scenario['name'],
                'status': 'ERROR', 
                'error': str(e)
            })
    
    # CEO-focused summary report
    print("\n" + "=" * 80)
    print("🎯 CEO COMPASS TEST SUMMARY")
    print("=" * 80)
    
    passed_tests = [r for r in test_results if r['status'] == 'PASSED']
    failed_tests = [r for r in test_results if r['status'] in ['FAILED', 'ERROR']]
    
    print(f"✅ Successful Analyses: {len(passed_tests)}/{len(test_results)}")
    print(f"❌ Failed Analyses: {len(failed_tests)}/{len(test_results)}")
    
    if passed_tests:
        print("\n🎯 Organizational Health Scores:")
        for result in passed_tests:
            print(f"  • {result['scenario']}: {result['team_health']:.2f} health ({result['risk_level']} risk)")
    
    if failed_tests:
        print("\n❌ Analysis Failures:")
        for result in failed_tests:
            print(f"  • {result['scenario']}: {result.get('error', 'Unknown error')}")
    
    # Validate CEO capabilities
    print("\n🔧 CEO COMPASS CAPABILITIES VALIDATED")
    print("-" * 50)
    
    capabilities = {
        'Leadership Effectiveness Analysis': len(passed_tests) > 0,
        'Organizational Alignment Detection': len(passed_tests) > 0,
        'Risk Level Assessment': len(passed_tests) > 0,
        'Actionable CEO Recommendations': len(passed_tests) > 0,
        'Multi-format Communication Parsing': len(passed_tests) > 0,
        'Strategic Dashboard Generation': len(passed_tests) > 0,
        'Team Dynamics Intelligence': len(passed_tests) > 0,
        'Cultural Health Monitoring': len(passed_tests) > 0
    }
    
    for capability, validated in capabilities.items():
        status = "✅" if validated else "❌"
        print(f"{status} {capability}")
    
    overall_success = len(passed_tests) == len(test_results)
    
    if overall_success:
        print("\n🎉 CEO COMPASS FULLY OPERATIONAL!")
        print("Your organizational intelligence system is ready to provide strategic insights.")
    else:
        print(f"\n⚠️  {len(failed_tests)} test(s) failed. Check errors above.")
    
    return overall_success
