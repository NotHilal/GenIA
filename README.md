# LLM Council - Local Deployment

A distributed multi-LLM system where multiple language models collaborate to answer queries through a 3-stage process: independent answers, peer review, and final synthesis.

## Team Information
- **Team Members:** [Your names here]
- **TD Group:** [Your TD group]

## Project Overview

This implementation replaces cloud-based LLM APIs with local inference using Ollama. The system runs across 2 PCs:

- **PC1 (Chairman):** Runs the Chairman LLM that synthesizes final answers
- **PC2 (Council):** Runs 3+ council LLMs that generate answers and reviews
- **Frontend:** Web interface to coordinate the workflow (can run on either PC)

## Architecture

```
User Query → Frontend Coordinator
                ↓
    Stage 1: First Opinions (PC2)
    - LLM 1 answers independently
    - LLM 2 answers independently
    - LLM 3 answers independently
                ↓
    Stage 2: Review & Ranking (PC2)
    - Each LLM ranks others' answers
                ↓
    Stage 3: Final Synthesis (PC1)
    - Chairman LLM creates final answer
                ↓
    Display Results to User
```

## System Requirements

### Both PCs Need:
- Python 3.8+
- Ollama installed and running
- Network connectivity between PCs

### Recommended Models (download via Ollama):
- **PC2 Council:** `llama3.2:3b`, `mistral:7b`, `phi3:mini` (or any 3+ models)
- **PC1 Chairman:** `llama3.2:3b` (or any model)

## Quick Start

### 1. Install Ollama on Both PCs

**Windows/Mac/Linux:**
```bash
# Download from https://ollama.ai
# Or use:
curl -fsSL https://ollama.com/install.sh | sh
```

**Pull required models:**
```bash
# On PC2 (Council)
ollama pull llama3.2:3b
ollama pull mistral:7b
ollama pull phi3:mini

# On PC1 (Chairman)
ollama pull llama3.2:3b
```

### 2. Setup PC2 (Council Server)

```bash
cd pc2_council
pip install -r requirements.txt

# Edit council_server.py to configure:
# - Available models
# - Port (default: 5001)

python council_server.py
```

**PC2 will run on:** `http://<PC2_IP>:5001`

### 3. Setup PC1 (Chairman Server)

```bash
cd pc1_chairman
pip install -r requirements.txt

# Edit chairman_server.py to configure:
# - Chairman model
# - Port (default: 5002)

python chairman_server.py
```

**PC1 will run on:** `http://<PC1_IP>:5002`

### 4. Setup Frontend (Either PC)

```bash
cd frontend
pip install -r requirements.txt

# Edit coordinator.py to set:
# - PC1_CHAIRMAN_URL = "http://<PC1_IP>:5002"
# - PC2_COUNCIL_URL = "http://<PC2_IP>:5001"

python coordinator.py
```

**Access the UI at:** `http://localhost:5000`

## Usage

1. Open the web interface at `http://localhost:5000`
2. Enter your query
3. Click "Submit to Council"
4. View results in tabs:
   - **Stage 1:** Individual LLM responses
   - **Stage 2:** Review rankings
   - **Stage 3:** Chairman's final answer

## Project Structure

```
GenIA/
├── pc1_chairman/          # Runs on PC1
│   ├── chairman_server.py # Chairman LLM API
│   ├── requirements.txt
│   └── README.md
├── pc2_council/           # Runs on PC2
│   ├── council_server.py  # Council LLMs API
│   ├── requirements.txt
│   └── README.md
├── frontend/              # Can run on either PC
│   ├── coordinator.py     # Main coordinator
│   ├── requirements.txt
│   ├── static/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   └── README.md
└── README.md             # This file
```

## Key Design Decisions

### 1. **Ollama for Local Inference**
- Easy setup and model management
- Consistent API across different models
- Low resource overhead

### 2. **REST API Architecture**
- Flask-based microservices
- Clear separation between Chairman and Council
- Easy to scale and debug

### 3. **3-Stage Workflow**
- **Stage 1:** Parallel independent responses
- **Stage 2:** Anonymous peer review
- **Stage 3:** Synthesis with all context

### 4. **Model Selection**
- Smaller models (3B-7B params) for faster responses
- Different model families for diverse reasoning
- Configurable via simple Python lists

## Technical Implementation

### PC2 Council Server
- Hosts multiple LLM endpoints
- `/answer` - Stage 1: Generate independent answers
- `/review` - Stage 2: Rank other answers
- Each model runs via Ollama API

### PC1 Chairman Server
- Single LLM for synthesis
- `/synthesize` - Stage 3: Create final answer
- Receives all responses and rankings

### Frontend Coordinator
- Orchestrates the 3-stage workflow
- RESTful communication with both servers
- Displays results in tabbed interface

## Improvements Over Original

1. **Fully Local Execution** - No API keys or cloud dependencies
2. **True Distribution** - Actual multi-machine setup
3. **Model Flexibility** - Easy to swap models
4. **Clean Architecture** - Separated concerns, modular design
5. **Simple Deployment** - Minimal dependencies

## Troubleshooting

### Ollama Connection Issues
```bash
# Check Ollama is running
ollama list

# Test Ollama API
curl http://localhost:11434/api/tags
```

### Network Issues Between PCs
- Ensure both PCs are on same network
- Check firewall allows ports 5001, 5002
- Use `ipconfig` (Windows) or `ifconfig` (Linux/Mac) to find IP addresses

### Model Not Found
```bash
# List available models
ollama list

# Pull missing model
ollama pull <model-name>
```

## Generative AI Usage Statement

[Include details about any AI tools used during development]

## Demo Checklist

- [ ] PC1 Chairman server running
- [ ] PC2 Council server running (3+ models)
- [ ] Frontend accessible
- [ ] Submit a test query
- [ ] Show Stage 1: Individual responses
- [ ] Show Stage 2: Review rankings
- [ ] Show Stage 3: Chairman synthesis
- [ ] Explain architecture and distribution

## Future Enhancements

- [ ] Model health monitoring
- [ ] Performance metrics dashboard
- [ ] Dark mode UI
- [ ] Response comparison view
- [ ] Load balancing
- [ ] Caching layer

## License

Educational project for [Your Course Name]
