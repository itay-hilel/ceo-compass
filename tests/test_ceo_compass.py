import pytest
import os
import uuid
from unittest.mock import patch, Mock
import json

# Set environment variable for testing
os.environ['OPENAI_API_KEY'] = 'test-key-12345'

from ceo_compass.test_scenarios import run_ceo_compass_test
from ceo_compass.parsers import OrganizationalParser
from ceo_compass.ceo_compass import CEOCompass

class TestOrganizationalParser:
    """Test the organizational communication parser"""
    
    def test_parse_team_meeting(self, sample_team_meeting_data):
        """Test parsing team meeting data"""
        messages = OrganizationalParser.parse_team_meeting(sample_team_meeting_data)
        
        assert len(messages) > 0
        assert all('speaker' in msg for msg in messages)
        assert all('content' in msg for msg in messages)
        assert any(msg.get('is_leadership', False) for msg in messages)
    
    def test_auto_detect_communication_type(self):
        """Test automatic communication type detection"""
        # Test email detection
        email_data = "From: ceo@company.com\nSubject: Test\nContent here"
        assert OrganizationalParser.auto_detect_communication_type(email_data) == "leadership_email"
        
        # Test all hands detection
        all_hands_data = "CEO: Welcome to our all hands meeting"
        assert OrganizationalParser.auto_detect_communication_type(all_hands_data) == "all_hands"
        
        # Test default to team meeting
        meeting_data = "John: Let's start the meeting"
        assert OrganizationalParser.auto_detect_communication_type(meeting_data) == "team_meeting"
    
    def test_extract_team_dynamics(self, sample_team_meeting_data):
        """Test team dynamics extraction"""
        messages = OrganizationalParser.parse_team_meeting(sample_team_meeting_data)
        dynamics = OrganizationalParser.extract_team_dynamics(messages)
        
        assert 'total_participants' in dynamics
        assert 'leadership_participation_rate' in dynamics
        assert 'speaker_statistics' in dynamics
        assert dynamics['total_participants'] > 0

class TestCEOCompass:
    """Test the main CEO Compass functionality with modern patterns"""
    
    @patch('ceo_compass.ceo_compass.OpenAI')
    def test_ceo_compass_initialization(self, mock_openai, mock_openai_api_key):
        """Test CEO Compass initialization with modern features"""
        compass = CEOCompass(openai_api_key=mock_openai_api_key, enable_checkpointing=True)
        assert compass.client is not None
        assert compass.workflow is not None
        assert compass.checkpointer is not None
    
    @patch('ceo_compass.ceo_compass.OpenAI')
    def test_ceo_compass_no_checkpointing(self, mock_openai, mock_openai_api_key):
        """Test CEO Compass initialization without checkpointing"""
        compass = CEOCompass(openai_api_key=mock_openai_api_key, enable_checkpointing=False)
        assert compass.client is not None
        assert compass.workflow is not None
        assert compass.checkpointer is None
    
    @patch('ceo_compass.ceo_compass.OpenAI')
    def test_analyze_organization_with_config(self, mock_openai, sample_team_meeting_data):
        """Test successful organization analysis with modern configuration"""
        # Mock OpenAI responses
        mock_client = Mock()
        mock_response = Mock()
        
        # Mock successful analysis responses
        success_responses = [
            '{"leadership_effectiveness": {"communication_clarity": 0.8}, "leadership_style_indicators": {}, "team_response_patterns": {}, "red_flags": [], "positive_leadership_moments": []}',
            '{"organizational_alignment": {"goal_clarity": 0.9}, "cultural_health_indicators": {}, "information_flow": {}, "early_warning_signals": [], "cultural_strengths": [], "recommended_interventions": []}',
            '{"executive_summary": {"overall_team_health": 0.85, "leadership_impact_score": 0.8, "organizational_risk_level": "low", "intervention_urgency": "none"}, "key_insights": {"team_strengths": ["Good collaboration"], "areas_of_concern": [], "leadership_opportunities": [], "cultural_evolution": "positive"}, "actionable_recommendations": {"immediate_actions": [], "30_day_focus_areas": [], "strategic_initiatives": []}, "performance_metrics": {"team_collaboration_index": 0.8, "innovation_capacity_score": 0.7, "execution_effectiveness": 0.85, "talent_retention_risk": 0.2}, "next_conversation_focus": [], "success_indicators_to_monitor": []}'
        ]
        
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = success_responses[0]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # Test with different response for each call
        def side_effect(*args, **kwargs):
            response = Mock()
            response.choices = [Mock()]
            if 'leadership effectiveness' in str(kwargs.get('messages', [])):
                response.choices[0].message.content = success_responses[0]
            elif 'organizational alignment' in str(kwargs.get('messages', [])):
                response.choices[0].message.content = success_responses[1]
            else:
                response.choices[0].message.content = success_responses[2]
            return response
        
        mock_client.chat.completions.create.side_effect = side_effect
        
        compass = CEOCompass(openai_api_key="test-key")
        
        # Test with modern configuration options
        result = compass.analyze_organization(
            raw_communication=sample_team_meeting_data,
            communication_type="team_meeting",
            thread_id="test-thread-123",
            model_name="gpt-4",
            max_retries=2,
            enable_validation=True,
            temperature=0.2
        )
        
        assert result['status'] == 'success'
        assert 'ceo_dashboard' in result
        assert 'executive_summary' in result
        assert 'thread_id' in result
        assert result['thread_id'] == "test-thread-123"
    
    @patch('ceo_compass.ceo_compass.OpenAI')
    def test_workflow_state_management(self, mock_openai, mock_openai_api_key):
        """Test workflow state management with checkpointing"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        compass = CEOCompass(openai_api_key=mock_openai_api_key, enable_checkpointing=True)
        
        # Test getting state (should return None for non-existent thread)
        state = compass.get_workflow_state("non-existent-thread")
        # Note: This might return None or empty state depending on implementation
        
        # Test with checkpointing disabled
        compass_no_checkpoint = CEOCompass(openai_api_key=mock_openai_api_key, enable_checkpointing=False)
        state = compass_no_checkpoint.get_workflow_state("any-thread")
        assert state is None
    
    @patch('ceo_compass.ceo_compass.OpenAI')
    def test_resume_workflow_error_handling(self, mock_openai, mock_openai_api_key):
        """Test resume workflow error handling"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Test with checkpointing disabled
        compass = CEOCompass(openai_api_key=mock_openai_api_key, enable_checkpointing=False)
        
        with pytest.raises(ValueError, match="Checkpointing not enabled"):
            compass.resume_workflow("any-thread")

