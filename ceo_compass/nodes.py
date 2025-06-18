import json
import logging
import re
from datetime import datetime
from openai import OpenAI
from .state import OrganizationalState
from .parsers import OrganizationalParser
from .prompts import CEOPromptTemplates
from .utils import validate_ceo_dashboard_schema

logger = logging.getLogger(__name__)

class CEOAnalysisNodes:
    """LangGraph workflow nodes for CEO organizational insights"""
    
    def __init__(self, openai_client: OpenAI):
        self.client = openai_client
        self.parser = OrganizationalParser()
        self.prompts = CEOPromptTemplates()
    
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
    
    def preprocess_organizational_data(self, state: OrganizationalState) -> OrganizationalState:
        """Parse and structure organizational communication data"""
        logger.info("Processing organizational communication data...")
        
        try:
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
    
    def analyze_leadership_effectiveness(self, state: OrganizationalState) -> OrganizationalState:
        """Analyze leadership communication patterns and effectiveness"""
        logger.info("Analyzing leadership effectiveness...")
        
        try:
            messages = state.get("messages", [])
            team_metadata = state.get("team_metadata", {})
            
            leadership_prompt = self.prompts.leadership_effectiveness_prompt(messages, team_metadata)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior organizational consultant specializing in leadership effectiveness analysis for CEOs."},
                    {"role": "user", "content": leadership_prompt}
                ],
                temperature=0.3
            )
            
            leadership_data = self._safe_json_parse(response.choices[0].message.content)
            
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
    
    def analyze_organizational_alignment(self, state: OrganizationalState) -> OrganizationalState:
        """Analyze organizational alignment and cultural indicators"""
        logger.info("Analyzing organizational alignment...")
        
        try:
            messages = state.get("messages", [])
            team_metadata = state.get("team_metadata", {})
            
            alignment_prompt = self.prompts.organizational_alignment_prompt(messages, team_metadata)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a strategic advisor helping CEOs understand organizational health and culture."},
                    {"role": "user", "content": alignment_prompt}
                ],
                temperature=0.3
            )
            
            alignment_data = self._safe_json_parse(response.choices[0].message.content)
            
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
    
    def synthesize_ceo_dashboard(self, state: OrganizationalState) -> OrganizationalState:
        """Create CEO-focused dashboard with actionable insights"""
        logger.info("Synthesizing CEO dashboard...")
        
        try:
            leadership_analysis = state.get("leadership_analysis", {})
            organizational_insights = state.get("organizational_insights", {})
            team_metadata = state.get("team_metadata", {})
            messages = state.get("messages", [])
            
            synthesis_prompt = self.prompts.team_performance_synthesis_prompt(
                leadership_analysis, organizational_insights, team_metadata
            )
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are the CEO's chief of staff, synthesizing organizational insights into actionable strategic guidance."},
                    {"role": "user", "content": synthesis_prompt}
                ],
                temperature=0.2
            )
            
            ceo_dashboard = self._safe_json_parse(response.choices[0].message.content)
            
            # Add analysis metadata
            ceo_dashboard["analysis_metadata"] = {
                "analysis_timestamp": datetime.now().isoformat(),
                "communication_type": state.get("communication_type", "unknown"),
                "participants_analyzed": team_metadata.get("total_participants", 0),
                "messages_processed": len(messages),
                "leadership_participants": len([m for m in messages if m.get('is_leadership', False)]),
                "analysis_scope": "organizational_communication"
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
    
    def validate_insights(self, state: OrganizationalState) -> OrganizationalState:
        """Validate and finalize CEO insights"""
        logger.info("Validating CEO insights...")
        
        try:
            ceo_dashboard = state.get("ceo_dashboard", {})
            validate_ceo_dashboard_schema(ceo_dashboard)
            
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