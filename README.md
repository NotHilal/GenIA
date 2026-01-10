# LLM Council - Local Distributed Deployment

## Team Information

**TD Group:** CCC1

**Team Members:**
- Hilal ELAYOUBI
- Clement FIGARD

---

## Project Overview

This project implements a **distributed LLM Council system** where multiple Large Language Models collaborate to answer user queries through a three-stage workflow:

1. **Stage 1 - Independent Answers:** Multiple council LLMs generate independent responses to a user query
2. **Stage 2 - Peer Review:** Each LLM anonymously reviews and ranks the responses from other models
3. **Stage 3 - Chairman Synthesis:** A dedicated Chairman LLM synthesizes all answers and reviews into a final authoritative response

The system has been refactored from the original cloud-based implementation (using OpenRouter) to run entirely on **local infrastructure** using **Ollama**, with a distributed architecture across multiple physical machines.

---

## System Architecture

### Distributed Design

Our implementation follows a **2-PC distributed architecture**:

- **PC1 (Chairman Server)** - IP: `172.20.10.9:5002`
  - Runs the Chairman LLM (`llama3.2:3b`)
  - Handles Stage 3: Final synthesis

- **PC2 (Council Server)** - IP: `localhost:5001`
  - Runs 3 Council LLMs in parallel:
    - `llama3.2:3b`
    - `mistral:7b`
    - `phi3:mini`
  - Handles Stage 1: Answer generation
  - Handles Stage 2: Peer reviews

- **Frontend Coordinator** - Port: `5000`
  - Web-based user interface
  - Orchestrates communication between PC1 and PC2
  - Displays results with tabbed interface

### Communication Flow

```
User Query → Frontend Coordinator → PC2 Council (Stage 1) →
PC2 Council (Stage 2) → PC1 Chairman (Stage 3) → Frontend → User
```

All services communicate via **REST APIs** using Flask servers and HTTP requests.

---

## Technology Stack

- **Local LLM Framework:** Ollama
- **Backend:** Python 3.x, Flask, Flask-CORS
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Parallel Processing:** ThreadPoolExecutor (concurrent.futures)
- **API Communication:** HTTP REST (requests library)

---

## LLM Models Used

| Model | Parameters | Role | Reason for Selection |
|-------|-----------|------|---------------------|
| `llama3.2:3b` | 3B | Council + Chairman | Balanced performance/quality |
| `mistral:7b` | 7B | Council | Higher quality reasoning |
| `phi3:mini` | 3.8B | Council | Fast inference, diverse perspective |

**Model Selection Rationale:**
- Mix of model sizes provides diverse reasoning approaches
- All models are optimized for local inference
- Balance between quality and speed
- Total diversity in architecture and training data

---

## Setup and Installation

### Prerequisites

