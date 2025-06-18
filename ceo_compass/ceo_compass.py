import logging
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from openai import OpenAI
from .state import OrganizationalState
from .nodes import CEOAnalysisNodes
from .utils import generate_ceo_summary

logger = logging.getLogger(__name__)

class CEOCompass:
    """AI-powered organizational communication intelligence for CEOs"""
    
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.nodes = CEOAnalysisNodes(self.client)
        self.workflow = None
        self._build_organizational_workflow()
    
    def _build_organizational_workflow(self):
        """Construct the organizational analysis workflow"""
        workflow = StateGraph(OrganizationalState)
        
        # Add CEO-focused analysis nodes
        workflow.add_node("process_data", self.nodes.preprocess_organizational_data)
        workflow.add_node("analyze_leadership", self.nodes.analyze_leadership_effectiveness)
        workflow.add_node("analyze_alignment", self.nodes.analyze_organizational_alignment)
        workflow.add_node("synthesize_dashboard", self.nodes.synthesize_ceo_dashboard)
        workflow.add_node("validate_insights", self.nodes.validate_insights)
        
        # Create linear workflow with conditional validation
        workflow.add_edge("process_data", "analyze_leadership")
        workflow.add_edge("analyze_leadership", "analyze_alignment")
        workflow.add_edge("analyze_alignment", "synthesize_dashboard")
        workflow.add_conditional_edges(
            "synthesize_dashboard",
            self._should_validate_insights,
            {
                "validate": "validate_insights",
                "complete": END
            }
        )
        workflow.add_edge("validate_insights", END)
        
        # Set entry point
        workflow.set_entry_point("process_data")
        
        self.workflow = workflow.compile()
    
    def _should_validate_insights(self, state: OrganizationalState) -> str:
        """Determine if insights should be validated"""
        if state.get("processing_stage") == "error":
            return "complete"
        return "validate"
    
    def analyze_organization(self, raw_communication: str, communication_type: str = "auto") -> Dict[str, Any]:
        """Analyze organizational communication for CEO insights"""
        logger.info(f"Starting organizational analysis for CEO: {communication_type}")
        
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
        
        # Run the organizational analysis workflow
        final_state = self.workflow.invoke(initial_state)
        
        if final_state.get("processing_stage") == "error":
            return {
                "error": final_state.get("error_context"),
                "status": "analysis_failed"
            }
        
        return {
            "ceo_dashboard": final_state.get("ceo_dashboard", {}),
            "leadership_insights": final_state.get("leadership_analysis", {}),
            "organizational_insights": final_state.get("organizational_insights", {}),
            "team_metadata": final_state.get("team_metadata", {}),
            "status": "success",
            "executive_summary": generate_ceo_summary(final_state)
        }