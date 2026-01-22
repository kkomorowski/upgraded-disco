import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """Sample activities data for testing"""
    return {
        "Soccer Team": {
            "description": "Join the soccer team and participate in matches and tournaments",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 22,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice basketball skills and compete in games",
            "schedule": "Mondays and Wednesdays, 5:00 PM - 7:00 PM",
            "max_participants": 15,
            "participants": ["ava@mergington.edu", "mia@mergington.edu"]
        }
    }