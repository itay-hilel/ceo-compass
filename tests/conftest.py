import pytest
import os
from unittest.mock import Mock

@pytest.fixture
def mock_openai_api_key():
    """Provide mock OpenAI API key for testing"""
    return "test-api-key-12345"

@pytest.fixture
def sample_team_meeting_data():
    """Sample team meeting data for testing"""
    return """
Sarah (Engineering Manager): Good morning team! Let's dive into sprint planning.
Alex (Senior Dev): Morning Sarah! I've reviewed the backlog and I think we can tackle the payment integration.
Jordan (Product Manager): That aligns perfectly with our Q3 goals.
Mike (Junior Dev): I'd love to take on the frontend components.
Sarah: Great initiative Mike! Alex, can you pair with Mike on the complex parts?
Alex: Absolutely! I think we can break it into smaller chunks.
"""

@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing"""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = '{"test": "response"}'
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client