- **2 Windows PCs** connected on the same network
- **Python 3.8+** installed on both PCs
- **Ollama** installed on both PCs ([Download Ollama](https://ollama.ai/download))
- **Network connectivity** between PCs (we used mobile hotspot for reliable connection)

### Installation Steps

#### On PC1 (Chairman):

1. Navigate to the `pc1_chairman` folder:
   ```bash
   cd pc1_chairman
   ```

2. Run the setup script:
   ```bash
   setup.bat
   ```
   This will:
   - Pull the Chairman model (`llama3.2:3b`)
   - Install Python dependencies

#### On PC2 (Council):

1. Navigate to the `pc2_council` folder:
   ```bash
   cd pc2_council
   ```

2. Run the setup script:
   ```bash
   setup.bat
   ```
   This will:
   - Pull all 3 council models
   - Install Python dependencies

#### On Frontend PC (can be either PC1 or PC2):

1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Important:** Edit `coordinator.py` and update the IP addresses:
   - Set `PC1_CHAIRMAN_URL` to PC1's actual IP address
   - Set `PC2_COUNCIL_URL` to PC2's actual IP address (or `localhost` if frontend runs on PC2)

---

## Running the Demo

### Step 1: Get IP Addresses

On **PC1**, open CMD and run:
```bash
ipconfig
```
Note the IPv4 address (e.g., `172.20.10.9`)

On **PC2**, do the same and note its IP address.

### Step 2: Start the Servers

**On PC1:**
```bash
cd pc1_chairman
launcher.bat
```
Wait for: `PC1 CHAIRMAN SERVER Running on port 5002`

**On PC2:**
```bash
cd pc2_council
launcher.bat
```
Wait for: `PC2 COUNCIL SERVER Running on port 5001`

**On Frontend PC:**
```bash
cd frontend
python coordinator.py
```
Wait for: `LLM COUNCIL FRONTEND COORDINATOR Running on port 5000`

### Step 3: Access the Web Interface

Open a web browser and navigate to:
```
http://localhost:5000
```

### Step 4: Test the System

1. Check that **PC1 Status** and **PC2 Status** both show **✓ Healthy**
2. Enter a query (e.g., "What is artificial intelligence?")
3. Click **Submit to Council**
4. Watch the progress indicators as each stage completes:
   - Stage 1: Council answers (~30-45 seconds)
   - Stage 2: Peer reviews (~40-60 seconds)
   - Stage 3: Chairman synthesis (~2-4 minutes)
5. View results in the tabbed interface

---

## Key Improvements Over Original Repository

### 1. **Parallel Processing**
- **Original:** Council models answered sequentially (one at a time)
- **Our Implementation:** All 3 council models run in parallel using `ThreadPoolExecutor`
- **Impact:** Stage 1 and Stage 2 are 3x faster

### 2. **Performance Optimization**
- Added Ollama inference parameters:
  - `temperature`: 0.7-0.8 (faster sampling)
  - `num_predict`: 150 tokens (faster generation)
  - `top_k`: 40 (reduced sampling space)
  - `top_p`: 0.9 (nucleus sampling)
- **Impact:** Overall workflow ~60% faster

### 3. **Real-Time Progress Tracking**
- **Original:** No progress feedback during processing
- **Our Implementation:** Live progress indicators showing active stage with visual feedback
- **Impact:** Better user experience, transparent processing

### 4. **Distributed Architecture**
- **Original:** Cloud-based, single server
- **Our Implementation:** True distributed system across 2 physical PCs
- **Impact:** Demonstrates scalability, load distribution, network communication

### 5. **Enhanced Frontend**
- Status health monitoring for both PCs
- Tabbed interface for viewing different stages
- Clean, modern UI with responsive design
- Error handling and display

### 6. **Network Resilience**
- Configurable timeouts for each stage
- Health check endpoints
- Clear error messages for debugging

---

## Project Structure

```
GenIA/
├── pc1_chairman/
│   ├── chairman_server.py      # Chairman LLM server
│   ├── setup.bat               # One-click installation
│   ├── launcher.bat            # One-click server start
│   └── requirements.txt
│
├── pc2_council/
│   ├── council_server.py       # Council LLMs server
│   ├── setup.bat               # One-click installation
│   ├── launcher.bat            # One-click server start
│   └── requirements.txt
│
├── frontend/
│   ├── coordinator.py          # Frontend coordinator server
│   ├── static/
│   │   ├── index.html         # Web interface
│   │   ├── script.js          # Frontend logic
│   │   └── style.css          # Styling
│   └── requirements.txt
│
└── README.md                   # This file
```

---

## API Endpoints

### PC2 Council Server (Port 5001)
- `GET /health` - Health check
- `GET /models` - List available council models
- `GET /test` - Test all models
- `POST /answer` - Generate answers (Stage 1)
- `POST /review` - Generate reviews (Stage 2)

### PC1 Chairman Server (Port 5002)
- `GET /health` - Health check
- `GET /model` - Get chairman model info
- `GET /test` - Test chairman model
- `POST /synthesize` - Generate final synthesis (Stage 3)

### Frontend Coordinator (Port 5000)
- `GET /` - Web interface
- `GET /health` - Check all services
- `GET /config` - View configuration
- `POST /stage1` - Execute Stage 1
- `POST /stage2` - Execute Stage 2
- `POST /stage3` - Execute Stage 3
- `POST /council` - Execute full workflow

---

## Troubleshooting

### PCs Can't Communicate
- Ensure both PCs are on the same network
- Try using a mobile hotspot instead of WiFi
- Disable Windows Firewall on both PCs
- Set network to "Private" in Windows settings
- Test with `ping <other-pc-ip>`

### Models Not Found
- Run `ollama list` to check installed models
- Re-run `setup.bat` to pull models again

### Stage 3 Timeout
- This is normal for first run (model loading)
- Subsequent runs should be faster
- Ensure PC1 has sufficient RAM (4GB+ recommended)

### CSS/JS Not Loading
- Paths should be `/static/style.css` and `/static/script.js`
- Check browser console for 404 errors

---

## Performance Metrics

**Typical execution times:**
- Stage 1 (Answers): ~24 seconds
- Stage 2 (Reviews): ~39 seconds
- Stage 3 (Synthesis): ~90-180 seconds
- **Total:** ~2.5-4 minutes per query

---

## Generative AI Usage Statement

### Declaration of Generative AI Usage

This project utilized **Generative AI tools** during development. In accordance with the course policy, we declare the following usage:

**Tool Used:** Claude Code (Anthropic's Claude Sonnet 4.5 via CLI)

**Purpose and Scope:**
1. **Code Architecture & Implementation:**
   - Initial project structure design
   - Flask server implementation for PC1, PC2, and Frontend
   - REST API endpoint design
   - Parallel processing implementation using ThreadPoolExecutor

2. **Performance Optimization:**
   - Ollama parameter tuning for faster inference
   - Parallel execution strategy for council models
   - Timeout configuration and optimization

3. **Frontend Development:**
   - HTML/CSS/JavaScript implementation
   - Real-time progress tracking system
   - Tabbed interface design
   - Error handling and user feedback

4. **Debugging & Troubleshooting:**
   - Network connectivity issues (PC-to-PC communication)
   - Static file path resolution (404 errors)
   - Stage 3 timeout debugging
   - Cross-origin resource sharing (CORS) configuration

5. **Documentation:**
   - This README.md file
   - Code comments and docstrings
   - Setup instructions

**Student Contributions:**
- System testing on physical hardware
- Network setup and configuration
- Model selection and evaluation
- Project integration and validation
- Design decisions and requirements analysis
- Live demo preparation

**Rationale:**
We chose to leverage Claude Code to accelerate development and focus on understanding distributed systems architecture, local LLM deployment, and the council workflow concept rather than low-level implementation details. All code generated was reviewed, tested, and understood by the team.

---

## Future Enhancements

Potential improvements for future versions:
- Add model performance dashboard
- Implement response time tracking per model
- Add dark/light mode toggle
- Enable side-by-side comparison of council answers
- Add token usage estimation
- Implement model health monitoring with heartbeat
- Support for additional local LLM frameworks (GPT4All, Llamafile)
- Persistent storage of query history
- Export results to PDF/JSON

---

## License

This project is an academic implementation for educational purposes.

---

## Acknowledgments

- Inspired by Andrej Karpathy's LLM Council concept
- Built using Ollama for local LLM inference
- Course: Generative AI (TD CCC1)

---

## Contact

For questions or issues, contact:
- Hilal ELAYOUBI
- Clement FIGARD
