from flask import Flask, render_template, request, jsonify
from chatbot_groq import ExpertSoftChatbotRAG

app = Flask(__name__)
chatbot = ExpertSoftChatbotRAG("expert_soft_chatbot_dataset.json")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.json
    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"error": "No input provided."}), 400

    try:
        reply = chatbot.chat(user_input)
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("3000"),debug=True)
