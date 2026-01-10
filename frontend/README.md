# Frontend Coordinator

This is the web interface and coordinator for the LLM Council system. It can run on either PC or on a third machine.

## What This Does

- **Serves the web UI** for user interaction
- **Coordinates the workflow** between PC1 (Chairman) and PC2 (Council)
- **Orchestrates all 3 stages** of the council process
- **Displays results** in an intuitive tabbed interface

## Prerequisites

1. **Python 3.8+**
2. **PC1 Chairman server** running and accessible
3. **PC2 Council server** running and accessible

## Setup

1. Install dependencies:
   ```bash
   cd frontend
   pip install -r requirements.txt
   ```

2. Configure server URLs (edit `coordinator.py`):
   ```python
   # Line 15-16: Set PC URLs
   PC1_CHAIRMAN_URL = "http://192.168.1.100:5002"  # Replace with PC1's IP
   PC2_COUNCIL_URL = "http://192.168.1.101:5001"   # Replace with PC2's IP
   PORT = 5000  # Frontend port
   ```

   **For local testing on one PC:**
   ```python
   PC1_CHAIRMAN_URL = "http://localhost:5002"
   PC2_COUNCIL_URL = "http://localhost:5001"
   ```

## Running

```bash
python coordinator.py
```

Then open your browser:
```
http://localhost:5000
```

## Usage

1. **Check Status**
   - Green indicators mean services are healthy
   - Red means error or unreachable

2. **Submit Query**
   - Enter your question in the text area
   - Click "Submit to Council"
   - Wait for processing (can take 30-60 seconds)

3. **View Results**
   - **Stage 1 Tab:** See each LLM's independent answer
   - **Stage 2 Tab:** See peer reviews and rankings
   - **Stage 3 Tab:** See Chairman's final synthesis

4. **Clear Results**
   - Click "Clear Results" to reset the interface

## API Endpoints

### GET /
Serves the main web interface.

### GET /health
Check health of all connected services.

**Response:**
```json
{
  "frontend": "healthy",
  "pc1_chairman": "healthy",
  "pc2_council": "healthy",
  "chairman_data": {...},
  "council_data": {...}
}
```

### GET /config
Get current configuration.

**Response:**
```json
{
  "pc1_chairman_url": "http://...",
  "pc2_council_url": "http://...",
  "frontend_port": 5000
}
```

### POST /council
Execute the full 3-stage council workflow.

**Request:**
```json
{
  "query": "What is artificial intelligence?"
}
```

**Response:**
```json
{
  "query": "...",
  "stage1_answers": [
    {"model": "llama3.2:3b", "response": "..."},
    ...
  ],
  "stage2_reviews": [
    {"reviewer": "llama3.2:3b", "review_text": "...", "rankings": [...]},
    ...
  ],
  "stage3_final": "The synthesized answer...",
  "chairman_model": "llama3.2:3b",
  "errors": []
}
```

## Network Configuration

### Option 1: Run on PC1 or PC2
If running the frontend on PC1:
```python
PC1_CHAIRMAN_URL = "http://localhost:5002"
PC2_COUNCIL_URL = "http://<PC2_IP>:5001"
```

If running the frontend on PC2:
```python
PC1_CHAIRMAN_URL = "http://<PC1_IP>:5002"
PC2_COUNCIL_URL = "http://localhost:5001"
```

### Option 2: Run on Third Machine
```python
PC1_CHAIRMAN_URL = "http://<PC1_IP>:5002"
PC2_COUNCIL_URL = "http://<PC2_IP>:5001"
```

### Getting IP Addresses
**Windows:**
```bash
ipconfig
# Look for "IPv4 Address"
```

**Linux/Mac:**
```bash
ifconfig
# or
ip addr show
```

## Troubleshooting

### "PC1 Chairman: Error" or "PC2 Council: Error"

**Check if servers are running:**
```bash
# On PC1
curl http://localhost:5002/health

# On PC2
curl http://localhost:5001/health
```

**Check network connectivity:**
```bash
# From frontend machine
ping <PC1_IP>
ping <PC2_IP>
```

**Check firewall:**
- Ensure ports 5001 and 5002 are open on both PCs
- Test with telnet: `telnet <PC_IP> <PORT>`

### "Connection refused"

1. Verify the IP addresses in `coordinator.py` are correct
2. Ensure both PC1 and PC2 servers are running
3. Check that all PCs are on the same network
4. Try accessing the URLs directly in a browser

### Slow responses

This is normal! The council workflow involves:
- 3+ LLMs generating answers (Stage 1)
- 3+ LLMs writing reviews (Stage 2)
- 1 Chairman synthesizing (Stage 3)

Expected time: **30-90 seconds** depending on:
- Number of council members
- Model sizes
- Query complexity
- Hardware performance

### Timeouts

If you get timeout errors, increase the timeout values in `coordinator.py`:

```python
# Line 80, 106, 128 - Change timeout=180 to timeout=300
timeout=300  # 5 minutes
```

## UI Features

### Status Indicators
- **Green (✓ Healthy):** Service is running and responding
- **Red (✗ Error):** Service is unreachable or erroring
- **Gray (⚫ Unknown):** Status not yet checked

### Tabs
- **Stage 1:** Shows all council members' answers
- **Stage 2:** Shows peer reviews
- **Stage 3:** Shows Chairman's final answer

### Badges
- Show count of answers/reviews

### Keyboard Shortcuts
- **Ctrl+Enter:** Submit query while in text area

## Customization

### Change Port
Edit `coordinator.py`:
```python
PORT = 5000  # Change to your desired port
```

### Styling
Edit `static/style.css` to customize:
- Colors (see `:root` CSS variables)
- Fonts
- Layout
- Spacing

### Add Features
Edit `static/script.js` to add:
- Loading progress indicators
- Model performance metrics
- Export functionality
- History of queries

## Example Queries to Test

1. **General knowledge:**
   - "What is the capital of France?"
   - "Explain photosynthesis"

2. **Technical:**
   - "What is the difference between REST and GraphQL?"
   - "Explain how neural networks work"

3. **Opinion/Analysis:**
   - "What are the pros and cons of remote work?"
   - "Compare Python and JavaScript for web development"

4. **Complex reasoning:**
   - "If a train leaves Paris at 2pm going 80km/h, and another leaves Lyon at 3pm going 100km/h, when do they meet?"
   - "Explain the trolley problem and different ethical perspectives"

## Production Considerations

This is an educational prototype. For production:

1. **Add authentication** to protect the endpoints
2. **Use HTTPS** for secure communication
3. **Implement rate limiting** to prevent abuse
4. **Add logging** for debugging and monitoring
5. **Use a production WSGI server** (not Flask debug server)
6. **Add error recovery** and retry logic
7. **Implement caching** to reduce redundant requests
8. **Add request queuing** for handling concurrent users

## Architecture Overview

```
User Browser
    ↓
Frontend Server (coordinator.py)
    ↓
    ├─→ PC2 Council Server (Stage 1 & 2)
    │       ↓
    │   Ollama → Multiple LLMs
    │
    └─→ PC1 Chairman Server (Stage 3)
            ↓
        Ollama → Chairman LLM
```

The frontend is stateless and simply orchestrates communication between the two backend servers.
