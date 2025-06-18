# CEO Compass - Personalized Organizational Intelligence

AI-powered communication analysis that adapts to **your** leadership style and gives you strategic insights tailored to your specific needs as a CEO.

## 🎯 What Makes CEO Compass Different

CEO Compass doesn't give generic advice - it learns your leadership style, company stage, and focus areas to provide **personalized organizational intelligence**:

- **🎨 Personalized Analysis**: Analysis customized for your leadership style (collaborative, directive, coaching, strategic)
- **🏢 Company Stage Aware**: Different insights for startup, growth, and enterprise-stage companies  
- **🎯 Focus Area Alignment**: Emphasizes what matters most to you (execution, culture, team health, innovation)
- **📝 Custom Prompts**: Replace our templates with your own analysis frameworks
- **🤖 Leadership Adaptation**: AI adapts tone and recommendations to your intervention preferences

## 💡 CEO Personas Supported

**Startup CEO ("Move Fast" Mode)**
```python
compass = create_startup_ceo_compass(api_key, "Sarah Chen", "TechCorp")
# Focuses on: execution, team health, scaling challenges
# Style: Direct, concise, action-oriented
```

**Enterprise CEO ("Strategic" Mode)** 
```python
compass = create_enterprise_ceo_compass(api_key, "Michael Rodriguez", "BigCorp")  
# Focuses on: culture, innovation, organizational alignment
# Style: Comprehensive, diplomatic, systemic thinking
```

**Custom CEO Profile**
```python
your_profile = {
    "name": "Your Name",
    "leadership_style": "coaching",  # collaborative, directive, coaching, strategic
    "focus_areas": ["team_development", "innovation", "culture"],
    "intervention_preference": "coaching"  # coaching, directive, hands_off
}
compass = CEOCompass(api_key, ceo_profile=your_profile)
```

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables  
export OPENAI_API_KEY="your-openai-api-key"

# Quick test with your CEO style
python -c "
from ceo_compass import create_startup_ceo_compass
compass = create_startup_ceo_compass('your-api-key', 'Your Name', 'Your Company')
compass.demonstrate_customization()
"

# Run comprehensive CEO persona tests
python -m ceo_compass.test_scenarios
```

## 🎯 Core Intelligence Features

What CEO Compass analyzes for **you**:

- **👑 Leadership Effectiveness**: How well are your leaders communicating in your preferred style?
- **🎯 Organizational Alignment**: Are teams aligned on what matters most to you?
- **💪 Cultural Health**: Is your culture evolving the way you want it to?
- **⚠️ Risk Detection**: Early warnings calibrated to your risk tolerance
- **📊 Performance Intelligence**: Metrics that matter for your company stage and goals

## 🛠 Customization Examples

**Set Your Analysis Focus**
```python
compass.update_ceo_profile({
    "focus_areas": ["execution", "team_health", "scaling"],
    "directness_level": 0.8,  # Very direct feedback
    "intervention_preference": "coaching"
})
```

**Use Your Own Analysis Framework**
```python
compass.set_custom_prompt("leadership_effectiveness", """
As my leadership coach, focus on:
1. How well managers are developing their people
2. Decision-making speed under pressure  
3. Team morale during our growth phase

My philosophy: Servant leadership that drives results.
""")
```

**Quick CEO Setups**
```python
# For hands-on startup CEOs
compass.setup_for_startup_ceo("Elon Jr", "RocketChat")

# For strategic enterprise CEOs  
compass.setup_for_enterprise_ceo("Mary Smith", "Global Industries")
```

## 🏗 Architecture

```
ceo_compass/
├── ceo_compass.py          # 🧠 Core personalized intelligence system
├── nodes.py                # 🔄 Customizable analysis workflow  
├── prompts.py              # 📝 CEO-adaptable prompt templates
├── parsers.py              # 📊 Multi-format communication parsing
├── state.py                # 🏛 Organizational state management
├── utils.py                # 🛠 Validation and summary utilities
└── test_scenarios.py       # 🎭 CEO persona test scenarios
```

**Key Innovation**: Every component adapts to your CEO profile and preferences.

## 📈 Your Personalized CEO Value

**Before CEO Compass**: Generic org analysis that doesn't match your leadership style.

**With CEO Compass**: 
- **🎯 Tailored Insights**: Analysis that speaks your language and priorities
- **⚡ Your Style**: Recommendations that fit how you actually lead
- **🎨 Your Focus**: Emphasizes what matters most for your company stage
- **🔧 Your Framework**: Use your own mental models and analysis approaches
- **📊 Your Metrics**: Track what success looks like for your leadership style

## 🎭 Real CEO Examples

Our test scenarios include parody versions of famous CEO styles:

**"Elon Mode" (Visionary/Chaotic)**
- Focus: Speed, innovation, disruption
- Style: Direct, fast-moving, paradigm-shifting
- Intervention: Command and inspire

**"Sam Altman Mode" (Strategic/Philosophical)**  
- Focus: Long-term alignment, existential considerations
- Style: Thoughtful, consensus-building, big picture
- Intervention: Socratic questioning

**"Adam Neumann Mode" (Charismatic/Visionary)**
- Focus: Culture, community, flow state
- Style: Inspirational, esoteric, vision-driven  
- Intervention: Motivational storytelling

## 🎯 Perfect For Your Leadership Journey

- **🚀 Scaling Startups**: Maintain your culture while growing fast
- **🏢 Remote Leadership**: Understand team dynamics from anywhere
- **📚 Leadership Development**: Get feedback that matches your style
- **🔄 Organizational Change**: Navigate transitions with personalized intelligence
- **🎨 Culture Building**: Shape culture that aligns with your vision

**Bottom Line**: CEO Compass doesn't just analyze your organization - it learns how **you** think and adapts its intelligence to help **you** lead more effectively.