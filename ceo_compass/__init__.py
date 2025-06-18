from .ceo_compass import CEOCompass, create_startup_ceo_compass, create_enterprise_ceo_compass
from .state import OrganizationalState
from .test_scenarios import run_ceo_compass_test

__version__ = "1.0.0"
__title__ = "CEO Compass - Organizational Communication Intelligence"
__description__ = "AI-powered communication analysis for CEO organizational insights"
__all__ = [
    "CEOCompass", 
    "create_startup_ceo_compass", 
    "create_enterprise_ceo_compass",
    "OrganizationalState", 
    "run_ceo_compass_test"
]