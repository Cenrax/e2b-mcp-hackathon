# AI DevSecOps Pipeline Orchestrator

An intelligent DevSecOps orchestrator that combines E2B sandboxes with Docker MCP servers to create a self-healing, security-first CI/CD pipeline.

> **New here?** Start with **[GETTING_STARTED.md](GETTING_STARTED.md)** for a 10-minute setup guide!  
> **Looking for docs?** See **[INDEX.md](INDEX.md)** for complete documentation index.

## Features

- **Automated Vulnerability Detection**: Scans repositories for security issues
- **AI-Powered Patch Generation**: Uses OpenAI GPT-4 to generate fixes
- **Isolated Testing**: Tests patches in secure E2B sandboxes
- **Automated PR Creation**: Creates pull requests via GitHub MCP
- **Team Notifications**: Sends alerts via Slack MCP

## Architecture

```
Python MCP Client → Docker MCP Gateway → [GitHub, Slack, Playwright]
                  ↓
              [OpenAI API, E2B Sandboxes]
```

## Prerequisites

1. **Docker Desktop** with MCP Toolkit enabled
2. **Python 3.10+**
3. **API Keys**:
   - E2B API key ([get here](https://e2b.dev/dashboard))
   - OpenAI API key ([get here](https://platform.openai.com/api-keys))

## Setup

### 1. Enable Docker MCP Servers

```bash
# Enable required MCP servers
docker mcp server enable github-official
docker mcp server enable slack
docker mcp server enable playwright

# Authenticate GitHub
docker mcp oauth authorize github
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Usage

### Quick Start

```python
from src.orchestrator import DevSecOpsOrchestrator

async def main():
    orchestrator = DevSecOpsOrchestrator()
    await orchestrator.run_pipeline("https://github.com/user/repo")

asyncio.run(main())
```

### CLI

```bash
# Scan a repository
devsecops scan https://github.com/user/repo

# Run full pipeline
devsecops pipeline https://github.com/user/repo
```

## Project Structure

```
src/
├── core/           # Core orchestration logic
├── mcp/            # MCP client implementation
├── vulnerability/  # Vulnerability detection
├── patch/          # Patch generation
├── sandbox/        # E2B sandbox management
└── utils/          # Utilities
```

## Development

See [PROGRESS.md](PROGRESS.md) for implementation status.

## Documentation

- **[SETUP.md](SETUP.md)** - Complete setup instructions
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Implementation details
- **[PROGRESS.md](PROGRESS.md)** - Development progress
- **[PROJECT_TREE.md](PROJECT_TREE.md)** - Project structure
- **[docs/architecture.md](docs/architecture.md)** - Technical architecture
- **[docs/features.md](docs/features.md)** - Feature list
- **[docs/plan.md](docs/plan.md)** - Original project plan

## Key Features Implemented

- MCP client connecting to Docker MCP Gateway  
- GitHub integration via pre-built MCP server  
- Slack notifications via pre-built MCP server  
- Vulnerability scanning for Python dependencies  
- AI-powered patch generation with OpenAI GPT-4  
- Isolated testing in E2B sandboxes  
- Complete pipeline orchestration  
- CLI interface with rich output  
- Example scripts and documentation  

## Tech Stack

| Component | Technology |
|-----------|-----------|
| MCP Client | Python MCP SDK |
| GitHub Integration | Docker MCP (github-official) |
| Slack Integration | Docker MCP (slack) |
| AI Patch Generation | OpenAI GPT-4 |
| Sandbox Testing | E2B Code Interpreter |
| CLI Framework | Click + Rich |
| Configuration | Pydantic Settings |


## License

MIT
