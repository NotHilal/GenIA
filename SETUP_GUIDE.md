# LLM Council - Complete Setup Guide

This guide will walk you through setting up the entire LLM Council system across 2 PCs.

## Overview

**Your Team (2 people):**
- **Person 1:** Manages PC1 (Chairman)
- **Person 2:** Manages PC2 (Council)
- **Either person:** Runs the frontend (or run on one of the PCs)

**Timeline:** Allow 30-60 minutes for first-time setup

---

## Phase 1: Install Ollama on Both PCs (15 min)

### On PC1 (Chairman)

1. **Download and install Ollama:**
   - Visit: https://ollama.ai
   - Download for your OS (Windows/Mac/Linux)
   - Run installer

2. **Verify installation:**
   ```bash
   ollama --version
   ```

3. **Pull the Chairman model:**
   ```bash
   ollama pull llama3.2:3b
   ```

4. **Verify the model:**
   ```bash
   ollama list
   # Should show llama3.2:3b
   ```

### On PC2 (Council)

1. **Download and install Ollama:**
   - Visit: https://ollama.ai
   - Download for your OS
   - Run installer

2. **Verify installation:**
   ```bash
   ollama --version
   ```

3. **Pull the council models:**
   ```bash
   ollama pull llama3.2:3b
   ollama pull mistral:7b
   ollama pull phi3:mini
   ```

   **Note:** These are large downloads (3-7 GB each). Make sure you have:
   - Good internet connection
   - At least 20 GB free disk space

4. **Verify all models:**
   ```bash
   ollama list
   # Should show all 3 models
   ```

---

## Phase 2: Network Setup (10 min)

### Find IP Addresses

**On PC1:**
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```

Look for something like: `192.168.1.100`
**Write this down as PC1_IP**

**On PC2:**
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```

Look for something like: `192.168.1.101`
**Write this down as PC2_IP**

### Test Connectivity

**From PC1, ping PC2:**
```bash
ping <PC2_IP>
```

**From PC2, ping PC1:**
```bash
ping <PC1_IP>
```

Both should respond successfully.

### Configure Firewalls

**On PC1:**
- Allow incoming on port 5002

**Windows:**
```
Control Panel → Windows Defender Firewall → Advanced Settings
→ Inbound Rules → New Rule → Port → TCP 5002 → Allow
```

**Linux:**
```bash
sudo ufw allow 5002
```

**On PC2:**
- Allow incoming on port 5001

**Windows:**
```
Control Panel → Windows Defender Firewall → Advanced Settings
→ Inbound Rules → New Rule → Port → TCP 5001 → Allow
```

**Linux:**
```bash
sudo ufw allow 5001
```

---

## Phase 3: Install Python Dependencies (5 min)

### On PC1

```bash
cd GenIA/pc1_chairman
pip install -r requirements.txt
```

### On PC2

```bash
cd GenIA/pc2_council
pip install -r requirements.txt
```

### On Frontend PC (choose PC1 or PC2)

```bash
cd GenIA/frontend
pip install -r requirements.txt
```

---

## Phase 4: Configuration (5 min)

### On PC2 (Council)

Edit `pc2_council/council_server.py`:

```python
# Line 12-14
OLLAMA_URL = "http://localhost:11434"  # Keep as localhost
PORT = 5001  # Keep as 5001

# Line 17-21 - Verify these models are pulled
COUNCIL_MODELS = [
    "llama3.2:3b",
    "mistral:7b",
    "phi3:mini"
]
```

### On PC1 (Chairman)

Edit `pc1_chairman/chairman_server.py`:

```python
# Line 15-16
OLLAMA_URL = "http://localhost:11434"  # Keep as localhost
PORT = 5002  # Keep as 5002

# Line 19 - Verify this model is pulled
CHAIRMAN_MODEL = "llama3.2:3b"
```

### On Frontend PC

Edit `frontend/coordinator.py`:

```python
# Line 15-17
PC1_CHAIRMAN_URL = "http://<PC1_IP>:5002"  # Use actual PC1 IP
PC2_COUNCIL_URL = "http://<PC2_IP>:5001"   # Use actual PC2 IP
PORT = 5000
```

**Example:**
```python
PC1_CHAIRMAN_URL = "http://192.168.1.100:5002"
PC2_COUNCIL_URL = "http://192.168.1.101:5001"
PORT = 5000
```

**If running frontend on PC1:**
```python
PC1_CHAIRMAN_URL = "http://localhost:5002"
PC2_COUNCIL_URL = "http://192.168.1.101:5001"
```

**If running frontend on PC2:**
```python
PC1_CHAIRMAN_URL = "http://192.168.1.100:5002"
PC2_COUNCIL_URL = "http://localhost:5001"
```

---

## Phase 5: Testing (10 min)

### Test PC2 Council Server

**On PC2, start the server:**
```bash
cd pc2_council
python council_server.py
```

You should see:
```
╔════════════════════════════════════════════╗
║   PC2 COUNCIL SERVER                       ║
║   Running on port 5001                     ║
╚════════════════════════════════════════════╝
```

