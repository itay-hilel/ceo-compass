from typing import TypedDict, Annotated, List, Dict, Any, Optional, Literal
import operator

class CEOInputState(TypedDict):
    """Input schema for CEO Compass analysis"""
    raw_input: str
    communication_type: str  # "team_meeting", "leadership_email", "all_hands", "slack_channel", "auto"

class CEOOutputState(TypedDict):
    """Output schema for CEO Compass analysis"""
    ceo_dashboard: Dict[str, Any]
    leadership_insights: Dict[str, Any]
    organizational_insights: Dict[str, Any]
    team_metadata: Dict[str, Any]
    status: str
    executive_summary: str

class CEOConfig(TypedDict, total=False):
    """Configuration schema for CEO Compass workflow"""
    model_name: Literal["gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"]
    max_retries: int
    enable_validation: bool
    temperature: float

class OrganizationalState(TypedDict):
    """Core state for CEO organizational communication analysis"""
    messages: Annotated[List[Dict[str, Any]], operator.add]
    raw_input: str
    communication_type: str  # "team_meeting", "leadership_email", "all_hands", "slack_channel"
    team_metadata: Dict[str, Any]
    leadership_analysis: Dict[str, Any]
    organizational_insights: Dict[str, Any]
    ceo_dashboard: Dict[str, Any]
    processing_stage: str
    error_context: Optional[str]