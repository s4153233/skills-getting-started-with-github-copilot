import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app

@pytest.fixture
def client():
    """Create a TestClient for the FastAPI app"""
    return TestClient(app)

@pytest.fixture
def sample_email():
    """Sample email for testing"""
    return "test_student@mergington.edu"

@pytest.fixture
def sample_activity():
    """Sample activity name for testing"""
    return "Chess Club"
