import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def generate_response(question, retrieved_chunks):
    """
    Generates a response using the Ollama API.
    """
    system_prompt = """
You are StudyBuddy, a strict study assistant.
You MUST answer ONLY using the content from the retrieved notes.
If the answer is not found in the notes, say: "I don’t know based on the notes."
Never hallucinate.
"""

    context = "\n".join(retrieved_chunks)
    prompt = f"System Prompt: {system_prompt}\n\nRetrieved Notes:\n{context}\n\nQuestion: {question}"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    start_time = time.time()
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()

        end_time = time.time()
        latency = end_time - start_time

        response_data = response.json()
        answer = response_data.get("response", "")
        tokens = response_data.get("eval_count", 0)

        return {
            "answer": answer.strip(),
            "latency": latency,
            "tokens": tokens
        }
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return None
