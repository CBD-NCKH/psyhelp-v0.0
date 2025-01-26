from flask import Flask, request, jsonify, send_from_directory
import openai
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="", template_folder="../frontend")

# Đặt OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Route để hiển thị giao diện (frontend)
@app.route('/')
def serve_index():
    return send_from_directory(app.template_folder, "index.html")

# API Chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'Message is required'}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        return jsonify({'response': response['choices'][0]['message']['content']})
    except openai.error.OpenAIError as e:
        return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
