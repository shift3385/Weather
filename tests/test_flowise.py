import requests

api_url = "https://shift3385-mikas2.hf.space/api/v1/prediction/56adc21d-f093-43f4-853b-3150e141c8c2"
tokenauth = "Bearer JUMR63un7aT-uRpSwJGqjHvMFt3rATdW8Dh9o92Pn5A"
headers = {"Authorization": f"Bearer {tokenauth}"}


def test_post_endpoint():
    
    payload = {
        "question": "hello",
    }

    response = requests.post(api_url, json=payload, headers=headers)


    assert response.status_code == 200

    data = response.json()

    assert data['question'] == 'hello'
    assert 'sessionId' in data  
