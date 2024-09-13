import pytest
import requests_mock
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test if the index page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Weather Assistant" in response.data 

def test_send_message(client):
    """Test sending a message to the bot and getting a response"""
    with requests_mock.Mocker() as mocker:
        mocker.post("https://shift3385-mikas2.hf.space/api/v1/prediction/56adc21d-f093-43f4-853b-3150e141c8c2", 
                    json={"text": "False response"})
        
        response = client.post('/send_message', data={'message': 'Hello, bot!'})
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['user_message'] == 'Hello, bot!'
        assert json_data['bot_response'] == 'False response'

def test_save_conversation(client):
    """Test saving a conversation"""
    conversation_data = "User: Hello\nBot: Hi!"
    
    response = client.post('/save_conversation', data={'conversation': conversation_data})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert 'conversation_id' in json_data
    global conversation_id
    conversation_id = json_data['conversation_id']

def test_get_conversation(client):
    """Test retrieving a saved conversation"""
    response = client.get(f'/get_conversation/{conversation_id}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'User: Hello' in json_data['conversation_content']

def test_get_nonexistent_conversation(client):
    """Test retrieving a conversation that does not exist"""
    response = client.get('/get_conversation/nonexistent')  
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['error'] == 'Conversation not found'

def test_delete_conversation(client):
    """Test deleting a conversation"""
    conversation_data = "User: Hello\nBot: Hi!"
    response = client.post('/save_conversation', data={'conversation': conversation_data})
    assert response.status_code == 200
    json_data = response.get_json()
    conversation_id = json_data['conversation_id']
    response = client.post('/delete_conversation', data={'conversation_id': conversation_id})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'

    response = client.get(f'/get_conversation/{conversation_id}')
    assert response.status_code == 404

def test_clear_history(client):
    """Test clearing all conversation history"""
    conversation_data = "User: Hello\nBot: Hi!"
    response = client.post('/save_conversation', data={'conversation': conversation_data})
    assert response.status_code == 200
    json_data = response.get_json()
    conversation_id = json_data['conversation_id']
    
    response = client.post('/clear_history')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'

    response = client.get(f'/get_conversation/{conversation_id}')
    assert response.status_code == 404
