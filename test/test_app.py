import pytest
import os 
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    """Test the hello world route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, Jenkins CI/CD World!, Testing Successful' in response.data

def test_health_check(client):
    """Test the health check route"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data == b'OK'