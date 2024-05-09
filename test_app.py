import os
import tempfile
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Medical Chatbot' in response.data

def test_get_bot_response(client):
    response = client.get('/get?msg=OK')
    assert response.status_code == 200
    assert b'What is your name ?' in response.data

def test_session_management(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['name'] = 'John'
            sess['age'] = 30
            sess['gender'] = 'Male'
            sess['step'] = 'age'

        response = c.get('/get?msg=30')
        assert 'age' in c.session
        assert c.session['age'] == 30
        assert b'Can you specify your gender ?' in response.data

def test_get_bot_response_with_parameters(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['name'] = 'John'
            sess['age'] = 30
            sess['gender'] = 'Male'
            sess['step'] = 'Depart'

        response = c.get('/get?msg=S')
        assert response.status_code == 200
        assert b'Well, Hello again Mr/Ms John' in response.data
