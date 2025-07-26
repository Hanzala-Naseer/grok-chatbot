🧠 ChatBotWeb – AI Chatbot for Expert Soft
📌 Overview
ChatBotWeb is a lightweight AI chatbot built with Python and Flask. It uses a locally defined dataset (expert_soft_chatbot_dataset.json) to respond intelligently to user queries using NLP techniques. Designed as a prototype for software houses like Expert Soft, it's modular, fast, and easy to customize.

🚀 Features
Intent-based NLP chatbot

Contextual response logic using sentence embeddings

Flask-powered web interface

Easy to extend with more intents and responses

JSON-based dataset for flexibility

📁 Project Structure
bash
Copy
Edit
ChatBotWeb/
├── app.py # Flask app
├── chatbot_groq.py # Chat logic (intent matching)
├── expert_soft_chatbot_dataset.json # Dataset of intents
├── requirements.txt # Required Python libraries
├── .env # Environment variables
├── README.md # Project documentation
⚙️ Installation & Setup
bash
Copy
Edit
git clone https://github.com/Hanzala-Naseer/grok-chatbot
cd ChatBotWeb

# Create and activate virtual environment (optional)

python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate

# Install dependencies

pip install -r requirements.txt

# Run the Flask app

python app.py
Open your browser and go to: http://localhost:5000

🧩 How It Works
Receives user input from the front-end

Uses sentence transformer embeddings to compare input with training patterns

Matches the best intent and returns a response

Returns fallback message if no match is found

📊 Sample Intent (from JSON)
json
Copy
Edit
{
"tag": "greeting",
"patterns": ["hello", "hi", "good morning"],
"responses": ["Hello! How can I assist you today?", "Hi there!"]
}
🛠 Tech Stack
Python 3.x

Flask

Sentence Transformers

Scikit-learn

JSON for dataset

🧪 Future Improvements
GUI-based chatbot frontend

Chat history and context memory

Live database or API integration

Deployment on Render, Vercel, or Docker

👤 Author
Developed by Hanzala Naseer

📧 hanzalanaseer56@gmail.com
