# 🚀 Getting Started - AI DevSecOps Pipeline Orchestrator

## Welcome!

This guide will get you up and running in **10 minutes**.

---

## 📋 Prerequisites Checklist

Before you begin, make sure you have:

- [ ] **Docker Desktop** installed and running
- [ ] **Python 3.10+** installed
- [ ] **E2B API Key** ([Get it here](https://e2b.dev/dashboard?tab=keys))
- [ ] **OpenAI API Key** ([Get it here](https://platform.openai.com/api-keys))
- [ ] **GitHub account** (for MCP OAuth)

---

## ⚡ Quick Setup (10 minutes)

### Step 1: Enable Docker MCP Toolkit (2 min)

1. Open **Docker Desktop**
2. Go to **Settings** → **Beta features**
3. Enable **"Docker MCP Toolkit"**
4. Click **Apply & Restart**

### Step 2: Install Python Dependencies (2 min)

```bash
# Navigate to project directory
cd e2b-mcp-hackathon

# Create virtual environment (recommended)
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment (1 min)

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your favorite editor
```

Add your keys:
```bash
E2B_API_KEY=your_e2b_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 4: Enable Docker MCP Servers (3 min)

```bash
# Enable GitHub MCP server
docker mcp server enable github-official

# Authenticate with GitHub (opens browser)
docker mcp oauth authorize github

# Optional: Enable Slack (if you want notifications)
docker mcp server enable slack
```

### Step 5: Verify Installation (2 min)

```bash
# Test MCP connection
python -m src.cli test-connection
```

**Expected output:**
```
✓ Connected to Docker MCP Gateway
Available tools: 15+
  • github_read_file
  • github_create_pull_request
  • slack_post_message
  ...
```

If you see this, you're ready! 🎉

---

## 🎮 Try It Out

### Test 1: E2B Sandbox

```bash
python examples/test_e2b.py
```

This will:
- Create an isolated E2B sandbox
- Install a Python package
- Run test code
- Clean up automatically

### Test 2: Vulnerability Scan

```bash
# Edit examples/basic_scan.py first
# Change: repo_url = "owner/repo"  # Use any public repo

python examples/basic_scan.py
```

This will:
- Connect to GitHub via MCP
- Read requirements.txt
- Scan for vulnerabilities
- Display results

### Test 3: Full Pipeline

```bash
python examples/full_pipeline.py
```

This will:
- Scan repository for vulnerabilities
- Generate AI-powered patches
- Test patches in E2B sandbox
- Simulate PR creation
- Send notifications (if Slack configured)

---

## 📚 What to Read Next

### For Quick Demo
→ **[DEMO_GUIDE.md](DEMO_GUIDE.md)** - Step-by-step demo script

### For Understanding
→ **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical overview  
→ **[docs/architecture.md](docs/architecture.md)** - System architecture

### For Development
→ **[PROGRESS.md](PROGRESS.md)** - Implementation details  
→ **[PROJECT_TREE.md](PROJECT_TREE.md)** - File structure

---

## 🔧 Troubleshooting

### "docker: 'mcp' is not a docker command"

**Solution:** Docker MCP Toolkit not enabled
1. Open Docker Desktop Settings
2. Go to Beta features
3. Enable Docker MCP Toolkit
4. Restart Docker Desktop

### "E2B_API_KEY not found"

**Solution:** Environment not configured
1. Check `.env` file exists in project root
2. Verify it contains `E2B_API_KEY=...`
3. Make sure you're in the right directory

### "Invalid OpenAI API key"

**Solution:** Check your API key
1. Verify key in `.env` file
2. Check you have credits at [OpenAI Usage](https://platform.openai.com/usage)
3. Try regenerating the key

### "Connection timeout" or "No response"

**Solution:** Docker MCP Gateway not running
1. Ensure Docker Desktop is running
2. Try: `docker mcp server list`
3. Re-enable servers if needed

### Import errors

**Solution:** Dependencies not installed
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 💡 Usage Examples

### CLI Commands

```bash
# Test connection
python -m src.cli test-connection

# Run pipeline on a repository
python -m src.cli pipeline owner/repo
```

### Python API

```python
import asyncio
from src.core.orchestrator import DevSecOpsOrchestrator

async def main():
    orchestrator = DevSecOpsOrchestrator()
    result = await orchestrator.run_pipeline("owner/repo")
    print(f"Found {result.vulnerabilities_found} vulnerabilities")
    print(f"Generated {result.patches_generated} patches")
    print(f"Passed {result.tests_passed} tests")

asyncio.run(main())
```

---

## 🎯 Next Steps

1. ✅ **Run the examples** to see it in action
2. 📖 **Read the documentation** to understand the architecture
3. 🔧 **Customize** for your use case
4. 🚀 **Deploy** to your infrastructure

---

## 🆘 Need Help?

- **Documentation**: Check the `docs/` folder
- **Examples**: See `examples/` for working code
- **Issues**: Review troubleshooting section above

---

## 🎉 You're Ready!

Your AI DevSecOps Pipeline Orchestrator is set up and ready to use.

**Quick test:**
```bash
python examples/test_e2b.py
```

If that works, you're all set! 🚀

---

**Happy automating!** 🤖
