# Setup Guide

## Prerequisites

### 1. Docker Desktop
- Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Enable Docker MCP Toolkit:
  1. Open Docker Desktop Settings
  2. Go to "Beta features"
  3. Enable "Docker MCP Toolkit"
  4. Click "Apply"

### 2. Python 3.10+
```bash
python --version  # Should be 3.10 or higher
```

### 3. API Keys

#### E2B API Key
1. Sign up at [e2b.dev](https://e2b.dev)
2. Get your API key from [dashboard](https://e2b.dev/dashboard?tab=keys)

#### OpenAI API Key
1. Sign up at [OpenAI](https://platform.openai.com)
2. Get your API key from [API keys page](https://platform.openai.com/api-keys)

## Installation

### Step 1: Clone and Setup Python Environment

```bash
cd e2b-mcp-hackathon

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API keys
# E2B_API_KEY=your_e2b_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here
```

### Step 3: Enable Docker MCP Servers

```bash
# Enable GitHub MCP server
docker mcp server enable github-official

# Authenticate with GitHub
docker mcp oauth authorize github

# Enable Slack MCP server (optional)
docker mcp server enable slack

# Enable Playwright MCP server (optional)
docker mcp server enable playwright
```

### Step 4: Verify Installation

```bash
# Test MCP connection
python -m src.cli test-connection

# Should output:
# ✓ Connected to Docker MCP Gateway
# Available tools: X
```

## Quick Start

### Test E2B Sandbox

```bash
python examples/test_e2b.py
```

### Run Basic Scan

```bash
python examples/basic_scan.py
```

Edit the file to set your repository URL:
```python
repo_url = "owner/repo"  # e.g., "octocat/Hello-World"
```

### Run Full Pipeline

```bash
python examples/full_pipeline.py
```

### Use CLI

```bash
# Run pipeline
python -m src.cli pipeline owner/repo

# Test connection
python -m src.cli test-connection
```

## Troubleshooting

### Docker MCP Gateway Not Found

**Error:** `docker: 'mcp' is not a docker command.`

**Solution:** Make sure Docker MCP Toolkit is enabled in Docker Desktop settings.

### E2B API Key Error

**Error:** `E2B_API_KEY not found`

**Solution:** 
1. Check `.env` file exists
2. Verify API key is correct
3. Make sure `.env` is in the project root

### OpenAI API Error

**Error:** `Invalid API key`

**Solution:**
1. Verify OpenAI API key in `.env`
2. Check you have credits in your OpenAI account

### MCP Connection Timeout

**Error:** Connection timeout or no response

**Solution:**
1. Ensure Docker Desktop is running
2. Restart Docker Desktop
3. Re-enable MCP servers

## Project Structure

```
e2b-mcp-hackathon/
├── src/
│   ├── core/           # Orchestrator and config
│   ├── mcp/            # MCP client (GitHub, Slack)
│   ├── vulnerability/  # Vulnerability scanner
│   ├── patch/          # AI patch generator
│   ├── sandbox/        # E2B sandbox manager
│   └── utils/          # Logger and utilities
├── examples/           # Example scripts
├── docs/              # Documentation
├── .env               # Your API keys (create from .env.example)
├── requirements.txt   # Python dependencies
└── README.md          # Main documentation
```

## Next Steps

1. Read [PROGRESS.md](PROGRESS.md) for implementation details
2. Check [docs/architecture.md](docs/architecture.md) for system design
3. Review [docs/features.md](docs/features.md) for capabilities
4. See [docs/plan.md](docs/plan.md) for project vision
