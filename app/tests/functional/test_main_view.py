import os
import pytest

from ... import create_app
from ...util.extensions import db
from ...models.model import User
from ...util.config import TestConfig

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestConfig)
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
 
    yield testing_client
 
    ctx.pop()
    
@pytest.fixture(scope='module')
def init_database():
    db.create_all()
    user1 = User('Gary@proivder.tld','Gary', 'SuperStrongPassword123',  'CHMU', 'Building', 'Room')
    user2 = User('Rene@proivder.tld','Rene', 'SuperStrongPassword321',  'CHMU', 'Building', 'Room')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    yield db
 
    db.drop_all()
    
def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Blocktopus Dashboard" in response.data
    assert b"New Sketch" in response.data
    assert b"Standard Library" in response.data