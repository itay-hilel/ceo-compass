import json
from typing import List, Dict, Any

class CEOPromptTemplates:
    """LLM prompts designed for CEO organizational insights"""
    
    @staticmethod
    def leadership_effectiveness_prompt(messages: List[Dict[str, Any]], team_metadata: Dict[str, Any]) -> str:
        """Analyze leadership effectiveness and communication style"""
        
        leadership_messages = [m for m in messages if m.get('is_leadership', False)]
        team_messages = [m for m in messages if not m.get('is_leadership', False)]
        
        conversation_text = "\n".join([
            f"[{'LEADER' if msg.get('is_leadership') else 'TEAM'}] {msg.get('speaker', 'Unknown')}: {msg.get('content', '')}"
            for msg in messages[:25]
        ])
        
        return f"""
As a senior organizational consultant, analyze leadership effectiveness in this communication:

{conversation_text}

Context: {len(leadership_messages)} leadership contributions, {len(team_messages)} team contributions
Team Metadata: {json.dumps(team_metadata, indent=2)}

IMPORTANT: Respond with ONLY valid JSON. No explanations, no markdown formatting, no additional text.

Provide analysis as JSON:
{{
    "leadership_effectiveness": {{
        "communication_clarity": 0.0 to 1.0,
        "team_engagement_fostered": 0.0 to 1.0,
        "decision_making_efficiency": 0.0 to 1.0,
        "psychological_safety_created": 0.0 to 1.0
    }},
    "leadership_style_indicators": {{
        "directive_vs_collaborative": -1.0 to 1.0,
        "micromanaging_signals": 0.0 to 1.0,
        "empowerment_level": 0.0 to 1.0,
        "transparency_score": 0.0 to 1.0
    }},
    "team_response_patterns": {{
        "openness_to_share": 0.0 to 1.0,
        "innovation_comfort": 0.0 to 1.0,
        "dissent_expression": 0.0 to 1.0,
        "engagement_energy": 0.0 to 1.0
    }},
    "red_flags": ["flag1", "flag2"],
    "positive_leadership_moments": ["moment1", "moment2"]
}}
"""
    
    @staticmethod
    def organizational_alignment_prompt(messages: List[Dict[str, Any]], team_metadata: Dict[str, Any]) -> str:
        """Analyze organizational alignment and culture indicators"""
        
        conversation_text = "\n".join([
            f"{msg.get('speaker', 'Unknown')}: {msg.get('content', '')}"
            for msg in messages[:25]
        ])
        
        return f"""
As a CEO's strategic advisor, analyze organizational alignment and cultural health:

{conversation_text}

Team Context: {json.dumps(team_metadata, indent=2)}

IMPORTANT: Respond with ONLY valid JSON. No explanations, no markdown formatting, no additional text.

Provide strategic insights as JSON:
{{
    "organizational_alignment": {{
        "goal_clarity": 0.0 to 1.0,
        "priority_consensus": 0.0 to 1.0,
        "role_clarity": 0.0 to 1.0,
        "strategic_understanding": 0.0 to 1.0
    }},
    "cultural_health_indicators": {{
        "collaboration_quality": 0.0 to 1.0,
        "innovation_mindset": 0.0 to 1.0,
        "accountability_culture": 0.0 to 1.0,
        "learning_orientation": 0.0 to 1.0
    }},
    "information_flow": {{
        "upward_transparency": 0.0 to 1.0,
        "lateral_coordination": 0.0 to 1.0,
        "decision_communication": 0.0 to 1.0
    }},
    "early_warning_signals": ["signal1", "signal2"],
    "cultural_strengths": ["strength1", "strength2"],
    "recommended_interventions": ["intervention1", "intervention2"]
}}
}}
"""
    
    @staticmethod
    def team_performance_synthesis_prompt(leadership_analysis: Dict[str, Any], alignment_analysis: Dict[str, Any], team_metadata: Dict[str, Any]) -> str:
        """Synthesize insights into CEO-actionable dashboard"""
        
        analysis_summary = {
            "leadership_analysis": leadership_analysis,
            "alignment_analysis": alignment_analysis,
            "team_metadata": team_metadata
        }
        
        return f"""
As a CEO's chief of staff, synthesize this organizational communication analysis into actionable insights:

{json.dumps(analysis_summary, indent=2)}

IMPORTANT: Respond with ONLY valid JSON. No explanations, no markdown formatting, no additional text.

Create a comprehensive CEO dashboard as JSON:
{{
    "executive_summary": {{
        "overall_team_health": 0.0 to 1.0,
        "leadership_impact_score": 0.0 to 1.0,
        "organizational_risk_level": "low|medium|high|critical",
        "intervention_urgency": "none|monitor|action_needed|immediate"
    }},
    "key_insights": {{
        "team_strengths": ["strength1", "strength2", "strength3"],
        "areas_of_concern": ["concern1", "concern2"],
        "leadership_opportunities": ["opportunity1", "opportunity2"],
        "cultural_evolution": "positive|stable|declining|concerning"
    }},
    "actionable_recommendations": {{
        "immediate_actions": ["action1", "action2"],
        "30_day_focus_areas": ["area1", "area2"],
        "strategic_initiatives": ["initiative1", "initiative2"]
    }},
    "performance_metrics": {{
        "team_collaboration_index": 0.0 to 1.0,
        "innovation_capacity_score": 0.0 to 1.0,
        "execution_effectiveness": 0.0 to 1.0,
        "talent_retention_risk": 0.0 to 1.0
    }},
    "next_conversation_focus": ["topic1", "topic2"],
    "success_indicators_to_monitor": ["indicator1", "indicator2"]
}}
"""