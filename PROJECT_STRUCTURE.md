# 📁 BMAD Agent FastMCP Project Structure

## 🎯 Project Overview

BMAD Agent FastMCP Service is an agent calling service based on the FastMCP framework, supporting dual LLM modes (Cursor built-in LLM + DeepSeek API), providing 25 professional MCP tools and 10 professional agents.

## 📂 Directory Structure

```
bmad-agent-fastmcp/
├── 📁 .bmad-core/                    # Core data directory (do not modify)
│   ├── agents/                       # 10 agent configurations
│   ├── workflows/                    # 6 workflows
│   ├── tasks/                        # 19 task definitions
│   └── templates/                    # 11 template files
│
├── 📄 bmad_agent_mcp.py             # 🔒 Main service file (25 MCP tools)
├── 📄 llm_client.py                 # 🔒 LLM client (dual mode support)
├── 📄 utils.py                      # 🔒 Utility functions
├── 📄 requirements.txt              # 🔒 Python dependencies
├── 📄 .env                          # 🔒 Environment variable configuration
│
├── 📁 docs/                         # 📚 Documentation and guides
├── 📁 tests/                        # 🧪 Test files
├── 📁 logs/                         # 📋 Log files
├── 📁 archive/                      # 📦 Archived files
└── 📁 __pycache__/                  # 🔒 Python cache
```

## 🔒 Core Files (Important, do not move)

### Main Files

| File | Description | Importance |
|------|------|--------|
| `bmad_agent_mcp.py` | Main service file containing 25 MCP tools | ⭐⭐⭐⭐⭐ |
| `llm_client.py` | LLM client supporting dual mode switching | ⭐⭐⭐⭐⭐ |
| `utils.py` | Core utility functions and BMADCore class | ⭐⭐⭐⭐⭐ |
| `requirements.txt` | Python dependency package list | ⭐⭐⭐⭐ |
| `.env` | Environment variable configuration | ⭐⭐⭐⭐ |

### Data Directories

| Directory | Description | File Count |
|------|------|----------|
| `.bmad-core/agents/` | Agent configuration files | 10 |
| `.bmad-core/workflows/` | Workflow definitions | 6 |
| `.bmad-core/tasks/` | Task configurations | 19 |
| `.bmad-core/templates/` | Document templates | 11 |

## 🚀 Quick Start

### 1. Core File Check
```bash
# Ensure core files exist
ls bmad_agent_mcp.py llm_client.py utils.py requirements.txt
```

### 2. Environment Configuration
```bash
# Install dependencies
pip install -r requirements.txt

# Check environment variables
cat .env
```

### 3. Start Service
```bash
# Run main service directly
python bmad_agent_mcp.py
```

### 4. Cursor Integration
Refer to `docs/CURSOR_USAGE_GUIDE.md` for Cursor IDE integration configuration.

## 🔧 Maintenance Guide

### Important File Protection

**🚨 Never modify or delete:**
- `bmad_agent_mcp.py` - Main service file
- `llm_client.py` - LLM client
- `utils.py` - Core utilities
- `.bmad-core/` - Data directory
- `requirements.txt` - Dependencies file

### Safe Modifications

**✅ Can be safely modified:**
- `.env` - Environment variables (modify with caution)
- Files in `docs/` directory
- Files in `tests/` directory
- Files in `archive/` directory

### Adding New Features

1. **New MCP Tools**: Add in `bmad_agent_mcp.py`
2. **New Agents**: Add configuration file in `.bmad-core/agents/`
3. **New Workflows**: Add definition in `.bmad-core/workflows/`
4. **New Documentation**: Add in `docs/` directory

## 📊 Project Statistics

- **Total Files**: Approximately 60+ files
- **Core Files**: 5 key files
- **MCP Tools**: 25 professional tools
- **Agents**: 10 professional roles
- **Workflows**: 6 complete workflows
- **Supported Modes**: Dual LLM modes

## 🎯 Usage Recommendations

1. **Daily Development**: Focus on core files in root directory
2. **View Documentation**: Visit `docs/` directory
3. **Run Tests**: Visit `tests/` directory
4. **Debug Issues**: Check `logs/` directory
5. **Historical Reference**: Check `archive/` directory

## 🔄 Version Management

It is recommended to use Git to manage the project, focusing on tracking:
- All core files
- `.bmad-core/` directory
- Important documents in `docs/` directory
- Configuration files

**Ignore files**:
- `__pycache__/`
- `*.log`
- Temporary test files

---

**📝 Note**: This project structure has been carefully designed to ensure the stability of core functions and code maintainability. Please follow the above guidelines for development and maintenance.
