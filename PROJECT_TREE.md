# Project Structure

```
e2b-mcp-hackathon/
│
├── 📄 README.md                      # Main documentation
├── 📄 SETUP.md                       # Setup instructions
├── 📄 PROGRESS.md                    # Implementation progress tracker
├── 📄 IMPLEMENTATION_SUMMARY.md      # Complete implementation overview
├── 📄 PROJECT_TREE.md                # This file
│
├── 📦 requirements.txt               # Python dependencies
├── 📦 pyproject.toml                 # Project metadata
├── 🔒 .env.example                   # Environment template
├── 🔒 .gitignore                     # Git ignore rules
│
├── 📁 src/                           # Source code
│   ├── __init__.py
│   ├── cli.py                        # CLI interface
│   │
│   ├── 📁 core/                      # Core orchestration
│   │   ├── __init__.py
│   │   ├── config.py                 # Configuration management
│   │   └── orchestrator.py           # Main pipeline orchestrator
│   │
│   ├── 📁 mcp/                       # MCP client implementations
│   │   ├── __init__.py
│   │   ├── client.py                 # Base MCP client (Docker gateway)
│   │   ├── github.py                 # GitHub operations via MCP
│   │   └── slack.py                  # Slack notifications via MCP
│   │
│   ├── 📁 vulnerability/             # Vulnerability detection
│   │   ├── __init__.py
│   │   └── scanner.py                # Dependency vulnerability scanner
│   │
│   ├── 📁 patch/                     # Patch generation
│   │   ├── __init__.py
│   │   └── generator.py              # AI-powered patch generator (OpenAI)
│   │
│   ├── 📁 sandbox/                   # E2B sandbox management
│   │   ├── __init__.py
│   │   └── manager.py                # E2B sandbox lifecycle manager
│   │
│   └── 📁 utils/                     # Utilities
│       ├── __init__.py
│       └── logger.py                 # Rich logging setup
│
├── 📁 examples/                      # Example scripts
│   ├── basic_scan.py                 # Simple vulnerability scan
│   ├── full_pipeline.py              # Complete pipeline demo
│   └── test_e2b.py                   # E2B sandbox test
│
└── 📁 docs/                          # Documentation
    ├── architecture.md               # System architecture
    ├── features.md                   # Feature list
    └── plan.md                       # Original project plan
```

## File Count Summary

- **Python Files**: 20
- **Documentation Files**: 8
- **Configuration Files**: 4
- **Total Files**: 32+

## Lines of Code

| Component | Files | Approx. Lines |
|-----------|-------|---------------|
| Core | 2 | 250 |
| MCP Client | 3 | 200 |
| Vulnerability | 1 | 100 |
| Patch Generation | 1 | 120 |
| Sandbox | 1 | 120 |
| Utils | 1 | 30 |
| CLI | 1 | 70 |
| Examples | 3 | 150 |
| **Total** | **13** | **~1040** |

## Key Files

### Entry Points
- `src/cli.py` - Command-line interface
- `examples/full_pipeline.py` - Complete demo
- `examples/basic_scan.py` - Simple scan demo

### Core Logic
- `src/core/orchestrator.py` - Main pipeline
- `src/mcp/client.py` - MCP gateway connection
- `src/sandbox/manager.py` - E2B integration

### Configuration
- `.env.example` - Environment template
- `src/core/config.py` - Settings management
- `requirements.txt` - Dependencies

### Documentation
- `README.md` - Overview and quick start
- `SETUP.md` - Detailed setup guide
- `IMPLEMENTATION_SUMMARY.md` - Complete summary
- `docs/architecture.md` - Technical architecture
