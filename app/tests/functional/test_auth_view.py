import os
import pytest

from . import test_client
    
def test_register_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/register' page is requested
    THEN check the response is valid
    """
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b"Sign up" in response.data
    assert b"Register" in response.data
    
def test_login_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Remember Me" in response.data
    assert b"Need an account?" in response.data