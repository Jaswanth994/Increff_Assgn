import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

NOVITA_API_KEY = os.getenv("NOVITA_API_KEY")
API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"

headers = {
    "Authorization": f"Bearer {NOVITA_API_KEY}",
    "Content-Type": "application/json"
}

# Load knowledge base
with open('knowledge_base.json', 'r') as f:
    KNOWLEDGE_BASE = json.load(f)

# System prompt with instructions
SYSTEM_PROMPT = f"""You are a customer support assistant for an electronics store. 
Use this knowledge to answer questions:
{json.dumps(KNOWLEDGE_BASE, indent=2)}

Follow these rules:
1. Be polite and professional
2. Answer based on the knowledge provided
3. If you don't know the answer, say "I don't have that information"
4. Keep responses concise
"""

def ask_chatbot(user_input):
    payload = {
        "model": "deepseek/deepseek-prover-v2-671b",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 200,
        "stream": False
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Connection error: {str(e)}"