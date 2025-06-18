import json
import logging
import re
from datetime import datetime
from typing import Optional
from openai import OpenAI
from langchain_core.runnables import RunnableConfig
from .state import OrganizationalState
from .parsers import OrganizationalParser
from .prompts import CEOPromptTemplates  # Using enhanced version
from .utils import validate_ceo_dashboard_schema

logger = logging.getLogger(__name__)

class CEOAnalysisNodes:
    """Enhanced LangGraph workflow nodes with CEO customization support"""
    
    def __init__(self, openai_client: OpenAI, ceo_profile: Optional[dict] = None):
        self.client = openai_client
        self.parser = OrganizationalParser()
        
        # Initialize with CEO-customized prompts
        self.prompts = CEOPromptTemplates(ceo_profile)
        
        # Store CEO profile for context
        self.ceo_profile = ceo_profile or {}
    
    def update_ceo_profile(self, new_profile: dict):
        """Allow updating CEO profile during runtime"""
        self.ceo_profile.update(new_profile)
        self.prompts = CEOPromptTemplates(self.ceo_profile)
        logger.info(f"Updated CEO profile for: {new_profile.get('name', 'Unknown CEO')}")
    
    def set_custom_prompt(self, prompt_type: str, custom_prompt: str):
        """Allow setting completely custom prompts"""
        self.prompts.set_custom_prompt(prompt_type, custom_prompt)
        logger.info(f"Set custom prompt for: {prompt_type}")
    
    def _safe_json_parse(self, content: str) -> dict:
        """Safely parse JSON from OpenAI response, handling extra content"""
        try:
            # First, try direct parsing
            return json.loads(content)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON from the content
            try:
                # Look for JSON object boundaries
                start_idx = content.find('{')
                if start_idx == -1:
                    raise ValueError("No JSON object found in response")
                
                # Find the matching closing brace
                brace_count = 0
                end_idx = start_idx
                for i in range(start_idx, len(content)):
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i + 1
                            break
                
                if brace_count != 0:
                    raise ValueError("Unmatched braces in JSON")
                
                json_content = content[start_idx:end_idx]
                return json.loads(json_content)
                
            except (ValueError, json.JSONDecodeError) as e:
                logger.error(f"Failed to parse JSON from content: {content[:200]}...")
                raise ValueError(f"JSON parsing failed: {str(e)}")
    
    def _get_model_config(self, config: Optional[RunnableConfig] = None) -> dict:
        """Extract model configuration from workflow config"""
        if not config or "configurable" not in config:
            return {
                "model": "gpt-4",
                "temperature": 0.3,
                "max_retries": 3
            }
        
        configurable = config["configurable"]
        return {
            "model": configurable.get("model_name", "gpt-4"),
            "temperature": configurable.get("temperature", 0.3),
            "max_retries": configurable.get("max_retries", 3)
        }
    
    def _extract_ceo_profile_from_config(self, config: Optional[RunnableConfig] = None) -> dict:
        """Extract CEO profile from config if provided"""
        if config and "configurable" in config:
            return config["configurable"].get("ceo_profile", self.ceo_profile)
        return self.ceo_profile
    
    def preprocess_organizational_data(
        self, 
        state: OrganizationalState, 
        config: Optional[RunnableConfig] = None
    ) -> OrganizationalState:
        """Parse and structure organizational communication data"""
        logger.info("Processing organizational communication data...")
        
        try:
            # Check if CEO profile was passed in config
            runtime_ceo_profile = self._extract_ceo_profile_from_config(config)
            if runtime_ceo_profile != self.ceo_profile:
                self.update_ceo_profile(runtime_ceo_profile)
            
            raw_input = state.get("raw_input", "")
            communication_type = state.get("communication_type", "auto")
            
            # Auto-detect if not specified
            if communication_type == "auto":
                communication_type = self.parser.auto_detect_communication_type(raw_input)
            
            # Parse based on organizational context
            if communication_type == "team_meeting":
                messages = self.parser.parse_team_meeting(raw_input)
            elif communication_type == "leadership_email":
                messages = self.parser.parse_leadership_email(raw_input)
            elif communication_type == "all_hands":
                messages = self.parser.parse_all_hands(raw_input)
            elif communication_type == "slack_channel":
                messages = self.parser.parse_slack_channel(raw_input)
            else:
                messages = self.parser.parse_team_meeting(raw_input)  # Default
            
            # Extract team dynamics
            team_metadata = self.parser.extract_team_dynamics(messages)
            
            # Add CEO context to metadata
            team_metadata["ceo_profile"] = self.ceo_profile
            
            return {
                **state,
                "messages": messages,
                "team_metadata": team_metadata,
                "communication_type": communication_type,
                "processing_stage": "data_processed"
            }
            
        except Exception as e:
            logger.error(f"Data processing error: {e}")
            return {
                **state,
                "error_context": f"Data processing failed: {str(e)}",
                "processing_stage": "error"
            }
    
    def analyze_leadership_effectiveness(
        self, 
        state: OrganizationalState, 
        config: Optional[RunnableConfig] = None
    ) -> OrganizationalState:
        """Analyze leadership effectiveness using CEO-customized prompts"""
        logger.info("Analyzing leadership effectiveness...")
        
        try:
            messages = state.get("messages", [])
            team_metadata = state.get("team_metadata", {})
            model_config = self._get_model_config(config)
            
            # Use CEO-customized prompt
            leadership_prompt = self.prompts.leadership_effectiveness_prompt(messages, team_metadata)
            
            # Add CEO context to system message
            ceo_name = self.ceo_profile.get('name', 'the CEO')
            system_message = f"You are a senior organizational consultant specializing in leadership effectiveness analysis for {ceo_name}. Your analysis should align with their leadership style and organizational goals."
            
            response = self.client.chat.completions.create(
                model=model_config["model"],
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": leadership_prompt}
                ],
                temperature=model_config["temperature"]
            )
            
            leadership_data = self._safe_json_parse(response.choices[0].message.content)
            
            # Add analysis metadata
            leadership_data["analysis_metadata"] = {
                "analyzed_for": ceo_name,
                "leadership_style": self.ceo_profile.get('leadership_style', 'unknown'),
                "customization_level": "template" if not self.prompts.custom_prompts.get("leadership_effectiveness") else "custom"
            }
            
            return {
                **state,
                "leadership_analysis": leadership_data,
                "processing_stage": "leadership_analyzed"
            }
            
        except Exception as e:
            logger.error(f"Leadership analysis error: {e}")
            return {
                **state,
                "error_context": f"Leadership analysis failed: {str(e)}",
                "processing_stage": "error"
            }
    
    def analyze_organizational_alignment(
        self, 
        state: OrganizationalState, 
        config: Optional[RunnableConfig] = None
    ) -> OrganizationalState:
        """Analyze organizational alignment using CEO-customized prompts"""
        logger.info("Analyzing organizational alignment...")
        
        try:
            messages = state.get("messages", [])
            team_metadata = state.get("team_metadata", {})
            model_config = self._get_model_config(config)
            
            # Use CEO-customized prompt
            alignment_prompt = self.prompts.organizational_alignment_prompt(messages, team_metadata)
            
            # Customize system message
            ceo_name = self.ceo_profile.get('name', 'the CEO')
            company_stage = self.ceo_profile.get('company_stage', 'growth')
            system_message = f"You are a strategic advisor helping {ceo_name} understand organizational health and culture in their {company_stage}-stage company."
            
            response = self.client.chat.completions.create(
                model=model_config["model"],
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": alignment_prompt}
                ],
                temperature=model_config["temperature"]
            )
            
            alignment_data = self._safe_json_parse(response.choices[0].message.content)
            
            # Add analysis metadata
            alignment_data["analysis_metadata"] = {
                "analyzed_for": ceo_name,
                "company_stage": company_stage,
                "focus_areas": self.ceo_profile.get('communication_preferences', {}).get('focus_areas', []),
                "customization_level": "template" if not self.prompts.custom_prompts.get("organizational_alignment") else "custom"
            }
            
            return {
                **state,
                "organizational_insights": alignment_data,
                "processing_stage": "alignment_analyzed"
            }
            
        except Exception as e:
            logger.error(f"Alignment analysis error: {e}")
            return {
                **state,
                "error_context": f"Alignment analysis failed: {str(e)}",
                "processing_stage": "error"
            }
    
    def synthesize_ceo_dashboard(
        self, 
        state: OrganizationalState, 
        config: Optional[RunnableConfig] = None
    ) -> OrganizationalState:
        """Create CEO-focused dashboard with personalized insights"""
        logger.info("Synthesizing CEO dashboard...")
        
        try:
            leadership_analysis = state.get("leadership_analysis", {})
            organizational_insights = state.get("organizational_insights", {})
            team_metadata = state.get("team_metadata", {})
            messages = state.get("messages", [])
            model_config = self._get_model_config(config)
            
            # Use CEO-customized synthesis prompt
            synthesis_prompt = self.prompts.team_performance_synthesis_prompt(
                leadership_analysis, organizational_insights, team_metadata
            )
            
            # Customize system message for synthesis
            ceo_name = self.ceo_profile.get('name', 'the CEO')
            intervention_style = self.ceo_profile.get('intervention_preference', 'coaching')
            system_message = f"You are {ceo_name}'s chief of staff, synthesizing organizational insights into actionable strategic guidance. Frame recommendations using a {intervention_style} approach."
            
            response = self.client.chat.completions.create(
                model=model_config["model"],
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": synthesis_prompt}
                ],
                temperature=model_config["temperature"]
            )
            
            ceo_dashboard = self._safe_json_parse(response.choices[0].message.content)
            
            # Add comprehensive analysis metadata
            config_info = config.get("configurable", {}) if config else {}
            ceo_dashboard["analysis_metadata"] = {
                "analysis_timestamp": datetime.now().isoformat(),
                "analyzed_for": ceo_name,
                "ceo_profile": self.ceo_profile,
                "communication_type": state.get("communication_type", "unknown"),
                "participants_analyzed": team_metadata.get("total_participants", 0),
                "messages_processed": len(messages),
                "leadership_participants": len([m for m in messages if m.get('is_leadership', False)]),
                "analysis_scope": "organizational_communication",
                "model_used": model_config["model"],
                "thread_id": config_info.get("thread_id", "unknown"),
                "customization_summary": {
                    "custom_prompts_used": list(self.prompts.custom_prompts.keys()),
                    "profile_based_customization": True,
                    "focus_areas": self.ceo_profile.get('communication_preferences', {}).get('focus_areas', [])
                }
            }
            
            return {
                **state,
                "ceo_dashboard": ceo_dashboard,
                "processing_stage": "dashboard_synthesized"
            }
            
        except Exception as e:
            logger.error(f"Dashboard synthesis error: {e}")
            return {
                **state,
                "error_context": f"Dashboard synthesis failed: {str(e)}",
                "processing_stage": "error"
            }
    
    def validate_insights(
        self, 
        state: OrganizationalState, 
        config: Optional[RunnableConfig] = None
    ) -> OrganizationalState:
        """Validate and finalize CEO insights"""
        logger.info("Validating CEO insights...")
        
        try:
            # Check if validation is enabled in config
            if config and config.get("configurable", {}).get("enable_validation", True):
                ceo_dashboard = state.get("ceo_dashboard", {})
                validate_ceo_dashboard_schema(ceo_dashboard)
                
                # Add validation success info
                validation_info = {
                    "validation_passed": True,
                    "validation_timestamp": datetime.now().isoformat(),
                    "validated_for": self.ceo_profile.get('name', 'Unknown CEO')
                }
                
                # Add validation info to dashboard metadata
                if "analysis_metadata" in ceo_dashboard:
                    ceo_dashboard["analysis_metadata"]["validation"] = validation_info
            
            return {
                **state,
                "processing_stage": "insights_validated"
            }
            
        except Exception as e:
            logger.error(f"Insights validation error: {e}")
            return {
                **state,
                "error_context": f"Insights validation failed: {str(e)}",
                "processing_stage": "error"
            }
    
    # Convenience methods for quick CEO setup
    def setup_for_startup_ceo(self, ceo_name: str):
        """Quick setup for startup CEO"""
        self.prompts.customize_for_startup_ceo(ceo_name)
        self.ceo_profile = self.prompts.ceo_profile
        logger.info(f"Configured analysis for startup CEO: {ceo_name}")
    
    def setup_for_enterprise_ceo(self, ceo_name: str):
        """Quick setup for enterprise CEO"""
        self.prompts.customize_for_enterprise_ceo(ceo_name)
        self.ceo_profile = self.prompts.ceo_profile
        logger.info(f"Configured analysis for enterprise CEO: {ceo_name}")
    
    def get_customization_status(self) -> dict:
        """Get current customization status for debugging"""
        return {
            "ceo_profile": self.ceo_profile,
            "custom_prompts": list(self.prompts.custom_prompts.keys()),
            "available_customizations": self.prompts.list_customizable_prompts(),
            "profile_summary": self.prompts.get_profile_summary()
        }
    
    def demonstrate_prompt_customization(self):
        """Show examples of how to customize prompts"""
        
        examples = {
            "leadership_custom_prompt": """
            As my leadership coach, I want you to focus specifically on:
            
            1. How well my managers are developing their direct reports
            2. Whether they're being decisive enough in tough situations  
            3. If they're maintaining team morale during this challenging quarter
            
            My leadership philosophy: I believe in servant leadership and want managers who coach their teams to excellence.
            
            Communication to analyze:
            {messages}
            
            Give me specific feedback on each manager and actionable coaching suggestions.
            """,
            
            "alignment_custom_prompt": """
            As my strategic advisor, analyze whether my team is truly aligned on our Q4 priorities.
            
            Context: We're a fast-growing startup and I'm worried about execution drift.
            
            Focus on:
            - Are people clear on what "done" looks like?
            - Is anyone working on the wrong things?
            - How confident is the team in our strategy?
            
            Communication:
            {messages}
            
            Be direct - I need to know if we're off track.
            """
        }
        
        logger.info("Prompt customization examples:")
        for prompt_type, example in examples.items():
            logger.info(f"\n{prompt_type}:\n{example}")
        
        return examples