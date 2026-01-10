"""
Frontend Coordinator - Can run on either PC
This server coordinates the entire LLM Council workflow and serves the web UI.
It orchestrates communication between PC1 (Chairman) and PC2 (Council).
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

# Configuration - EDIT THESE TO MATCH YOUR SETUP
PC1_CHAIRMAN_URL = "http://172.20.10.9:5002"  # PC1 Chairman server (update with PC1's actual IP)
PC2_COUNCIL_URL = "http://localhost:5001"     # PC2 Council server (localhost if frontend is on PC2)
PORT = 5000  # Frontend server port

# For distributed setup, replace with actual IPs:
# PC1_CHAIRMAN_URL = "http://192.168.1.100:5002"
# PC2_COUNCIL_URL = "http://192.168.1.101:5001"

@app.route('/')
def index():
    """Serve the main web interface."""
    return send_from_directory('static', 'index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """
    Check health of all components in the system.
    """
    health_status = {
        "frontend": "healthy",
        "pc1_chairman": "unknown",
        "pc2_council": "unknown"
    }

    # Check PC1 Chairman
    try:
        response = requests.get(f"{PC1_CHAIRMAN_URL}/health", timeout=5)
        if response.status_code == 200:
            health_status["pc1_chairman"] = "healthy"
            health_status["chairman_data"] = response.json()
        else:
            health_status["pc1_chairman"] = f"error: {response.status_code}"
    except Exception as e:
        health_status["pc1_chairman"] = f"error: {str(e)}"

    # Check PC2 Council
    try:
        response = requests.get(f"{PC2_COUNCIL_URL}/health", timeout=5)
        if response.status_code == 200:
            health_status["pc2_council"] = "healthy"
            health_status["council_data"] = response.json()
        else:
            health_status["pc2_council"] = f"error: {response.status_code}"
    except Exception as e:
        health_status["pc2_council"] = f"error: {str(e)}"

    return jsonify(health_status)

@app.route('/stage1', methods=['POST'])
def run_stage1():
    """Stage 1: Get answers from council"""
    data = request.get_json()
    query = data.get('query', '')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    print(f"\n→ Stage 1: Requesting answers from council LLMs...")
    try:
        response = requests.post(
            f"{PC2_COUNCIL_URL}/answer",
            json={"query": query},
            timeout=180
        )
        response.raise_for_status()
        stage1_data = response.json()
        print(f"  ✓ Received {len(stage1_data.get('answers', []))} answers\n")
        return jsonify(stage1_data)
    except Exception as e:
        print(f"  ✗ Stage 1 error: {str(e)}\n")
        return jsonify({"error": str(e)}), 500

@app.route('/stage2', methods=['POST'])
def run_stage2():
    """Stage 2: Get reviews from council"""
    data = request.get_json()
    query = data.get('query', '')
    answers = data.get('answers', [])

    if not query or not answers:
        return jsonify({"error": "Query and answers required"}), 400

    print(f"\n→ Stage 2: Requesting reviews from council LLMs...")
    try:
        response = requests.post(
            f"{PC2_COUNCIL_URL}/review",
            json={"query": query, "answers": answers},
            timeout=180
        )
        response.raise_for_status()
        stage2_data = response.json()
        print(f"  ✓ Received {len(stage2_data.get('reviews', []))} reviews\n")
        return jsonify(stage2_data)
    except Exception as e:
        print(f"  ✗ Stage 2 error: {str(e)}\n")
        return jsonify({"error": str(e)}), 500

@app.route('/stage3', methods=['POST'])
def run_stage3():
    """Stage 3: Get final synthesis from Chairman"""
    data = request.get_json()
    query = data.get('query', '')
    answers = data.get('answers', [])
    reviews = data.get('reviews', [])

    if not query or not answers:
        return jsonify({"error": "Query and answers required"}), 400

    print(f"\n→ Stage 3: Requesting final synthesis from Chairman...")
    try:
        response = requests.post(
            f"{PC1_CHAIRMAN_URL}/synthesize",
            json={"query": query, "answers": answers, "reviews": reviews},
            timeout=300  # Increased to 5 minutes for Chairman synthesis
        )
        response.raise_for_status()
        stage3_data = response.json()
        print(f"  ✓ Received final synthesis\n")
        return jsonify(stage3_data)
    except Exception as e:
        print(f"  ✗ Stage 3 error: {str(e)}\n")
        return jsonify({"error": str(e)}), 500

@app.route('/council', methods=['POST'])
def run_council():
    """
    Execute the full 3-stage LLM Council workflow.

    Request body:
        {
            "query": "What is artificial intelligence?"
        }

    Response:
        {
            "query": "...",
            "stage1_answers": [...],
            "stage2_reviews": [...],
            "stage3_final": "...",
            "chairman_model": "...",
            "errors": [...]
        }
    """
    data = request.get_json()
    query = data.get('query', '')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    result = {
        "query": query,
        "stage1_answers": [],
        "stage2_reviews": [],
        "stage3_final": "",
        "chairman_model": "",
        "errors": []
    }

    print(f"\n{'='*80}")
    print(f"COUNCIL WORKFLOW STARTED")
    print(f"Query: {query}")
    print(f"{'='*80}\n")

    # STAGE 1: Get answers from council (PC2)
    print("→ Stage 1: Requesting answers from council LLMs...")
    try:
        response = requests.post(
            f"{PC2_COUNCIL_URL}/answer",
            json={"query": query},
            timeout=180
        )
        response.raise_for_status()
        stage1_data = response.json()
        result["stage1_answers"] = stage1_data.get("answers", [])
        print(f"  ✓ Received {len(result['stage1_answers'])} answers\n")
    except Exception as e:
        error_msg = f"Stage 1 error: {str(e)}"
        print(f"  ✗ {error_msg}\n")
        result["errors"].append(error_msg)
        return jsonify(result), 500

    # STAGE 2: Get reviews from council (PC2)
    print("→ Stage 2: Requesting reviews from council LLMs...")
    try:
        response = requests.post(
            f"{PC2_COUNCIL_URL}/review",
            json={
                "query": query,
                "answers": result["stage1_answers"]
            },
            timeout=180
        )
        response.raise_for_status()
        stage2_data = response.json()
        result["stage2_reviews"] = stage2_data.get("reviews", [])
        print(f"  ✓ Received {len(result['stage2_reviews'])} reviews\n")
    except Exception as e:
        error_msg = f"Stage 2 error: {str(e)}"
        print(f"  ✗ {error_msg}\n")
        result["errors"].append(error_msg)
        # Continue to Stage 3 even without reviews

    # STAGE 3: Get final synthesis from Chairman (PC1)
    print("→ Stage 3: Requesting final synthesis from Chairman...")
    try:
        response = requests.post(
            f"{PC1_CHAIRMAN_URL}/synthesize",
            json={
                "query": query,
                "answers": result["stage1_answers"],
                "reviews": result["stage2_reviews"]
            },
            timeout=180
        )
        response.raise_for_status()
        stage3_data = response.json()
        result["stage3_final"] = stage3_data.get("final_answer", "")
        result["chairman_model"] = stage3_data.get("chairman_model", "")
        print(f"  ✓ Received final synthesis\n")
    except Exception as e:
        error_msg = f"Stage 3 error: {str(e)}"
        print(f"  ✗ {error_msg}\n")
        result["errors"].append(error_msg)
        return jsonify(result), 500

    print(f"{'='*80}")
    print(f"COUNCIL WORKFLOW COMPLETED SUCCESSFULLY")
    print(f"{'='*80}\n")

    return jsonify(result)

@app.route('/config', methods=['GET'])
def get_config():
    """Return current configuration."""
    return jsonify({
        "pc1_chairman_url": PC1_CHAIRMAN_URL,
        "pc2_council_url": PC2_COUNCIL_URL,
        "frontend_port": PORT
    })

if __name__ == '__main__':
    print(f"""
    ╔════════════════════════════════════════════════════════╗
    ║   LLM COUNCIL FRONTEND COORDINATOR                     ║
    ║   Running on port {PORT}                               ║
    ╚════════════════════════════════════════════════════════╝

    Configuration:
      PC1 Chairman: {PC1_CHAIRMAN_URL}
      PC2 Council:  {PC2_COUNCIL_URL}

    Open your browser:
      → http://localhost:{PORT}

    Endpoints:
      GET  /health  - Check all services
      GET  /config  - View configuration
      POST /council - Run full council workflow

    Make sure PC1 and PC2 servers are running!
    """)

    app.run(host='0.0.0.0', port=PORT, debug=True)
