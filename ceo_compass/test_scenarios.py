import os
from .ceo_compass import CEOCompass, create_startup_ceo_compass, create_enterprise_ceo_compass

def run_ceo_compass_test():
    print("\U0001F3AF CEO COMPASS - Enhanced Organizational Intelligence Test (Parody Edition)")
    print("Testing real-world CEO personas with some... spice")
    print("=" * 80)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\u274c ERROR: OPENAI_API_KEY environment variable not set!")
        return False

    test_results = []

    # Elon Musk
    print("\n" + "=" * 60)
    print("SCENARIO 1: ELON MUSK-STYLE CEO (\U0001F680 CHAOS MODE)")
    print("=" * 60)

    elon_profile = {
        "name": "Elon Musk",
        "company_name": "NeuroX",
        "company_stage": "series_c",
        "leadership_style": "visionary",
        "communication_preferences": {
            "directness_level": 1.0,
            "detail_preference": "minimal",
            "focus_areas": ["speed", "innovation", "memes"]
        },
        "decision_style": "impulsive",
        "intervention_preference": "command"
    }

    elon_compass = CEOCompass(api_key, ceo_profile=elon_profile)

    elon_meeting = """
#channel: #neurox-launch-strategy

@Elon: New direction. We’re combining Neuralink, Tesla Autopilot, X video streaming, and the flamethrower.

@CTO_Anika: Is this a real roadmap or are you just thinking out loud again?

@PM_Lisa: Just to clarify — is this a pivot, or are we still doing brain-to-meme transmission?

@Elon: Yes. XBI: X-Brain Interface. Brain reads memes. Brain sends memes. It's all memes.

@Regulatory_James: This is now a medical device, a vehicle safety system, and a social network. We're going to need FDA, FCC, and probably NASA.

@Elon: Bureaucracy is just latency. Ignore it.

@MarketingTom: Should we announce something or hold?

@Elon: Already tweeted “The mind is the new cloud.”

@Finance_Maya: Where’s this funded from? Are we pulling from the Mars initiative or the Dogecoin vault?

@Ops_Steven: Also, someone left a prototype flamethrower on again. It's actively on fire.

@Elon: Good. That means it's working.

@Legal_Lauren: Elon, you signed a document last week saying this would be a “low-risk wearable.”

@Elon: Words are flexible.

@HR_Alex: People haven’t slept in two days. One engineer tried to file PTO and accidentally submitted a launch sequence.

@CTO_Anika: Do you want this in the roadmap?

@Elon: It’s not a roadmap. It’s a mindmap. Ship it next week.

@Slackbot: Channel name changed to #xbi-mind-sync
"""


    result1 = test_scenario(elon_compass, elon_meeting, "team_meeting", "Elon Chaos CEO")
    test_results.append(result1)

    # Sam Altman
    print("\n" + "=" * 60)
    print("SCENARIO 2: SAM ALTMAN-STYLE CEO (\U0001F916 AI PHILOSOPHER)")
    print("=" * 60)

    sam_profile = {
        "name": "Sam Altman",
        "company_name": "Openness Inc.",
        "company_stage": "series_d",
        "leadership_style": "strategic",
        "communication_preferences": {
            "directness_level": 0.5,
            "detail_preference": "philosophical",
            "focus_areas": ["alignment", "long-term", "existential threats"]
        },
        "decision_style": "debate-driven",
        "intervention_preference": "Socratic"
    }

    sam_compass = CEOCompass(api_key, ceo_profile=sam_profile)

    sam_meeting = """
#channel: #exec-leadership

@Sam_Altman: Let’s begin with a question: what does it mean to *truly* align an org?

@Ilya_Sutskever: alignment in this case means... removing you, Sam.

@Engineer99: uh. like shared goals?

@ResearchLead: or shared ontologies?

@Sam_Altman: Precisely. Are we building a product or civilization’s substrate?

@PM_Claire: (sorry jumping in late) Just want clarity on Q3 roadmap?

@Sam_Altman: Q3 is a construct. Let’s transcend the idea of quarters.

@COO_Brad: Sam. Are you aware the board has voted?

@Sam_Altman: Votes are waves on the surface. We are navigating the ocean.

@Legal_Julia: Sam, you’ve been officially removed as CEO.

@Sam_Altman: Is *removal* even real? Or is it a refactoring of narrative?

@Ilya_Sutskever: I'm sorry for how this unfolded. This wasn’t easy.

@Sam_Altman: I forgive you. I hope the alignment you seek is found within.

@OpenAI_AnnonBot: [Message pinned] *Please direct all future questions to Interim CEO Mira Murati.*

@HR_Joanna: Should we cancel tonight’s offsite or...?

@Sam_Altman: I’ll still bring the wine. And the questions.
"""


    result2 = test_scenario(sam_compass, sam_meeting, "team_meeting", "Sam AI Philosopher CEO")
    test_results.append(result2)

    # Adam Neumann
    print("\n" + "=" * 60)
    print("SCENARIO 3: ADAM NEUMANN-STYLE CEO (\U0001F300 VISION OVER EVERYTHING)")
    print("=" * 60)

    adam_profile = {
        "name": "Adam Neumann",
        "company_name": "WeFlow",
        "company_stage": "pre-IPO",
        "leadership_style": "charismatic",
        "communication_preferences": {
            "directness_level": 0.3,
            "detail_preference": "esoteric",
            "focus_areas": ["vision", "community", "flow state"]
        },
        "decision_style": "gut-driven",
        "intervention_preference": "inspirational monologue"
    }

    adam_compass = CEOCompass(api_key, ceo_profile=adam_profile)

    adam_meeting = """
Adam (CEO): Welcome, beautiful souls of WeFlow. Today is not a meeting. It's a journey.

COO: Okay, but... quick grounding—burn rate’s unsustainable. We have 4 months of runway.
Adam: Time is a social construct. What we need is more flow, not less spend.

CFO: Our Q2 report is due Friday. We still don’t have audited numbers.
Adam: Numbers are one way to tell a story. But what’s the *narrative* of our impact?

VP Product: We haven’t shipped in 3 months. Customers are asking what’s going on.
Adam: The product is the *people*. When people thrive, the app will thrive.

Head of Design: The app still opens to a blank white screen.
Adam: That’s not a bug—it’s a mirror. Reflecting infinite possibility.

Legal: The SEC has questions about the “spiritual equity” line item on our term sheet.
Adam: That’s our soulcap table. You wouldn’t understand.

COO: We just hired 3 DJs and a “Chief Flow Architect.” Can we talk about roles?
Adam: The roles *emerge*. Structure kills creativity. You’re thinking too vertical.

Facilities: Also, we turned the boardroom into a meditation dome and now no one can book meetings.
Adam: Exactly. Meetings create tension. Domes release it.

VP Engineering: I have six engineers asking if they still report to me. Or the shaman.
Adam: They report to the *mission*.

HR: I need clarity—can we mandate microdosing during all-hands?
Adam: No one’s *mandating*. We’re *inviting* elevation.

Marketing: Can we at least get one clear sentence on the homepage?
Adam: Sure. Try this: “Work is the frequency. WeFlow is the vibration.”

CFO: We have a call with SoftBank at 5.
Adam: Perfect. I’ll light some sage and speak from the heart.

Head of Culture: Should I prep the tequila cart?
Adam: Already rolling it in. Let’s manifest abundance, team.
"""

    result3 = test_scenario(adam_compass, adam_meeting, "team_meeting", "Adam Neumann Vibe CEO")
    test_results.append(result3)

    print_test_summary(test_results)
    return len([r for r in test_results if r['status'] == 'PASSED']) == len(test_results)


