from typing import Dict, Any

def validate_ceo_dashboard_schema(dashboard: Dict[str, Any]):
    """Validate CEO dashboard against expected schema"""
    required_sections = [
        "executive_summary", "key_insights", 
        "actionable_recommendations", "performance_metrics"
    ]
    
    for section in required_sections:
        if section not in dashboard:
            raise ValueError(f"Missing dashboard section: {section}")
    
    # Validate score ranges
    performance_metrics = dashboard.get("performance_metrics", {})
    for metric_name, metric_value in performance_metrics.items():
        if not (0.0 <= metric_value <= 1.0):
            raise ValueError(f"Performance metric {metric_name} out of range: {metric_value}")

def generate_ceo_summary(state) -> str:
    """Generate executive summary for CEO"""
    dashboard = state.get("ceo_dashboard", {})
    executive_summary = dashboard.get("executive_summary", {})
    key_insights = dashboard.get("key_insights", {})
    recommendations = dashboard.get("actionable_recommendations", {})
    
    team_health = executive_summary.get("overall_team_health", 0)
    leadership_impact = executive_summary.get("leadership_impact_score", 0)
    risk_level = executive_summary.get("organizational_risk_level", "unknown")
    
    summary = f"""
CEO ORGANIZATIONAL INTELLIGENCE REPORT

EXECUTIVE OVERVIEW:
• Team Health Score: {team_health:.2f}/1.0
• Leadership Impact: {leadership_impact:.2f}/1.0  
• Risk Level: {risk_level.title()}
• Communication Type: {state.get('communication_type', 'unknown').replace('_', ' ').title()}

KEY STRENGTHS:
{chr(10).join([f"• {strength}" for strength in key_insights.get('team_strengths', [])])}

AREAS OF FOCUS:
{chr(10).join([f"• {concern}" for concern in key_insights.get('areas_of_concern', [])])}

IMMEDIATE ACTIONS:
{chr(10).join([f"• {action}" for action in recommendations.get('immediate_actions', [])])}

This analysis processed {len(state.get('messages', []))} communications from 
{state.get('team_metadata', {}).get('total_participants', 0)} team members to provide 
strategic insights into your organizational dynamics.
"""
    
    return summary.strip()