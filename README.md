# CEO Compass - Organizational Communication Intelligence

AI-powered communication analysis that gives CEOs strategic insights into their organization's health, culture, and leadership effectiveness.

## 🎯 What CEO Compass Does

CEO Compass analyzes your team's communication patterns to provide actionable insights on:

- **Leadership Effectiveness**: How well are leaders communicating and engaging teams?
- **Organizational Alignment**: Are teams aligned on goals, priorities, and strategy?
- **Cultural Health**: Is your culture fostering innovation, collaboration, and psychological safety?
- **Risk Detection**: Early warning signals for team dysfunction or cultural issues
- **Performance Intelligence**: Team collaboration, execution effectiveness, and talent retention risks

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run CEO scenarios test
python main.py
```

## 🏗 Architecture

```
ceo_compass/
├── __init__.py              # Package initialization
├── ceo_compass.py          # Core CEOCompass intelligence system
├── state.py                # Organizational state management
├── nodes.py                # LangGraph analysis workflow nodes
├── parsers.py              # Multi-format communication parsing
├── prompts.py              # CEO-focused analysis prompts
├── utils.py                # Validation and summary utilities
├── test_scenarios.py       # Realistic CEO test scenarios
└── main.py                 # Main entry point
```

## 📊 CEO Dashboard Output

```python
from ceo_compass import CEOCompass

compass = CEOCompass(openai_api_key="your-key")

result = compass.analyze_organization(
    raw_communication="Your team communication...",
    communication_type="team_meeting"  # or "leadership_email", "all_hands", "slack_channel"
)

dashboard = result['ceo_dashboard']
print(f"Team Health: {dashboard['executive_summary']['overall_team_health']:.2f}")
print(f"Risk Level: {dashboard['executive_summary']['organizational_risk_level']}")
```

## 🎯 Key Features

### Leadership Intelligence
- Communication clarity and effectiveness scoring
- Team engagement fostering analysis  
- Decision-making efficiency assessment
- Psychological safety creation measurement

### Organizational Health
- Goal clarity and priority consensus tracking
- Cultural health indicators monitoring
- Information flow analysis (upward, lateral, downward)
- Early warning signal detection

### Strategic Recommendations
- Immediate actions for CEO attention
- 30-day focus areas for sustained improvement
- Strategic initiatives for long-term organizational health
- Success indicators to monitor

## 🔍 Supported Communication Types

- **Team Meetings**: Sprint planning, standups, retrospectives
- **Leadership Emails**: Executive communication threads
- **All-Hands**: Company-wide meetings and announcements  
- **Slack Channels**: Ongoing team conversations

## 📈 CEO Value Proposition

**Traditional approach**: CEOs rely on filtered reports and annual surveys to understand organizational health.

**CEO Compass approach**: Real-time communication intelligence that reveals:
- How leadership communication actually lands with teams
- Whether your culture initiatives are working
- Early signals of team dysfunction before they become crises
- Specific, actionable areas for leadership improvement

## 🏆 Perfect for

- **Scaling Startups**: Maintain culture and effectiveness during rapid growth
- **Remote Teams**: Understand dynamics when you can't observe in person
- **Leadership Development**: Data-driven feedback on communication effectiveness
- **Cultural Transformation**: Monitor progress on cultural change initiatives
- **Board Reporting**: Quantitative insights on organizational health

This system transforms communication data into strategic intelligence, giving CEOs the organizational awareness they need to lead effectively.