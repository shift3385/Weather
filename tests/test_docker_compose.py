import requests
import time

FLASK_LOCAL_URL = "http://flaskapp:5000"
NGROK_API_URL = "http://ngrok:4040/api/tunnels"

# Helper function to wait until the Flask app or ngrok is ready
def wait_for_service(url, timeout=30):
    """Wait for the Flask app or ngrok to be ready."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            time.sleep(2)
    return False

# Test to ensure the Flask app is running on localhost
def test_flask_app_is_up():
    """Test if the Flask app is accessible."""
    assert wait_for_service(FLASK_LOCAL_URL), "Flask app is not running!"

    response = requests.get(f"{FLASK_LOCAL_URL}/")
    assert response.status_code == 200, "Failed to reach the Flask home page."
    
    assert b"<title>Weather Assistant</title>" in response.content, "Expected title not found in the Flask app response."
    assert b"<div class=\"chat-container\">" in response.content, "Expected container not found in the Flask app response."


# Test to ensure ngrok is running and tunneling the Flask app
def test_ngrok_tunnel_is_up():
    """Test if ngrok is tunneling the Flask app correctly."""
    assert wait_for_service(NGROK_API_URL), "ngrok is not running!"
    
    time.sleep(5) 
    
    response = requests.get(NGROK_API_URL)
    assert response.status_code == 200, "Failed to reach ngrok API."

    tunnels = response.json().get("tunnels", [])
    assert len(tunnels) > 0, "No tunnels found."

    public_url = tunnels[0]["public_url"]
    assert wait_for_service(public_url), "Flask app not accessible via ngrok!"