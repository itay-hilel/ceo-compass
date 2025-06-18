import logging
import uuid
from typing import Dict, Any, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from openai import OpenAI
from .state import OrganizationalState, CEOConfig, CEOInputState, CEOOutputState
from .nodes import CEOAnalysisNodes
from .utils import generate_ceo_summary

logger = logging.getLogger(__name__)

class CEOCompass:
    """AI-powered organizational communication intelligence for CEOs"""
    
    def __init__(self, openai_api_key: str, enable_checkpointing: bool = True):
        self.client = OpenAI(api_key=openai_api_key)
        self.nodes = CEOAnalysisNodes(self.client)
        self.checkpointer = MemorySaver() if enable_checkpointing else None
        self.workflow = None
        self._build_organizational_workflow()
    
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
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """Analyze organizational communication for CEO insights with modern config support"""
        logger.info(f"Starting organizational analysis for CEO: {communication_type}")
        
        # Create configuration for the workflow
        config = {
            "configurable": {
                "thread_id": thread_id or str(uuid.uuid4()),
                "model_name": model_name,
                "max_retries": max_retries,
                "enable_validation": enable_validation,
                "temperature": temperature
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
            
            # Return results in expected output format
            return {
                "ceo_dashboard": final_state.get("ceo_dashboard", {}),
                "leadership_insights": final_state.get("leadership_analysis", {}),
                "organizational_insights": final_state.get("organizational_insights", {}),
                "team_metadata": final_state.get("team_metadata", {}),
                "status": "success",
                "executive_summary": generate_ceo_summary(final_state),
                "thread_id": config["configurable"]["thread_id"]
            }
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return {
                "error": f"Workflow execution failed: {str(e)}",
                "status": "execution_failed",
                "thread_id": config["configurable"]["thread_id"]
            }
    
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
                "executive_summary": generate_ceo_summary(result),
                "thread_id": thread_id
            }
            
        except Exception as e:
            logger.error(f"Failed to resume workflow: {e}")
            return {
                "error": f"Failed to resume workflow: {str(e)}",
                "status": "resume_failed",
                "thread_id": thread_id
            }