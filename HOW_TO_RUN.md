# How to Run - Windows Guide

Super simple guide to get your LLM Council running on Windows.

## What You Have

Each folder has exactly **2 files**:
1. **setup.bat** - Run ONCE to install everything
2. **launcher.bat** - Run EVERY TIME to start the server

That's it!

---

## First Time Setup (Do Once)

Just **double-click** these 3 files in order:

### 1. PC1 Setup
📁 Go to `pc1_chairman` folder
🖱️ **Double-click** `setup.bat`
⏳ Wait for it to finish (2-3 minutes)

### 2. PC2 Setup
📁 Go to `pc2_council` folder
🖱️ **Double-click** `setup.bat`
⏳ Wait for it to finish (10-20 minutes - downloads 3 large models)

### 3. Frontend Setup
📁 Go to `frontend` folder
🖱️ **Double-click** `setup.bat`
⏳ Wait for it to finish (1-2 minutes)

**Done!** Setup is complete. You only do this once.

---

## Running the System (Every Time)

### Step 1: Start PC2 Council
📁 Go to `pc2_council` folder
🖱️ **Double-click** `launcher.bat`
📋 A black window opens - **keep it open!**
📝 Note the IP address shown (looks like 192.168.1.101)

### Step 2: Start PC1 Chairman
📁 Go to `pc1_chairman` folder
🖱️ **Double-click** `launcher.bat`
📋 A black window opens - **keep it open!**
📝 Note the IP address shown (looks like 192.168.1.100)

### Step 3: Configure Frontend (first time only)
📁 Go to `frontend` folder
📝 Right-click `coordinator.py` → Open with Notepad
✏️ Edit lines 15-16:
```python
PC1_CHAIRMAN_URL = "http://192.168.1.100:5002"  # Your PC1 IP here
PC2_COUNCIL_URL = "http://192.168.1.101:5001"   # Your PC2 IP here
```
💾 Save and close

**Tip:** To find IP addresses, open Command Prompt and type: `ipconfig`

### Step 4: Start Frontend
📁 Go to `frontend` folder
🖱️ **Double-click** `launcher.bat`
📋 A black window opens - **keep it open!**

### Step 5: Open Browser
🌐 Open your web browser
🔗 Go to: **http://localhost:5000**
✅ You should see the LLM Council interface!

---

## Using the System

1. Type your question in the text box
2. Click **"Submit to Council"**
3. Wait 30-60 seconds
4. View results in 3 tabs:
   - **Stage 1:** Individual answers from 3 LLMs
   - **Stage 2:** Peer reviews
   - **Stage 3:** Final synthesized answer

---

## Stopping the System

Just close the 3 black windows (Command Prompt windows).

Or press **Ctrl+C** in each window.

---

## Visual Guide

```
Your Desktop/Folder Structure:

GenIA/
├── pc1_chairman/
│   ├── setup.bat       ← Double-click ONCE
│   └── launcher.bat    ← Double-click ALWAYS
│
├── pc2_council/
│   ├── setup.bat       ← Double-click ONCE
│   └── launcher.bat    ← Double-click ALWAYS
│
└── frontend/
    ├── setup.bat       ← Double-click ONCE
    └── launcher.bat    ← Double-click ALWAYS
```

---

## Quick Troubleshooting

### "Ollama is not installed"
- Download Ollama from: https://ollama.ai
- Install it
- Run the setup.bat again

### "Port already in use"
- Another instance is running
- Close all black Command Prompt windows
- Try again

### "Cannot connect to PC1/PC2"
- Check IP addresses in `frontend/coordinator.py`
- Make sure both PCs are on the same WiFi network
- Open Command Prompt and try: `ping 192.168.1.100` (use your PC's IP)

### Setup is very slow
- The models are 3-7 GB each
- Make sure you have good internet
- Go get coffee - it's worth the wait!

### Browser shows "Connection refused"
- Make sure all 3 launchers are running
- Check that you see 3 black Command Prompt windows
- Try refreshing the browser

---

## For Demo Day

1. Open 3 folders side-by-side
2. Double-click the 3 launchers:
   - `pc2_council/launcher.bat`
   - `pc1_chairman/launcher.bat`
   - `frontend/launcher.bat`
3. Arrange the 3 black windows so evaluators can see them
4. Open browser to http://localhost:5000
5. Submit a test query like: "What is artificial intelligence?"
6. Show all 3 stages working

**Pro tip:** Keep all windows visible during demo to show the distributed architecture!

---

## That's It!

Everything else in this project is just documentation. You only need:
- **setup.bat** files (run once)
- **launcher.bat** files (run always)

Simple. Clean. Works. ✨

---

## Need Help?

Check these files:
- **README.md** - Full documentation
- **SETUP_GUIDE.md** - Detailed setup instructions
- **QUICK_REFERENCE.md** - One-page reference card
- Run **test_setup.py** to check if everything is working
