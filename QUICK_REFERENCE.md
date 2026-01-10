# LLM Council - Quick Reference Card

Print this for easy reference during setup and demo!

---

## System Architecture

```
┌─────────────┐         ┌─────────────┐
│   PC1       │         │   PC2       │
│  Chairman   │◄───────►│  Council    │
│             │         │             │
│ Port: 5002  │         │ Port: 5001  │
│ Model: 1    │         │ Models: 3+  │
└─────────────┘         └─────────────┘
       ▲                       ▲
       │                       │
       └───────┬───────────────┘
               │
       ┌───────▼────────┐
       │   Frontend     │
       │  Coordinator   │
       │  Port: 5000    │
       └────────────────┘
```

---

## Network Configuration

**PC1 IP:** ________________ (fill in)
**PC2 IP:** ________________ (fill in)

**PC1 Chairman:** `http://<PC1_IP>:5002`
**PC2 Council:** `http://<PC2_IP>:5001`
**Frontend:** `http://localhost:5000`

---

## Required Models

### PC1 (Chairman)
```bash
ollama pull llama3.2:3b
```

### PC2 (Council)
```bash
ollama pull llama3.2:3b
ollama pull mistral:7b
ollama pull phi3:mini
```

---

## Starting the System

**Order matters! Start in this sequence:**

### 1. Start PC2 Council
```bash
cd pc2_council
python council_server.py
```
Expected: Server running on port 5001

### 2. Start PC1 Chairman
```bash
cd pc1_chairman
python chairman_server.py
```
Expected: Server running on port 5002

### 3. Start Frontend
```bash
cd frontend
python coordinator.py
```
Expected: Server running on port 5000

### 4. Open Browser
```
http://localhost:5000
```
Expected: Green status for both PC1 and PC2

---

## Testing Commands

### Check Ollama
```bash
ollama list
```

### Test PC2 Health
```bash
curl http://localhost:5001/health
```

### Test PC1 Health
```bash
curl http://localhost:5002/health
```

### Test Frontend
```bash
curl http://localhost:5000/health
```

### Full Setup Test
```bash
python test_setup.py
```

---

## Common Issues

| Problem | Solution |
|---------|----------|
| Connection refused | Check server is running |
| Model not found | `ollama pull <model>` |
| Timeout | Increase timeout in code |
| Slow response | Normal! Wait 30-90 sec |
| Red status | Check firewall/IP |

---

## Firewall Ports

**PC1:** Allow incoming on port 5002
**PC2:** Allow incoming on port 5001

---

## Demo Checklist

- [ ] Both PCs on same network
- [ ] Ollama running (`ollama list`)
- [ ] All models pulled
- [ ] Firewalls configured
- [ ] PC2 server started (5001)
- [ ] PC1 server started (5002)
- [ ] Frontend started (5000)
- [ ] Browser shows green status
- [ ] Test query works

---

## API Endpoints

### PC2 Council (5001)
- `GET /health` - Health check
- `GET /models` - List models
- `GET /test` - Test models
- `POST /answer` - Stage 1
- `POST /review` - Stage 2

### PC1 Chairman (5002)
- `GET /health` - Health check
- `GET /model` - Get chairman model
- `GET /test` - Test model
- `POST /synthesize` - Stage 3

### Frontend (5000)
- `GET /` - Web UI
- `GET /health` - Check all
- `GET /config` - Show config
- `POST /council` - Full workflow

---

## Stopping the System

**Reverse order:**

1. Stop frontend (Ctrl+C)
2. Stop PC1 chairman (Ctrl+C)
3. Stop PC2 council (Ctrl+C)

---

## Emergency Commands

### Restart Ollama
```bash
# Linux/Mac
sudo systemctl restart ollama

# Windows
# Restart from Task Manager
```

### Check if port is in use
```bash
# Windows
netstat -ano | findstr :5001

# Linux/Mac
lsof -i :5001
```

### Kill process on port
```bash
# Windows
taskkill /PID <PID> /F

# Linux/Mac
kill -9 <PID>
```

---

## File Locations

```
GenIA/
├── README.md              ← Main documentation
├── SETUP_GUIDE.md         ← Detailed setup
├── QUICK_REFERENCE.md     ← This file
├── test_setup.py          ← Test script
├── pc1_chairman/          ← PC1 code
│   ├── chairman_server.py
│   └── requirements.txt
├── pc2_council/           ← PC2 code
│   ├── council_server.py
│   └── requirements.txt
└── frontend/              ← Frontend code
    ├── coordinator.py
    ├── requirements.txt
    └── static/
```

---

## Test Queries

**Simple:**
- What is the capital of France?
- What is 2+2?

**Medium:**
- Explain how photosynthesis works
- What are the benefits of remote work?

**Complex:**
- Compare and contrast different machine learning algorithms
- Explain the ethical implications of AI

---

## Expected Timing

- **Stage 1 (Answers):** 15-30 seconds
- **Stage 2 (Reviews):** 15-30 seconds
- **Stage 3 (Synthesis):** 10-20 seconds
- **Total:** 40-80 seconds

Longer times = larger models or slower hardware

---

## Contact Info

**Team Member 1 (PC1):**
Name: ________________
Email: ________________
Phone: ________________

**Team Member 2 (PC2):**
Name: ________________
Email: ________________
Phone: ________________

---

## Demo Presentation Order

1. **Introduction** (1 min)
   - Team introduction
   - Project overview

2. **Architecture** (2 min)
   - Show 2-PC setup
   - Explain distributed design

3. **Live Demo** (5 min)
   - Submit query
   - Show Stage 1 results
   - Show Stage 2 reviews
   - Show Stage 3 synthesis

4. **Technical Details** (2 min)
   - Ollama integration
   - REST API design
   - Improvements made

5. **Q&A** (2 min)

Total: ~12 minutes

---

## Troubleshooting Tree

```
Problem: Not working
│
├─ Servers running?
│  ├─ NO → Start them
│  └─ YES → Continue
│
├─ Green status?
│  ├─ NO → Check network/firewall
│  └─ YES → Continue
│
├─ Ollama working?
│  ├─ NO → Restart Ollama
│  └─ YES → Continue
│
└─ Still broken?
   └─ Check logs for errors
```

---

**Good luck with your demo!**
