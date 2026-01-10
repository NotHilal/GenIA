"""
PC1 Chairman Server - Runs on PC1
This server hosts the Chairman LLM that synthesizes the final answer.
The Chairman receives all council answers and reviews, then creates a final response.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from typing import List, Dict

app = Flask(__name__)
CORS(app)

# Configuration - Edit these values
OLLAMA_URL = "http://localhost:11434"  # Ollama API endpoint
PORT = 5002  # Port for this server

# Chairman Model - Make sure this model is pulled via: ollama pull <model-name>
CHAIRMAN_MODEL = "llama3.2:3b"

def call_ollama(model: str, prompt: str) -> str:
    """
    Call Ollama API to get a response from the Chairman model.

    Args:
        model: Name of the Ollama model
        prompt: The prompt to send to the model

    Returns:
        The model's response as a string
    """
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,      # Lower = faster, more focused
                    "num_predict": 200,      # Limit response length (Chairman gets more)
                    "top_k": 40,             # Reduce sampling space
                    "top_p": 0.9             # Nucleus sampling
                }
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error calling Chairman model: {str(e)}"

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify server is running."""
    return jsonify({
        "status": "healthy",
        "model": CHAIRMAN_MODEL,
        "ollama_url": OLLAMA_URL
    })

@app.route('/model', methods=['GET'])
def get_model():
    """Return the Chairman model being used."""
    return jsonify({
        "chairman_model": CHAIRMAN_MODEL
    })

@app.route('/synthesize', methods=['POST'])
def synthesize_final_answer():
    """
    Stage 3: Synthesize final answer from all council responses and reviews.

    Request body:
        {
            "query": "What is the capital of France?",
            "answers": [
                {"model": "llama3.2:3b", "response": "..."},
                {"model": "mistral:7b", "response": "..."},
                ...
            ],
            "reviews": [
                {
                    "reviewer": "llama3.2:3b",
                    "review_text": "...",
                    "rankings": [...]
                },
                ...
            ]
        }

    Response:
        {
            "final_answer": "The synthesized response from the Chairman",
            "chairman_model": "llama3.2:3b"
        }
    """
    data = request.get_json()
    query = data.get('query', '')
    answers = data.get('answers', [])
    reviews = data.get('reviews', [])

    if not query:
        return jsonify({"error": "No query provided"}), 400

    if not answers:
        return jsonify({"error": "No answers provided"}), 400

    print(f"\n{'='*60}")
    print(f"STAGE 3: Chairman synthesizing final answer")
    print(f"Query: {query}")
    print(f"Received {len(answers)} answers and {len(reviews)} reviews")
    print(f"{'='*60}\n")

    # Build the synthesis prompt
    answers_text = "\n\n".join([
        f"Model {ans['model']}:\n{ans['response']}"
        for ans in answers
    ])

    reviews_text = ""
    if reviews:
        reviews_text = "\n\n".join([
            f"Review by {rev['reviewer']}:\n{rev.get('review_text', 'No review text')}"
            for rev in reviews
        ])

    prompt = f"""You are the Chairman of an LLM Council. Multiple language models have answered a query, and some have reviewed each other's responses.

Your task is to synthesize a final, authoritative answer that:
1. Integrates the best insights from all responses
2. Considers the peer reviews and rankings
3. Provides a clear, accurate, and comprehensive answer
4. Acknowledges different perspectives where relevant

Original Query: {query}

Council Answers:
{answers_text}

"""

    if reviews_text:
        prompt += f"""
Peer Reviews:
{reviews_text}

"""

    prompt += """
Based on all the above information, provide your final synthesized answer. Be concise but thorough.

Final Answer:"""

    print("Generating synthesis from Chairman model...")

    final_answer = call_ollama(CHAIRMAN_MODEL, prompt)

    print(f"✓ Chairman synthesis complete ({len(final_answer)} chars)\n")

    return jsonify({
        "final_answer": final_answer,
        "chairman_model": CHAIRMAN_MODEL
    })

@app.route('/test', methods=['GET'])
def test_chairman():
    """
    Test endpoint to verify the Chairman model is accessible via Ollama.
    """
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": CHAIRMAN_MODEL,
                "prompt": "Say hello, I am the Chairman.",
                "stream": False
            },
            timeout=30
        )

        if response.status_code == 200:
            return jsonify({
                "status": "OK",
                "model": CHAIRMAN_MODEL,
                "response": response.json()["response"]
            })
        else:
            return jsonify({
                "status": "ERROR",
                "error": f"HTTP {response.status_code}"
            }), 500
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print(f"""
    ╔════════════════════════════════════════════╗
    ║   PC1 CHAIRMAN SERVER                      ║
    ║   Running on port {PORT}                   ║
    ╚════════════════════════════════════════════╝

    Chairman Model: {CHAIRMAN_MODEL}
    Ollama URL: {OLLAMA_URL}

    Endpoints:
      GET  /health      - Health check
      GET  /model       - Get Chairman model
      GET  /test        - Test Chairman model
      POST /synthesize  - Synthesize final answer (Stage 3)

    Make sure Ollama is running and the Chairman model is pulled!
    """)

    app.run(host='0.0.0.0', port=PORT, debug=True)