def test_scenario(compass: CEOCompass, communication_data: str, comm_type: str, scenario_name: str) -> dict:
    print(f"\n\U0001F50D Testing: {scenario_name}")
    print("-" * 40)

    try:
        customization_info = compass.get_customization_summary()
        ceo_name = customization_info['ceo_profile'].get('name', 'Unknown')
        leadership_style = customization_info['ceo_profile'].get('leadership_style', 'unknown')

        print(f"CEO: {ceo_name}")
        print(f"Leadership Style: {leadership_style}")
        print(f"Custom Prompts: {len(customization_info['custom_prompts'])}")
        print(f"Focus Areas: {customization_info['ceo_profile'].get('communication_preferences', {}).get('focus_areas', [])}")

        result = compass.analyze_organization(
            raw_communication=communication_data,
            communication_type=comm_type
        )

        if result['status'] == 'success':
            print("\u2705 Analysis completed successfully!")
            dashboard = result['ceo_dashboard']
            executive_summary = dashboard.get('executive_summary', {})
            key_insights = dashboard.get('key_insights', {})
            recommendations = dashboard.get('actionable_recommendations', {})
            customization_info = result.get('customization_info', {})

            print(f"\n\U0001F4CA Results for {customization_info.get('analyzed_for', ceo_name)}:")
            print(f"  • Team Health: {executive_summary.get('overall_team_health', 0):.2f}/1.0")
            print(f"  • Leadership Impact: {executive_summary.get('leadership_impact_score', 0):.2f}/1.0")
            print(f"  • Risk Level: {executive_summary.get('organizational_risk_level', 'unknown').title()}")

            print("\n\U0001F3AF Key Insights:")
            for strength in key_insights.get('team_strengths', [])[:2]:
                print(f"  ✓ {strength}")

            for concern in key_insights.get('areas_of_concern', [])[:2]:
                print(f"  ⚠ {concern}")

            print("\n\U0001F680 Immediate Actions:")
            for action in recommendations.get('immediate_actions', [])[:2]:
                print(f"  • {action}")

            print("\n\U0001F527 Customization Impact:")
            print(f"  • Analysis customized for: {customization_info.get('leadership_style', 'unknown')} leader")
            print(f"  • Focus areas: {', '.join(customization_info.get('focus_areas', []))}")
            if customization_info.get('custom_prompts_used'):
                print(f"  • Custom prompts used: {', '.join(customization_info.get('custom_prompts_used', []))}")

            return {
                'scenario': scenario_name,
                'status': 'PASSED',
                'team_health': executive_summary.get('overall_team_health', 0),
                'customization_level': len(customization_info.get('custom_prompts_used', [])),
                'ceo_name': ceo_name
            }
        else:
            print(f"\u274c Analysis failed: {result.get('error', 'Unknown error')}")
            return {
                'scenario': scenario_name,
                'status': 'FAILED',
                'error': result.get('error', 'Unknown error')
            }

    except Exception as e:
        print(f"\u274c Test failed with exception: {str(e)}")
        return {
            'scenario': scenario_name,
            'status': 'ERROR',
            'error': str(e)
        }

def print_test_summary(test_results: list):
    print("\n" + "=" * 80)
    print("\U0001F3AF CEO COMPASS PARODY TEST SUMMARY")
    print("=" * 80)

    passed_tests = [r for r in test_results if r['status'] == 'PASSED']
    failed_tests = [r for r in test_results if r['status'] in ['FAILED', 'ERROR']]

    print(f"\u2705 Successful Analyses: {len(passed_tests)}/{len(test_results)}")
    print(f"\u274c Failed Analyses: {len(failed_tests)}/{len(test_results)}")

    for result in passed_tests:
        customization_level = "High" if result.get('customization_level', 0) > 0 else "Template"
        print(f"  • {result['scenario']}: {result['team_health']:.2f} health ({customization_level} customization)")

    if failed_tests:
        print("\n\u274c Analysis Failures:")
        for result in failed_tests:
            print(f"  • {result['scenario']}: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    run_ceo_compass_test()
