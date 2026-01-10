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
from concurrent.futures import ThreadPoolExecutor, as_completed

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
                "stream": False,
                "options": {
                    "temperature": 0.7,      # Lower = faster, more focused
                    "num_predict": 150,      # Limit response length
                    "top_k": 40,             # Reduce sampling space
                    "top_p": 0.9             # Nucleus sampling
                }
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

    def generate_single_answer(model):
        """Generate answer from a single model"""
        print(f"Requesting answer from {model}...")

        prompt = f"""You are participating in an LLM council. Answer the following query briefly and concisely.

Query: {query}

Provide your answer (be brief):"""

        response = call_ollama(model, prompt)

        print(f"  ✓ {model} responded ({len(response)} chars)\n")

        return {
            "model": model,
            "response": response
        }

    # Run all models in parallel
    answers = []
    with ThreadPoolExecutor(max_workers=len(COUNCIL_MODELS)) as executor:
        # Submit all tasks
        future_to_model = {executor.submit(generate_single_answer, model): model for model in COUNCIL_MODELS}

        # Collect results as they complete
        for future in as_completed(future_to_model):
            try:
                answer = future.result()
                answers.append(answer)
            except Exception as e:
                model = future_to_model[future]
                print(f"  ✗ {model} failed: {str(e)}\n")

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

    def generate_single_review(model):
        """Generate review from a single model"""
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

        prompt = f"""You are reviewing answers from other LLMs. Rank them briefly based on accuracy and clarity.

Original Query: {query}

Answers to review:

{answers_text}

Rank from best (1) to worst ({len(anonymized_answers)}). Be brief.

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

        print(f"  ✓ {model} completed review\n")

        return {
            "reviewer": model,
            "review_text": review_response,
            "rankings": rankings
        }

    # Run all reviews in parallel
    reviews = []
    with ThreadPoolExecutor(max_workers=len(COUNCIL_MODELS)) as executor:
        # Submit all review tasks
        future_to_model = {executor.submit(generate_single_review, model): model for model in COUNCIL_MODELS}

        # Collect results as they complete
        for future in as_completed(future_to_model):
            try:
                review = future.result()
                reviews.append(review)
            except Exception as e:
                model = future_to_model[future]
                print(f"  ✗ {model} review failed: {str(e)}\n")

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
