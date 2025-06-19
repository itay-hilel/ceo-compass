# CEO Compass – Communication Health Analysis with LangGraph

CEO Compass analyzes internal communication—messages and meeting transcripts—to provide structured insights into communication health. It leverages LangGraph for workflow orchestration and OpenAI for contextual language analysis.

---

## Overview

This project was built as a take-home assignment. It demonstrates:

* LangGraph-powered multi-stage analysis
* Integration with OpenAI's API for natural language understanding
* Structured JSON output with scores and reasoning
* Adaptability to various CEO profiles and leadership styles 

---

## Communication Health Dimensions

The system evaluates five key dimensions:

* **Leadership Effectiveness** – Are leaders communicating clearly and consistently?
* **Organizational Alignment** – Do teams share priorities and coordinate well?
* **Cultural Health** – What tone and values emerge from the communication?
* **Risk Detection** – Are there signals of misalignment or friction?
* **Engagement Patterns** – How distributed and active is participation?

---

## Workflow Architecture

The LangGraph workflow runs sequential analysis nodes:

```
Input → Preprocessing → Leadership Analysis → Team Health → Risk Detection → Summary
```

Each stage uses a specialized OpenAI prompt for focused analysis.
---

## Quick Start

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-openai-api-key"
python main.py
```

Or run in code:

```python
from ceo_compass import CEOCompass

compass = CEOCompass("your-api-key")
result = compass.analyze_communication_health({
    "messages": ["Internal thread..."],
    "meeting_transcripts": ["Transcript..."]
})

print(result)
```

Run test personas:

```bash
python -m ceo_compass.test_scenarios
```

---

## Example Output

```json
{
  "communication_health_score": 7.2,
  "analysis_breakdown": {
    "leadership_effectiveness": {
      "score": 8.1,
      "key_findings": ["Clear leadership communication", "Consistent messaging"]
    },
    "team_alignment": {
      "score": 6.8,
      "key_findings": ["Shared goals mentioned in multiple exchanges"]
    }
  },
  "reasoning_explanation": "Strong leadership signals; moderate alignment gaps."
}
```

---

## CEO Profiles

The system supports predefined and custom leadership profiles:

```python
# Startup CEO
compass = create_startup_ceo_compass(api_key, "Sarah", "TechCorp")

# Enterprise CEO
compass = create_enterprise_ceo_compass(api_key, "Michael", "BigCorp")

# Custom CEO
profile = {
    "name": "Alex",
    "leadership_style": "coaching",
    "focus_areas": ["execution", "culture"],
    "intervention_preference": "hands_off"
}
compass = CEOCompass(api_key, ceo_profile=profile)
```

---

## Customization

Update your analysis strategy:

```python
compass.update_ceo_profile({
    "focus_areas": ["scaling", "team_health"],
    "directness_level": 0.9,
    "intervention_preference": "coaching"
})

compass.set_custom_prompt("leadership_effectiveness", """
Evaluate:
1. How well leaders support people development
2. Speed of decision-making
3. Morale through uncertainty
""")
```

---

## File Structure

```text
ceo_compass/
├── ceo_compass.py         # Core logic
├── nodes.py               # LangGraph node definitions
├── prompts.py             # Prompt templates
├── parsers.py             # Parsing utilities
├── state.py               # Organizational profile management
├── utils.py               # Helpers
└── test_scenarios.py      # Persona tests
```

---

## CEO Modes (Demo Personas)

These test cases simulate different leadership styles:

* **Elon Mode** – Fast, disruptive, execution-focused
* **Sam Altman Mode** – Strategic, consensus-building, future-focused
* **Adam Neumann Mode** – Inspirational, culture-focused, abstract

---

## Use Cases

CEO Compass is designed for:

* Scaling startups
* Remote team leaders
* Leadership development
* Cultural transformation
* Early risk detection in org dynamics 

---

**Bottom line**: CEO Compass gives CEOs actionable insights tailored to how they think and lead—making it easier to guide teams, grow culture, and catch problems early.