**Test from PC2:**
```bash
curl http://localhost:5001/health
```

Should return JSON with status "healthy"

**Test from PC1 (or frontend PC):**
```bash
curl http://<PC2_IP>:5001/health
```

Should also return healthy status.

### Test PC1 Chairman Server

**On PC1, start the server:**
```bash
cd pc1_chairman
python chairman_server.py
```

You should see:
```
╔════════════════════════════════════════════╗
║   PC1 CHAIRMAN SERVER                      ║
║   Running on port 5002                     ║
╚════════════════════════════════════════════╝
```

**Test from PC1:**
```bash
curl http://localhost:5002/health
```

**Test from PC2 (or frontend PC):**
```bash
curl http://<PC1_IP>:5002/health
```

### Test Frontend

**On frontend PC, start the coordinator:**
```bash
cd frontend
python coordinator.py
```

You should see:
```
╔════════════════════════════════════════════════════════╗
║   LLM COUNCIL FRONTEND COORDINATOR                     ║
║   Running on port 5000                                 ║
╚════════════════════════════════════════════════════════╝
```

**Open browser:**
```
http://localhost:5000
```

You should see:
- Green status indicators for both PC1 and PC2
- The query input form

---

## Phase 6: Full End-to-End Test (5 min)

1. **Open the web interface:** `http://localhost:5000`

2. **Check status indicators:**
   - PC1 Chairman: ✓ Healthy (green)
   - PC2 Council: ✓ Healthy (green)

3. **Enter a test query:**
   ```
   What is the capital of France?
   ```

4. **Click "Submit to Council"**

5. **Wait for processing** (30-60 seconds)

6. **Verify all 3 stages appear:**
   - **Stage 1:** 3 different answers from council LLMs
   - **Stage 2:** 3 reviews
   - **Stage 3:** 1 final synthesized answer from Chairman

---

## Common Issues and Solutions

### Issue: "Model not found"
**Solution:**
```bash
ollama pull <model-name>
ollama list  # Verify
```

### Issue: "Connection refused"
**Solution:**
1. Check server is running
2. Check IP address is correct
3. Check firewall allows the port
4. Test with: `telnet <IP> <PORT>`

### Issue: Slow responses
**Expected:** 30-90 seconds is normal for the full workflow
**If slower:**
- Use smaller models (3b instead of 7b)
- Close other applications
- Check CPU/RAM usage

### Issue: Timeout errors
**Solution:**
Edit `frontend/coordinator.py`, increase timeout:
```python
# Lines 80, 106, 128
timeout=300  # Increase from 180 to 300
```

### Issue: Green status but query fails
**Solution:**
1. Check Ollama logs
2. Try manual curl test
3. Verify models are fully downloaded
4. Restart Ollama service

---

## Running Order (Important!)

Always start in this order:

1. **Start Ollama** (should auto-start, verify with `ollama list`)
2. **Start PC2 Council Server**
3. **Start PC1 Chairman Server**
4. **Start Frontend**

To stop, reverse the order.

---

## Demo Day Checklist

**Before the demo:**
- [ ] Both PCs on same network
- [ ] Ollama running on both PCs
- [ ] All models pulled and verified
- [ ] All servers started in correct order
- [ ] Frontend accessible and showing green status
- [ ] Test query completed successfully

**During the demo:**
- [ ] Show the web interface
- [ ] Explain the 2-PC architecture
- [ ] Submit a query
- [ ] Show Stage 1 (council answers)
- [ ] Show Stage 2 (reviews)
- [ ] Show Stage 3 (final synthesis)
- [ ] Mention improvements made
- [ ] Answer questions

**Backup plan:**
- Have a video recording of the system working
- Have screenshots of each stage
- Be prepared to explain architecture even if demo fails

---

## Quick Reference

### PC1 (Chairman)
- **IP:** [Write yours here]
- **Port:** 5002
- **Model:** llama3.2:3b
- **Start:** `python chairman_server.py`
- **Test:** `curl http://localhost:5002/health`

### PC2 (Council)
- **IP:** [Write yours here]
- **Port:** 5001
- **Models:** llama3.2:3b, mistral:7b, phi3:mini
- **Start:** `python council_server.py`
- **Test:** `curl http://localhost:5001/health`

### Frontend
- **Port:** 5000
- **Start:** `python coordinator.py`
- **Access:** `http://localhost:5000`

---

## Next Steps

1. **Test thoroughly** before demo day
2. **Document any issues** you encounter
3. **Add improvements** (optional):
   - Performance metrics
   - Better UI
   - More models
   - Caching
4. **Update README** with your team info
5. **Add AI usage statement** if you used any AI tools
6. **Practice the demo** presentation

---

## Support

If you run into issues:
1. Check the README files in each directory
2. Review server logs for error messages
3. Test each component individually
4. Verify network connectivity
5. Check Ollama is working: `ollama run llama3.2:3b "test"`

Good luck with your project!
