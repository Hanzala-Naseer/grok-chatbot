import json
import faiss
import os
import requests
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

class ExpertSoftChatbotRAG:
    def __init__(self, dataset_path, model_name='all-MiniLM-L6-v2'):
        print(f"Loading model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dataset_path = dataset_path
        self.data = self._load_data()
        self.examples, self.intent_map = self._prepare_examples_intents()
        self.index, self.embeddings = self._build_faiss_index()

    def _load_data(self):
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _prepare_examples_intents(self):
        examples = []
        intent_map = []
        for item in self.data:
            intent = item.get("intent", "")
            for ex in item.get("examples", []):  # Safe access
                examples.append(ex.strip())
                intent_map.append(intent)
        return examples, intent_map

    def _build_faiss_index(self):
        print("Building FAISS index...")
        embeddings = self.model.encode(self.examples, convert_to_numpy=True)
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        return index, embeddings

    def search_top_intents(self, query, k=5, threshold=0.5):
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, k)
        matched_intents = set()

        for i, score in zip(indices[0], distances[0]):
            if score < threshold:
                matched_intents.add(self.intent_map[i])

        return list(matched_intents)

    def ask_groq(self, query, context, model="llama3-8b-8192"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY in environment")

        needs_detail = any(word in query.lower() for word in ["explain", "detail", "describe", "how", "why"])

        prompt = f"""
You are a helpful and professional assistant for Expert Soft Solution.

Use the context provided below to answer the user's question. Your responses should be **complete**, slightly elaborated, and helpful — typically 2 to 4 sentences. Do not be overly brief. Avoid generic language. Do **not** mention that you're an AI.

If the user asks for more detail or explanation, you may expand further.

Context:
{context}

User Question:
{query}

Your Response:"""

        if needs_detail:
            prompt += "\nThe user wants more explanation. Give a more detailed response."

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You must only answer based on the provided context. If nothing is relevant, respond with: 'Sorry, I couldn't find any relevant information.'"
                },
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()

    def chat(self, user_input, top_k=5, threshold=0.5):
        top_intents = self.search_top_intents(user_input, k=top_k, threshold=threshold)
        if not top_intents:
            return "Sorry, I couldn't find any relevant information."

        # Build context from intent-response pairs
        context_parts = []
        for item in self.data:
            if item["intent"] in top_intents:
                context_parts.append(f"Intent: {item['intent']}\nResponse: {item['response']}")

        context = "\n\n".join(context_parts)
        return self.ask_groq(user_input, context)

# CLI runner
if __name__ == "__main__":
    chatbot = ExpertSoftChatbotRAG("expert_soft_chatbot_dataset.json")

    print("\n=== Expert Soft Chatbot (LLM + FAISS Intent Context) ===")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ("exit", "quit"):
            print("👋 Exiting...")
            break
        try:
            answer = chatbot.chat(user_input)
            print(f"Bot: {answer}")
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Bot: Something went wrong while generating the response.")