class TestModernFeatures:
    """Test modern LangGraph features"""
    
    @patch('ceo_compass.nodes.OpenAI')
    def test_config_integration(self, mock_openai):
        """Test that configuration is properly passed through the workflow"""
        from ceo_compass.nodes import CEOAnalysisNodes
        from langchain_core.runnables import RunnableConfig
        
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        nodes = CEOAnalysisNodes(mock_client)
        
        # Test config extraction
        config = RunnableConfig(
            configurable={
                "model_name": "gpt-4-turbo",
                "temperature": 0.5,
                "max_retries": 5,
                "enable_validation": False
            }
        )
        
        model_config = nodes._get_model_config(config)
        assert model_config["model"] == "gpt-4-turbo"
        assert model_config["temperature"] == 0.5
        assert model_config["max_retries"] == 5
        
        # Test default config
        default_config = nodes._get_model_config(None)
        assert default_config["model"] == "gpt-4"
        assert default_config["temperature"] == 0.3
        assert default_config["max_retries"] == 3

class TestEndToEnd:
    """End-to-end testing with modern patterns"""
    
    @patch('ceo_compass.nodes.OpenAI')
    def test_run_ceo_compass_test_modern(self, mock_openai):
        """Test the main test function with modern LangGraph patterns"""
        # Mock successful OpenAI responses
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        
        # Create realistic mock responses
        mock_responses = {
            'leadership': '{"leadership_effectiveness": {"communication_clarity": 0.8, "team_engagement_fostered": 0.7, "decision_making_efficiency": 0.9, "psychological_safety_created": 0.8}, "leadership_style_indicators": {"directive_vs_collaborative": 0.3, "micromanaging_signals": 0.2, "empowerment_level": 0.8, "transparency_score": 0.9}, "team_response_patterns": {"openness_to_share": 0.8, "innovation_comfort": 0.7, "dissent_expression": 0.6, "engagement_energy": 0.9}, "red_flags": [], "positive_leadership_moments": ["Clear goal setting", "Encouraging mentorship"]}',
            
            'alignment': '{"organizational_alignment": {"goal_clarity": 0.9, "priority_consensus": 0.8, "role_clarity": 0.8, "strategic_understanding": 0.7}, "cultural_health_indicators": {"collaboration_quality": 0.9, "innovation_mindset": 0.8, "accountability_culture": 0.8, "learning_orientation": 0.9}, "information_flow": {"upward_transparency": 0.7, "lateral_coordination": 0.8, "decision_communication": 0.8}, "early_warning_signals": [], "cultural_strengths": ["Strong collaboration", "Learning mindset"], "recommended_interventions": []}',
            
            'dashboard': '{"executive_summary": {"overall_team_health": 0.85, "leadership_impact_score": 0.82, "organizational_risk_level": "low", "intervention_urgency": "none"}, "key_insights": {"team_strengths": ["Excellent collaboration", "Strong mentorship culture", "Clear communication"], "areas_of_concern": [], "leadership_opportunities": ["Continue fostering growth"], "cultural_evolution": "positive"}, "actionable_recommendations": {"immediate_actions": ["Maintain current momentum"], "30_day_focus_areas": ["Formalize mentorship programs"], "strategic_initiatives": ["Scale collaboration practices"]}, "performance_metrics": {"team_collaboration_index": 0.9, "innovation_capacity_score": 0.8, "execution_effectiveness": 0.85, "talent_retention_risk": 0.15}, "next_conversation_focus": ["Career development", "Technical growth"], "success_indicators_to_monitor": ["Team satisfaction", "Delivery velocity"]}'
        }
        
        def side_effect(*args, **kwargs):
            response = Mock()
            response.choices = [Mock()]
            
            messages = kwargs.get('messages', [])
            content = str(messages)
            
            if 'leadership effectiveness' in content.lower():
                response.choices[0].message.content = mock_responses['leadership']
            elif 'organizational alignment' in content.lower() or 'strategic advisor' in content.lower():
                response.choices[0].message.content = mock_responses['alignment']
            else:
                response.choices[0].message.content = mock_responses['dashboard']
            
            return response
        
        mock_client.chat.completions.create.side_effect = side_effect
        mock_openai.return_value = mock_client
        
        # Run the test with modern patterns
        result = run_ceo_compass_test()
        
        # The test should complete without throwing exceptions
        assert isinstance(result, bool)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])