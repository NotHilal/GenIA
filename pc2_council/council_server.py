"""
PC2 Council Server - Runs on PC2
This server hosts multiple LLMs that form the council.
Each LLM answers queries independently and reviews other LLMs' responses.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random
from typing import List, Dict

app = Flask(__name__)
CORS(app)

# Configuration - Edit these values
OLLAMA_URL = "http://localhost:11434"  # Ollama API endpoint
PORT = 5001  # Port for this server

# Council Models - Add or remove models as needed
# Make sure these models are pulled via: ollama pull <model-name>
COUNCIL_MODELS = [
    "llama3.2:3b",
    "mistral:7b",
    "phi3:mini"
]

def call_ollama(model: str, prompt: str) -> str:
    """
    Call Ollama API to get a response from a specific model.

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
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error calling {model}: {str(e)}"

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify server is running."""
    return jsonify({
        "status": "healthy",
        "models": COUNCIL_MODELS,
        "ollama_url": OLLAMA_URL
    })

@app.route('/models', methods=['GET'])
def get_models():
    """Return list of available council models."""
    return jsonify({
        "models": COUNCIL_MODELS
    })

@app.route('/answer', methods=['POST'])
def generate_answers():
    """
    Stage 1: Generate independent answers from all council models.

    Request body:
        {
            "query": "What is the capital of France?"
        }

    Response:
        {
            "answers": [
                {"model": "llama3.2:3b", "response": "..."},
                {"model": "mistral:7b", "response": "..."},
                ...
            ]
        }
    """
    data = request.get_json()
    query = data.get('query', '')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    print(f"\n{'='*60}")
    print(f"STAGE 1: Generating answers for query: {query}")
    print(f"{'='*60}\n")

    answers = []

    for model in COUNCIL_MODELS:
        print(f"Requesting answer from {model}...")

        prompt = f"""You are participating in an LLM council. Answer the following query clearly and concisely.

Query: {query}

Provide your answer:"""

        response = call_ollama(model, prompt)

        answers.append({
            "model": model,
            "response": response
        })

        print(f"  ✓ {model} responded ({len(response)} chars)\n")

    print(f"Stage 1 complete: {len(answers)} answers generated\n")

    return jsonify({"answers": answers})

@app.route('/review', methods=['POST'])
def review_answers():
    """
    Stage 2: Each model reviews and ranks other models' answers.

    Request body:
        {
            "query": "What is the capital of France?",
            "answers": [
                {"model": "llama3.2:3b", "response": "..."},
                {"model": "mistral:7b", "response": "..."},
                ...
            ]
        }

    Response:
        {
            "reviews": [
                {
                    "reviewer": "llama3.2:3b",
                    "rankings": [
                        {"answer_id": 1, "rank": 1, "reasoning": "..."},
                        {"answer_id": 2, "rank": 2, "reasoning": "..."},
                        ...
                    ]
                },
                ...
            ]
        }
    """
    data = request.get_json()
    query = data.get('query', '')
    answers = data.get('answers', [])

    if not query or not answers:
        return jsonify({"error": "Query and answers are required"}), 400

    print(f"\n{'='*60}")
    print(f"STAGE 2: Reviewing answers")
    print(f"{'='*60}\n")

    reviews = []

    for model in COUNCIL_MODELS:
        print(f"Model {model} reviewing answers...")

        # Create anonymized list of answers (excluding the reviewer's own answer)
        anonymized_answers = []
        for idx, ans in enumerate(answers):
            if ans['model'] != model:
                anonymized_answers.append({
                    "id": idx,
                    "response": ans['response']
                })

        # Shuffle to remove any ordering bias
        random.shuffle(anonymized_answers)

        # Build review prompt
        answers_text = "\n\n".join([
            f"Answer {i+1}:\n{ans['response']}"
            for i, ans in enumerate(anonymized_answers)
        ])

        prompt = f"""You are reviewing answers from other LLMs. Your task is to rank them based on accuracy, clarity, and insight.

Original Query: {query}

Here are the answers to review:

{answers_text}

Rank these answers from best (1) to worst ({len(anonymized_answers)}). For each answer, provide:
1. The answer number
2. Your rank for it (1 = best)
3. Brief reasoning (1-2 sentences)

Format your response as:
Answer X: Rank Y - Reasoning here
Answer X: Rank Y - Reasoning here
...

Provide your rankings:"""

        review_response = call_ollama(model, prompt)

        # Parse the review (simple parsing - in production you'd want more robust parsing)
        rankings = []
        for idx, ans in enumerate(anonymized_answers):
            rankings.append({
                "answer_id": ans['id'],
                "rank": idx + 1,  # Simple sequential ranking
                "reasoning": "See full review"
            })

        reviews.append({
            "reviewer": model,
            "review_text": review_response,
            "rankings": rankings
        })

        print(f"  ✓ {model} completed review\n")

    print(f"Stage 2 complete: {len(reviews)} reviews generated\n")

    return jsonify({"reviews": reviews})

@app.route('/test', methods=['GET'])
def test_models():
    """
    Test endpoint to verify all models are accessible via Ollama.
    """
    results = []

    for model in COUNCIL_MODELS:
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": "Say hello",
                    "stream": False
                },
                timeout=30
            )

            if response.status_code == 200:
                results.append({
                    "model": model,
                    "status": "OK",
                    "response": response.json()["response"][:100]
                })
            else:
                results.append({
                    "model": model,
                    "status": "ERROR",
                    "error": f"HTTP {response.status_code}"
                })
        except Exception as e:
            results.append({
                "model": model,
                "status": "ERROR",
                "error": str(e)
            })

    return jsonify({"test_results": results})

if __name__ == '__main__':
    print(f"""
    ╔════════════════════════════════════════════╗
    ║   PC2 COUNCIL SERVER                       ║
    ║   Running on port {PORT}                   ║
    ╚════════════════════════════════════════════╝

    Council Models: {', '.join(COUNCIL_MODELS)}
    Ollama URL: {OLLAMA_URL}

    Endpoints:
      GET  /health  - Health check
      GET  /models  - List models
      GET  /test    - Test all models
      POST /answer  - Generate answers (Stage 1)
      POST /review  - Review answers (Stage 2)

    Make sure Ollama is running and models are pulled!
    """)

    app.run(host='0.0.0.0', port=PORT, debug=True)
