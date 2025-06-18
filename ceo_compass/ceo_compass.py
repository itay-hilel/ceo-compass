import logging
import uuid
from typing import Dict, Any, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from openai import OpenAI
from .state import OrganizationalState, CEOConfig, CEOInputState, CEOOutputState
from .nodes import CEOAnalysisNodes  # Using enhanced version
from .utils import generate_ceo_summary

logger = logging.getLogger(__name__)

class CEOCompass:
    """Enhanced AI-powered organizational communication intelligence for CEOs"""
    
    def __init__(self, openai_api_key: str, enable_checkpointing: bool = True, ceo_profile: Optional[Dict[str, Any]] = None):
        """Initialize with optional CEO customization profile"""
        self.client = OpenAI(api_key=openai_api_key)
        
        # Initialize with CEO-specific customization
        self.ceo_profile = ceo_profile or self._get_default_ceo_profile()
        self.nodes = CEOAnalysisNodes(self.client, self.ceo_profile)
        
        self.checkpointer = MemorySaver() if enable_checkpointing else None
        self.workflow = None
        self._build_organizational_workflow()
        
        logger.info(f"CEO Compass initialized for: {self.ceo_profile.get('name', 'Unknown CEO')}")
    
    def _get_default_ceo_profile(self) -> Dict[str, Any]:
        """Default CEO profile that can be customized"""
        return {
            "name": "CEO",
            "company_stage": "growth",
            "leadership_style": "collaborative",
            "communication_preferences": {
                "directness_level": 0.7,
                "detail_preference": "concise", 
                "focus_areas": ["execution", "team_health", "culture"]
            },
            "decision_style": "data_driven",
            "intervention_preference": "coaching"
        }
    
    def update_ceo_profile(self, profile_updates: Dict[str, Any]):
        """Update CEO profile and reconfigure analysis"""
        self.ceo_profile.update(profile_updates)
        self.nodes.update_ceo_profile(self.ceo_profile)
        logger.info(f"Updated CEO profile: {profile_updates}")
    
    def set_custom_prompt(self, prompt_type: str, custom_prompt: str):
        """Allow CEO to set completely custom analysis prompts"""
        self.nodes.set_custom_prompt(prompt_type, custom_prompt)
        logger.info(f"Set custom prompt for: {prompt_type}")
    
    def _build_organizational_workflow(self):
        """Construct the organizational analysis workflow with modern LangGraph patterns"""
        # Initialize StateGraph with state schema
        workflow = StateGraph(OrganizationalState)
        
        # Add CEO-focused analysis nodes
        workflow.add_node("process_data", self.nodes.preprocess_organizational_data)
        workflow.add_node("analyze_leadership", self.nodes.analyze_leadership_effectiveness)
        workflow.add_node("analyze_alignment", self.nodes.analyze_organizational_alignment)
        workflow.add_node("synthesize_dashboard", self.nodes.synthesize_ceo_dashboard)
        workflow.add_node("validate_insights", self.nodes.validate_insights)
        
        # Create workflow with modern edge patterns
        workflow.add_edge(START, "process_data")
        workflow.add_edge("process_data", "analyze_leadership")
        workflow.add_edge("analyze_leadership", "analyze_alignment")
        workflow.add_edge("analyze_alignment", "synthesize_dashboard")
        workflow.add_conditional_edges(
            "synthesize_dashboard",
            self._route_validation,
            {
                "validate": "validate_insights",
                "complete": END
            }
        )
        workflow.add_edge("validate_insights", END)
        
        # Compile with checkpointing support
        self.workflow = workflow.compile(
            checkpointer=self.checkpointer
        )
    
    def _route_validation(self, state: OrganizationalState) -> str:
        """Determine if insights should be validated"""
        if state.get("processing_stage") == "error":
            return "complete"
        return "validate"
    
    def analyze_organization(
        self, 
        raw_communication: str, 
        communication_type: str = "auto",
        thread_id: Optional[str] = None,
        model_name: str = "gpt-4",
        max_retries: int = 3,
        enable_validation: bool = True,
        temperature: float = 0.3,
        ceo_profile_override: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze organizational communication with CEO customization support"""
        logger.info(f"Starting organizational analysis for CEO: {self.ceo_profile.get('name')}")
        
        # Use profile override if provided (useful for multi-tenant scenarios)
        effective_ceo_profile = ceo_profile_override or self.ceo_profile
        
        # Create configuration for the workflow
        config = {
            "configurable": {
                "thread_id": thread_id or str(uuid.uuid4()),
                "model_name": model_name,
                "max_retries": max_retries,
                "enable_validation": enable_validation,
                "temperature": temperature,
                "ceo_profile": effective_ceo_profile  # Pass CEO profile through config
            }
        }
        
        # Prepare input state according to modern schema
        input_state = {
            "raw_input": raw_communication,
            "communication_type": communication_type
        }
        
        # Initialize full state for internal processing
        initial_state = OrganizationalState(
            messages=[],
            raw_input=raw_communication,
            communication_type=communication_type,
            team_metadata={},
            leadership_analysis={},
            organizational_insights={},
            ceo_dashboard={},
            processing_stage="initialized",
            error_context=None
        )
        
        try:
            # Run the organizational analysis workflow with config
            final_state = self.workflow.invoke(initial_state, config=config)
            
            if final_state.get("processing_stage") == "error":
                return {
                    "error": final_state.get("error_context"),
                    "status": "analysis_failed",
                    "thread_id": config["configurable"]["thread_id"]
                }
            
            # Generate personalized executive summary
            personalized_summary = self._generate_personalized_summary(final_state, effective_ceo_profile)
            
            # Return results in expected output format with customization info
            return {
                "ceo_dashboard": final_state.get("ceo_dashboard", {}),
                "leadership_insights": final_state.get("leadership_analysis", {}),
                "organizational_insights": final_state.get("organizational_insights", {}),
                "team_metadata": final_state.get("team_metadata", {}),
                "status": "success",
                "executive_summary": personalized_summary,
                "thread_id": config["configurable"]["thread_id"],
                "customization_info": {
                    "analyzed_for": effective_ceo_profile.get('name'),
                    "leadership_style": effective_ceo_profile.get('leadership_style'),
                    "focus_areas": effective_ceo_profile.get('communication_preferences', {}).get('focus_areas', []),
                    "custom_prompts_used": list(self.nodes.prompts.custom_prompts.keys())
                }
            }
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return {
                "error": f"Workflow execution failed: {str(e)}",
                "status": "execution_failed",
                "thread_id": config["configurable"]["thread_id"]
            }
    
    def _generate_personalized_summary(self, state: Dict[str, Any], ceo_profile: Dict[str, Any]) -> str:
        """Generate executive summary personalized for this CEO"""
        
        dashboard = state.get("ceo_dashboard", {})
        executive_summary = dashboard.get("executive_summary", {})
        key_insights = dashboard.get("key_insights", {})
        recommendations = dashboard.get("actionable_recommendations", {})
        
        ceo_name = ceo_profile.get('name', 'CEO')
        leadership_style = ceo_profile.get('leadership_style', 'collaborative')
        intervention_style = ceo_profile.get('intervention_preference', 'coaching')
        
        team_health = executive_summary.get("overall_team_health", 0)
        leadership_impact = executive_summary.get("leadership_impact_score", 0)
        risk_level = executive_summary.get("organizational_risk_level", "unknown")
        
        # Customize summary based on CEO preferences
        if intervention_style == "directive":
            action_verb = "Actions Required"
        elif intervention_style == "coaching":
            action_verb = "Coaching Opportunities"
        else:
            action_verb = "Considerations"
        
        summary = f"""
{ceo_name.upper()}'S ORGANIZATIONAL INTELLIGENCE REPORT

EXECUTIVE OVERVIEW:
• Team Health Score: {team_health:.2f}/1.0
• Leadership Impact: {leadership_impact:.2f}/1.0  
• Risk Level: {risk_level.title()}
• Analysis Style: Customized for {leadership_style} leadership
• Communication Type: {state.get('communication_type', 'unknown').replace('_', ' ').title()}

KEY STRENGTHS:
{chr(10).join([f"• {strength}" for strength in key_insights.get('team_strengths', [])])}

AREAS REQUIRING ATTENTION:
{chr(10).join([f"• {concern}" for concern in key_insights.get('areas_of_concern', [])])}

{action_verb.upper()}:
{chr(10).join([f"• {action}" for action in recommendations.get('immediate_actions', [])])}

This analysis processed {len(state.get('messages', []))} communications from 
{state.get('team_metadata', {}).get('total_participants', 0)} team members using 
your personalized leadership analysis framework.
"""
        
        return summary.strip()
    
    def get_workflow_state(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """Get the current state of a workflow thread (requires checkpointing)"""
        if not self.checkpointer:
            logger.warning("Checkpointing not enabled. Cannot retrieve workflow state.")
            return None
        
        try:
            config = {"configurable": {"thread_id": thread_id}}
            state = self.workflow.get_state(config)
            return state.values if state else None
        except Exception as e:
            logger.error(f"Failed to retrieve workflow state: {e}")
            return None
    
    def resume_workflow(self, thread_id: str, additional_input: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Resume a workflow from checkpoint (requires checkpointing)"""
        if not self.checkpointer:
            raise ValueError("Checkpointing not enabled. Cannot resume workflow.")
        
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            if additional_input:
                result = self.workflow.invoke(additional_input, config=config)
            else:
                # Continue from last checkpoint
                state = self.workflow.get_state(config)
                if state:
                    result = self.workflow.invoke(None, config=config)
                else:
                    raise ValueError(f"No checkpoint found for thread_id: {thread_id}")
            
            return {
                "ceo_dashboard": result.get("ceo_dashboard", {}),
                "leadership_insights": result.get("leadership_analysis", {}),
                "organizational_insights": result.get("organizational_insights", {}),
                "team_metadata": result.get("team_metadata", {}),
                "status": "success",
                "executive_summary": self._generate_personalized_summary(result, self.ceo_profile),
                "thread_id": thread_id
            }
            
        except Exception as e:
            logger.error(f"Failed to resume workflow: {e}")
            return {
                "error": f"Failed to resume workflow: {str(e)}",
                "status": "resume_failed",
                "thread_id": thread_id
            }
    
    # Convenience methods for quick CEO setup
    def setup_for_startup_ceo(self, ceo_name: str, company_name: str = ""):
        """Quick configuration for a startup CEO"""
        startup_profile = {
            "name": ceo_name,
            "company_name": company_name,
            "company_stage": "startup",
            "leadership_style": "hands_on",
            "communication_preferences": {
                "directness_level": 0.8,
                "detail_preference": "concise",
                "focus_areas": ["execution", "team_health", "scaling"]
            },
            "decision_style": "data_driven", 
            "intervention_preference": "coaching"
        }
        
        self.update_ceo_profile(startup_profile)
        logger.info(f"Configured for startup CEO: {ceo_name}")
        
        return startup_profile
    
    def setup_for_enterprise_ceo(self, ceo_name: str, company_name: str = ""):
        """Quick configuration for an enterprise CEO"""
        enterprise_profile = {
            "name": ceo_name,
            "company_name": company_name,
            "company_stage": "mature",
            "leadership_style": "strategic",
            "communication_preferences": {
                "directness_level": 0.6,
                "detail_preference": "comprehensive",
                "focus_areas": ["culture", "innovation", "alignment"]
            },
            "decision_style": "consensus",
            "intervention_preference": "directive"
        }
        
        self.update_ceo_profile(enterprise_profile)
        logger.info(f"Configured for enterprise CEO: {ceo_name}")
        
        return enterprise_profile
    
    def get_customization_summary(self) -> Dict[str, Any]:
        """Get current customization status"""
        return {
            "ceo_profile": self.ceo_profile,
            "custom_prompts": list(self.nodes.prompts.custom_prompts.keys()),
            "available_customizations": self.nodes.prompts.list_customizable_prompts(),
            "nodes_status": self.nodes.get_customization_status()
        }
    
    def demonstrate_customization(self) -> Dict[str, Any]:
        """Show examples of customization options"""
        
        print(f"\n🎯 CEO COMPASS CUSTOMIZATION OPTIONS")
        print(f"Current CEO: {self.ceo_profile.get('name')}")
        print(f"Leadership Style: {self.ceo_profile.get('leadership_style')}")
        print("=" * 60)
        
        print("\n1. PROFILE CUSTOMIZATION:")
        print("   compass.update_ceo_profile({")
        print("       'name': 'Sarah Chen',")
        print("       'leadership_style': 'coaching',")
        print("       'focus_areas': ['team_development', 'innovation']")
        print("   })")
        
        print("\n2. CUSTOM PROMPTS:")
        print("   compass.set_custom_prompt('leadership_effectiveness', '''")
        print("   As Sarah's leadership coach, focus on:")
        print("   - How well managers are developing their teams")
        print("   - Decision-making speed and quality")
        print("   - Communication clarity under pressure")
        print("   ''')")
        
        print("\n3. QUICK SETUPS:")
        print("   compass.setup_for_startup_ceo('John Doe', 'TechCorp')")
        print("   compass.setup_for_enterprise_ceo('Jane Smith', 'BigCorp')")
        
        examples = self.nodes.demonstrate_prompt_customization()
        
        return {
            "current_profile": self.ceo_profile,
            "customization_examples": examples,
            "setup_methods": ["setup_for_startup_ceo", "setup_for_enterprise_ceo"],
            "custom_prompt_types": self.nodes.prompts.list_customizable_prompts()
        }

# Factory functions for common CEO types
def create_startup_ceo_compass(openai_api_key: str, ceo_name: str, company_name: str = "") -> CEOCompass:
    """Factory function to create a pre-configured startup CEO compass"""
    startup_profile = {
        "name": ceo_name,
        "company_name": company_name,
        "company_stage": "startup",
        "leadership_style": "hands_on",
        "communication_preferences": {
            "directness_level": 0.8,
            "detail_preference": "concise",
            "focus_areas": ["execution", "team_health", "scaling"]
        },
        "decision_style": "data_driven",
        "intervention_preference": "coaching"
    }
    
    return CEOCompass(openai_api_key, ceo_profile=startup_profile)

def create_enterprise_ceo_compass(openai_api_key: str, ceo_name: str, company_name: str = "") -> CEOCompass:
    """Factory function to create a pre-configured enterprise CEO compass"""
    enterprise_profile = {
        "name": ceo_name,
        "company_name": company_name,
        "company_stage": "mature",
        "leadership_style": "strategic",
        "communication_preferences": {
            "directness_level": 0.6,
            "detail_preference": "comprehensive",
            "focus_areas": ["culture", "innovation", "alignment"]
        },
        "decision_style": "consensus",
        "intervention_preference": "directive"
    }
    
    return CEOCompass(openai_api_key, ceo_profile=enterprise_profile)