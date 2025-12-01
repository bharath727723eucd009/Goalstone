"""Pytest configuration and shared fixtures."""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from ..main import app

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)

@pytest.fixture
def mock_database():
    """Mock database operations."""
    with patch('Backend.database.connection.get_database') as mock_db:
        mock_db.return_value = AsyncMock()
        yield mock_db

@pytest.fixture
def mock_session_manager():
    """Mock session manager."""
    with patch('Backend.sessions.session_manager.InMemorySessionManager') as mock_session:
        mock_instance = AsyncMock()
        mock_session.return_value = mock_instance
        yield mock_instance

@pytest.fixture(autouse=True)
def mock_logging():
    """Mock logging to reduce test output."""
    with patch('Backend.observability.logger.get_logger') as mock_logger:
        mock_logger.return_value = AsyncMock()
        yield mock_logger