from flask import Flask, render_template, request, jsonify
import requests
import re
import uuid 

def query_api(input_text):
    API_URL = "https://shift3385-mikas2.hf.space/api/v1/prediction/56adc21d-f093-43f4-853b-3150e141c8c2"
    headers = {"Authorization": "Bearer JUMR63un7aT-uRpSwJGqjHvMFt3rATdW8Dh9o92Pn5A"}
    
    payload = {
            "question": input_text,
        }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
    except:
         return "API Error"

def clean_text(input_str):
    input_cleaned = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', input_str)
    input_without_quotes = re.sub(r"['\"`]", '', input_cleaned)
    return input_without_quotes

app = Flask(__name__)

conversations = {}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    bot_response = query_api(clean_text(user_message))
    return jsonify({'user_message': user_message, 'bot_response': bot_response['text']})


@app.route('/save_conversation', methods=['POST'])
def save_conversation():
    conversation_content = request.form['conversation']
    conversation_id = str(uuid.uuid4()) 
    
    conversations[conversation_id] = conversation_content
    
    return jsonify({'status': 'success', 'conversation_id': conversation_id})


@app.route('/get_conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    if conversation_id in conversations:
        return jsonify({'conversation_content': conversations[conversation_id]})
    return jsonify({'error': 'Conversation not found'}), 404


@app.route('/delete_conversation', methods=['POST'])
def delete_conversation():
    conversation_id = request.form['conversation_id']
    if conversation_id in conversations:
        del conversations[conversation_id]
        return jsonify({'status': 'success'})
    return jsonify({'error': 'Conversation not found'}), 404


@app.route('/clear_history', methods=['POST'])
def clear_history():
    global conversations
    conversations = {}
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
