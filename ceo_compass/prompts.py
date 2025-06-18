import json
from typing import List, Dict, Any, Optional

class CEOPromptTemplates:
    """Enhanced LLM prompts with user customization support"""
    
    def __init__(self, ceo_profile: Optional[Dict[str, Any]] = None):
        """Initialize with optional CEO customization profile"""
        self.ceo_profile = ceo_profile or self._get_default_profile()
        self.custom_prompts = {}  # Store user-customized prompts
        
    def _get_default_profile(self) -> Dict[str, Any]:
        """Default CEO profile - users can override this"""
        return {
            "name": "CEO",
            "company_stage": "growth",
            "leadership_style": "collaborative", 
            "communication_preferences": {
                "directness_level": 0.7,  # 0-1 scale
                "detail_preference": "concise",  # concise, detailed, comprehensive
                "focus_areas": ["execution", "team_health", "culture"]
            },
            "decision_style": "data_driven",  # data_driven, intuitive, consensus
            "intervention_preference": "coaching"  # coaching, directive, hands_off
        }
    
    def set_custom_prompt(self, prompt_type: str, custom_prompt: str):
        """Allow CEO to completely customize a prompt"""
        self.custom_prompts[prompt_type] = custom_prompt
    
    def leadership_effectiveness_prompt(self, messages: List[Dict[str, Any]], team_metadata: Dict[str, Any]) -> str:
        """Analyze leadership effectiveness with CEO customization"""
        
        # Check if CEO has custom prompt for this analysis
        if "leadership_effectiveness" in self.custom_prompts:
            return self._apply_custom_prompt("leadership_effectiveness", {
                "messages": messages,
                "team_metadata": team_metadata
            })
        
        # Use enhanced template-based approach
        return self._get_leadership_template(messages, team_metadata)
    
    def _get_leadership_template(self, messages: List[Dict[str, Any]], team_metadata: Dict[str, Any]) -> str:
        """Enhanced leadership prompt template with CEO personalization"""
        
        leadership_messages = [m for m in messages if m.get('is_leadership', False)]
        team_messages = [m for m in messages if not m.get('is_leadership', False)]
        
        conversation_text = "\n".join([
            f"[{'LEADER' if msg.get('is_leadership') else 'TEAM'}] {msg.get('speaker', 'Unknown')}: {msg.get('content', '')}"
            for msg in messages[:25]
        ])
        
        # Get CEO-specific analysis focus
        ceo_focus = self._get_leadership_focus()
        ceo_context = self._get_ceo_context_string()
        
        return f"""
As {self.ceo_profile['name']}'s senior organizational consultant, analyze leadership effectiveness in this communication.

{ceo_context}

{conversation_text}

Context: {len(leadership_messages)} leadership contributions, {len(team_messages)} team contributions
Team Metadata: {json.dumps(team_metadata, indent=2)}

{ceo_focus}

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
    "ceo_specific_insights": {{
        "matches_preferred_style": 0.0 to 1.0,
        "actionability_score": 0.0 to 1.0,
        "alignment_with_culture_goals": 0.0 to 1.0
    }},
    "red_flags": ["flag1", "flag2"],
    "positive_leadership_moments": ["moment1", "moment2"],
    "personalized_recommendations": ["action1", "action2"]
}}
"""
    
    def _get_leadership_focus(self) -> str:
        """Generate CEO-specific analysis focus based on their profile"""
        
        style = self.ceo_profile.get('leadership_style', 'collaborative')
        focus_areas = self.ceo_profile.get('communication_preferences', {}).get('focus_areas', [])
        decision_style = self.ceo_profile.get('decision_style', 'data_driven')
        
        focus_instructions = []
        
        if style == "collaborative":
            focus_instructions.append("Pay special attention to how well leaders are fostering collaboration and shared decision-making.")
        elif style == "directive":
            focus_instructions.append("Focus on clarity of direction and decisiveness in leadership communication.")
        elif style == "coaching":
            focus_instructions.append("Analyze how well leaders are developing their team members and providing growth opportunities.")
        
        if "execution" in focus_areas:
            focus_instructions.append("Evaluate execution effectiveness: Are decisions leading to clear actions and deadlines?")
        
        if "team_health" in focus_areas:
            focus_instructions.append("Monitor team wellbeing signals: stress levels, workload balance, and morale indicators.")
        
        if "culture" in focus_areas:
            focus_instructions.append("Assess cultural alignment: Do behaviors match stated company values?")
        
        if decision_style == "data_driven":
            focus_instructions.append("Look for evidence-based decision making and use of metrics in discussions.")
        
        return "ANALYSIS FOCUS:\n" + "\n".join(f"- {instruction}" for instruction in focus_instructions)
    
    def _get_ceo_context_string(self) -> str:
        """Create context string about the CEO for the analysis"""
        
        profile = self.ceo_profile
        
        context_parts = [
            f"CEO Profile: {profile.get('name')} leads a {profile.get('company_stage')} company",
            f"Leadership Style: {profile.get('leadership_style')}",
            f"Decision Style: {profile.get('decision_style')}",
            f"Intervention Preference: {profile.get('intervention_preference')}"
        ]
        
        return "CEO CONTEXT:\n" + "\n".join(context_parts) + "\n"
    
    def organizational_alignment_prompt(self, messages: List[Dict[str, Any]], team_metadata: Dict[str, Any]) -> str:
        """Analyze organizational alignment with CEO customization"""
        
        # Check for custom prompt
        if "organizational_alignment" in self.custom_prompts:
            return self._apply_custom_prompt("organizational_alignment", {
                "messages": messages,
                "team_metadata": team_metadata
            })
        
        return self._get_alignment_template(messages, team_metadata)
    
    def _get_alignment_template(self, messages: List[Dict[str, Any]], team_metadata: Dict[str, Any]) -> str:
        """Enhanced alignment prompt template"""
        
        conversation_text = "\n".join([
            f"{msg.get('speaker', 'Unknown')}: {msg.get('content', '')}"
            for msg in messages[:25]
        ])
        
        ceo_context = self._get_ceo_context_string()
        alignment_focus = self._get_alignment_focus()
        
        return f"""
As {self.ceo_profile['name']}'s strategic advisor, analyze organizational alignment and cultural health:

{ceo_context}

{conversation_text}

Team Context: {json.dumps(team_metadata, indent=2)}

{alignment_focus}

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
    "ceo_alignment_metrics": {{
        "strategy_cascade": 0.0 to 1.0,
        "culture_match": 0.0 to 1.0,
        "execution_alignment": 0.0 to 1.0
    }},
    "early_warning_signals": ["signal1", "signal2"],
    "cultural_strengths": ["strength1", "strength2"],
    "recommended_interventions": ["intervention1", "intervention2"]
}}
"""
    
    def _get_alignment_focus(self) -> str:
        """CEO-specific alignment analysis focus"""
        
        focus_areas = self.ceo_profile.get('communication_preferences', {}).get('focus_areas', [])
        company_stage = self.ceo_profile.get('company_stage', 'growth')
        
        focus_instructions = []
        
        if company_stage == "startup":
            focus_instructions.append("Focus on alignment during rapid change and resource constraints.")
        elif company_stage == "growth" or company_stage == "scaling":
            focus_instructions.append("Pay attention to alignment challenges during scaling and process formalization.")
        elif company_stage == "mature":
            focus_instructions.append("Look for alignment on strategic initiatives and cultural evolution.")
        
        if "execution" in focus_areas:
            focus_instructions.append("Evaluate how well strategic goals translate into day-to-day execution.")
        
        if "culture" in focus_areas:
            focus_instructions.append("Assess whether team behaviors align with stated cultural values.")
        
        return "ALIGNMENT FOCUS:\n" + "\n".join(f"- {instruction}" for instruction in focus_instructions)
    
    def team_performance_synthesis_prompt(self, leadership_analysis: Dict[str, Any], alignment_analysis: Dict[str, Any], team_metadata: Dict[str, Any]) -> str:
        """Synthesize insights with CEO customization"""
        
        # Check for custom synthesis prompt
        if "synthesis" in self.custom_prompts:
            return self._apply_custom_prompt("synthesis", {
                "leadership_analysis": leadership_analysis,
                "alignment_analysis": alignment_analysis,
                "team_metadata": team_metadata
            })
        
        return self._get_synthesis_template(leadership_analysis, alignment_analysis, team_metadata)
    
    def _get_synthesis_template(self, leadership_analysis: Dict[str, Any], alignment_analysis: Dict[str, Any], team_metadata: Dict[str, Any]) -> str:
        """Enhanced synthesis template with CEO personalization"""
        
        analysis_summary = {
            "leadership_analysis": leadership_analysis,
            "alignment_analysis": alignment_analysis,
            "team_metadata": team_metadata
        }
        
        ceo_context = self._get_ceo_context_string()
        synthesis_focus = self._get_synthesis_focus()
        
        return f"""
As {self.ceo_profile['name']}'s chief of staff, synthesize this organizational communication analysis into actionable insights:

{ceo_context}

{synthesis_focus}

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
    "ceo_specific_insights": {{
        "style_effectiveness": 0.0 to 1.0,
        "culture_goal_progress": 0.0 to 1.0,
        "decision_impact_score": 0.0 to 1.0
    }},
    "next_conversation_focus": ["topic1", "topic2"],
    "success_indicators_to_monitor": ["indicator1", "indicator2"]
}}
"""
    
    def _get_synthesis_focus(self) -> str:
        """CEO-specific synthesis focus"""
        
        intervention_pref = self.ceo_profile.get('intervention_preference', 'coaching')
        directness = self.ceo_profile.get('communication_preferences', {}).get('directness_level', 0.7)
        
        focus_instructions = []
        
        if intervention_pref == "coaching":
            focus_instructions.append("Frame recommendations as coaching opportunities and development initiatives.")
        elif intervention_pref == "directive": 
            focus_instructions.append("Provide clear, actionable directives with specific steps and timelines.")
        elif intervention_pref == "hands_off":
            focus_instructions.append("Focus on systemic changes and structural improvements rather than individual interventions.")
        
        if directness > 0.7:
            focus_instructions.append("Be direct about problems and solutions. This CEO prefers candid assessment.")
        else:
            focus_instructions.append("Frame insights diplomatically while maintaining accuracy.")
        
        return "SYNTHESIS FOCUS:\n" + "\n".join(f"- {instruction}" for instruction in focus_instructions)
    
    def _apply_custom_prompt(self, prompt_type: str, variables: Dict[str, Any]) -> str:
        """Apply a user's custom prompt with variable substitution"""
        
        custom_prompt = self.custom_prompts[prompt_type]
        
        # Simple variable substitution - could be enhanced
        for var_name, var_value in variables.items():
            placeholder = f"{{{var_name}}}"
            if placeholder in custom_prompt:
                if isinstance(var_value, (dict, list)):
                    custom_prompt = custom_prompt.replace(placeholder, json.dumps(var_value, indent=2))
                else:
                    custom_prompt = custom_prompt.replace(placeholder, str(var_value))
        
        return custom_prompt
    
    # Convenience methods for quick customization
    def customize_for_startup_ceo(self, name: str = "Startup CEO"):
        """Quick setup for typical startup CEO"""
        self.ceo_profile.update({
            "name": name,
            "company_stage": "startup",
            "leadership_style": "hands_on",
            "communication_preferences": {
                "directness_level": 0.8,
                "detail_preference": "concise",
                "focus_areas": ["execution", "team_health", "scaling"]
            },
            "decision_style": "data_driven",
            "intervention_preference": "coaching"
        })
    
    def customize_for_enterprise_ceo(self, name: str = "Enterprise CEO"):
        """Quick setup for enterprise CEO"""
        self.ceo_profile.update({
            "name": name,
            "company_stage": "mature",
            "leadership_style": "strategic",
            "communication_preferences": {
                "directness_level": 0.6,
                "detail_preference": "comprehensive",
                "focus_areas": ["culture", "innovation", "alignment"]
            },
            "decision_style": "consensus",
            "intervention_preference": "directive"
        })
    
    def get_profile_summary(self) -> str:
        """Get a summary of current CEO profile for debugging"""
        return json.dumps(self.ceo_profile, indent=2)
    
    def list_customizable_prompts(self) -> List[str]:
        """List all prompts that can be customized"""
        return [
            "leadership_effectiveness",
            "organizational_alignment", 
            "synthesis"
        ]