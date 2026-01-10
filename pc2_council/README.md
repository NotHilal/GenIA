# PC2 Council Server

This server runs on PC2 and hosts the council LLMs that generate answers and reviews.

## What Runs Here

- **3+ Council LLMs** (default: llama3.2:3b, mistral:7b, phi3:mini)
- **Stage 1:** Independent answer generation
- **Stage 2:** Peer review and ranking

## Prerequisites

1. **Ollama installed and running**
   ```bash
   # Download from https://ollama.ai
   # Start Ollama (it usually auto-starts)
   ```

2. **Models pulled**
   ```bash
   ollama pull llama3.2:3b
   ollama pull mistral:7b
   ollama pull phi3:mini
   ```

3. **Python 3.8+**

## Setup

1. Install dependencies:
   ```bash
   cd pc2_council
   pip install -r requirements.txt
   ```

2. Configure the server (edit `council_server.py`):
   ```python
   # Line 12-14: Configure Ollama
   OLLAMA_URL = "http://localhost:11434"
   PORT = 5001

   # Line 17-21: Configure models
   COUNCIL_MODELS = [
       "llama3.2:3b",
       "mistral:7b",
       "phi3:mini"
   ]
   ```

3. Test that Ollama is working:
   ```bash
   ollama list  # Should show your models
   ```

## Running

```bash
python council_server.py
```

The server will start on `http://0.0.0.0:5001` (accessible from other PCs on your network).

## API Endpoints

### GET /health
Check server health and configuration.

```bash
curl http://localhost:5001/health
```

### GET /models
List available council models.

```bash
curl http://localhost:5001/models
```

### GET /test
Test all models to ensure they're working.

```bash
curl http://localhost:5001/test
```

### POST /answer (Stage 1)
Generate independent answers from all models.

```bash
curl -X POST http://localhost:5001/answer \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the capital of France?"}'
```

### POST /review (Stage 2)
Have models review and rank each other's answers.

```bash
curl -X POST http://localhost:5001/review \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the capital of France?",
    "answers": [
      {"model": "llama3.2:3b", "response": "Paris is the capital..."},
      {"model": "mistral:7b", "response": "The capital is Paris..."}
    ]
  }'
```

## Network Configuration

To allow PC1 and the frontend to connect to this server:

1. **Find your IP address:**
   ```bash
   # Windows
   ipconfig

   # Linux/Mac
   ifconfig
   ```

2. **Configure firewall:**
   - Allow incoming connections on port 5001
   - Windows: `Windows Firewall > Advanced Settings > Inbound Rules > New Rule`
   - Linux: `sudo ufw allow 5001`

3. **Share your IP with your teammate:**
   - They'll need to configure `PC2_COUNCIL_URL = "http://<YOUR_IP>:5001"`

## Troubleshooting

### "Connection refused" errors
- Check Ollama is running: `ollama list`
- Check server is running on correct port
- Check firewall settings

### "Model not found" errors
- Pull the model: `ollama pull <model-name>`
- Verify: `ollama list`

### Slow responses
- Smaller models are faster (3b vs 7b)
- Close other applications to free up RAM
- Consider using quantized models

### Network issues
- Ensure both PCs are on the same network
- Test connectivity: `ping <PC2_IP>` from PC1
- Check firewall isn't blocking port 5001

## Adding More Models

To add more council members:

1. Pull the model:
   ```bash
   ollama pull gemma:7b
   ```

2. Edit `council_server.py`:
   ```python
   COUNCIL_MODELS = [
       "llama3.2:3b",
       "mistral:7b",
       "phi3:mini",
       "gemma:7b"  # Added
   ]
   ```

3. Restart the server

## Performance Tips

- **Use smaller models** for faster responses (3b-7b param range)
- **Limit concurrent requests** - council runs sequentially by design
- **Monitor RAM usage** - each model needs memory when active
- **Use SSD** for faster model loading

## Example Output

When the server receives a request, you'll see:

```
============================================================
STAGE 1: Generating answers for query: What is AI?
============================================================

Requesting answer from llama3.2:3b...
  ✓ llama3.2:3b responded (342 chars)

Requesting answer from mistral:7b...
  ✓ mistral:7b responded (298 chars)

Requesting answer from phi3:mini...
  ✓ phi3:mini responded (315 chars)

Stage 1 complete: 3 answers generated
```
