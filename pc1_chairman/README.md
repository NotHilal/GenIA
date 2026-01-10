# PC1 Chairman Server

This server runs on PC1 and hosts the Chairman LLM that synthesizes the final answer.

## What Runs Here

- **Chairman LLM** (default: llama3.2:3b)
- **Stage 3:** Final answer synthesis

## Prerequisites

1. **Ollama installed and running**
   ```bash
   # Download from https://ollama.ai
   # Start Ollama (it usually auto-starts)
   ```

2. **Chairman model pulled**
   ```bash
   ollama pull llama3.2:3b
   ```

3. **Python 3.8+**

## Setup

1. Install dependencies:
   ```bash
   cd pc1_chairman
   pip install -r requirements.txt
   ```

2. Configure the server (edit `chairman_server.py`):
   ```python
   # Line 15-16: Configure Ollama
   OLLAMA_URL = "http://localhost:11434"
   PORT = 5002

   # Line 19: Configure Chairman model
   CHAIRMAN_MODEL = "llama3.2:3b"
   ```

3. Test that Ollama is working:
   ```bash
   ollama list  # Should show your Chairman model
   ```

## Running

```bash
python chairman_server.py
```

The server will start on `http://0.0.0.0:5002` (accessible from other PCs on your network).

## API Endpoints

### GET /health
Check server health and configuration.

```bash
curl http://localhost:5002/health
```

### GET /model
Get the Chairman model being used.

```bash
curl http://localhost:5002/model
```

### GET /test
Test the Chairman model to ensure it's working.

```bash
curl http://localhost:5002/test
```

### POST /synthesize (Stage 3)
Generate the final synthesized answer.

```bash
curl -X POST http://localhost:5002/synthesize \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the capital of France?",
    "answers": [
      {"model": "llama3.2:3b", "response": "Paris is the capital..."},
      {"model": "mistral:7b", "response": "The capital is Paris..."}
    ],
    "reviews": [
      {
        "reviewer": "llama3.2:3b",
        "review_text": "Answer 1 is more detailed...",
        "rankings": [{"answer_id": 0, "rank": 1}]
      }
    ]
  }'
```

## Network Configuration

To allow the frontend to connect to this server:

1. **Find your IP address:**
   ```bash
   # Windows
   ipconfig

   # Linux/Mac
   ifconfig
   ```

2. **Configure firewall:**
   - Allow incoming connections on port 5002
   - Windows: `Windows Firewall > Advanced Settings > Inbound Rules > New Rule`
   - Linux: `sudo ufw allow 5002`

3. **Share your IP:**
   - The frontend will need `PC1_CHAIRMAN_URL = "http://<YOUR_IP>:5002"`

## Chairman's Role

The Chairman LLM does NOT participate in Stage 1 (answering) or Stage 2 (reviewing).

The Chairman ONLY:
- Receives all council answers
- Receives all peer reviews
- Synthesizes everything into one final, authoritative answer

This separation ensures:
- The Chairman remains impartial
- The synthesis considers all perspectives
- Clear division of responsibilities

## Troubleshooting

### "Connection refused" errors
- Check Ollama is running: `ollama list`
- Check server is running on correct port
- Check firewall settings

### "Model not found" errors
- Pull the model: `ollama pull llama3.2:3b`
- Verify: `ollama list`

### Slow synthesis
- The Chairman needs to process all answers and reviews
- Use a smaller model (3b instead of 7b)
- Expected: 10-30 seconds depending on context size

### Network issues
- Ensure PC1 is accessible from the frontend
- Test connectivity: `ping <PC1_IP>`
- Check firewall isn't blocking port 5002

## Choosing a Chairman Model

You can use any Ollama model as the Chairman. Consider:

**Fast synthesis (recommended):**
- `llama3.2:3b` - Good balance of speed and quality
- `phi3:mini` - Very fast, decent quality

**Higher quality (slower):**
- `llama3.2:7b` - Better synthesis, more nuanced
- `mistral:7b` - Strong reasoning

**Large context:**
- Models with large context windows if you have many council members

To change the Chairman:
```bash
ollama pull mistral:7b
```

Edit `chairman_server.py`:
```python
CHAIRMAN_MODEL = "mistral:7b"
```

Restart the server.

## Performance Tips

- **Use smaller models** for faster synthesis (3b-7b param range)
- **Monitor RAM usage** - Chairman processes large prompts
- **SSD recommended** for faster model loading
- **Close other applications** when synthesizing

## Example Output

When the Chairman receives a synthesis request:

```
============================================================
STAGE 3: Chairman synthesizing final answer
Query: What is AI?
Received 3 answers and 3 reviews
============================================================

Generating synthesis from Chairman model...
✓ Chairman synthesis complete (542 chars)
```
