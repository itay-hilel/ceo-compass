from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator

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