# 🎯 BMAD Agent FastMCP Service

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-Compatible-green.svg)](https://github.com/jlowin/fastmcp)
[![Cursor IDE](https://img.shields.io/badge/Cursor-IDE-purple.svg)](https://cursor.sh/)

## 🎯 BMAD Methodology

This project is built upon the [BMAD-METHOD](https://github.com/bmadcode/BMAD-METHOD), a powerful business model and architecture development methodology.

### 🚀 Important: Keep Your BMad Installation Updated 

Stay up-to-date effortlessly! If you already have BMad-METHOD installed in your project, simply run:

```bash
npx bmad-method install
# OR
git pull
npm run install:bmad
```

### 📦 First Time Installation

If you're new to BMAD-METHOD, visit the official repository for complete installation and setup instructions:

👉 **[BMAD-METHOD Official Repository](https://github.com/bmadcode/BMAD-METHOD)**

The BMAD-METHOD provides:
- 🎯 Structured business analysis frameworks
- 🏗️ Architecture design patterns
- 📋 Project management templates
- 🔄 Workflow automation tools
- 📊 Quality assurance checklists

---

> 🚀 **Enterprise-grade Intelligence Service** - Professional AI agent service based on FastMCP framework, supports dual LLM modes, provides 25+ professional MCP tools and 10 professional agents, seamlessly integrated with Cursor IDE.

## 🌟 Core Features

- **🎯 10 Professional Agents**: Business Analyst, Architect, Full-stack Developer, Product Manager, QA Engineer, etc.
- **🔧 25+ MCP Tools**: Agent management, workflow control, task execution, etc.
- **🔄 Dual LLM Mode**: Supports dynamic switching between Cursor built-in LLM and DeepSeek API
- **📋 6 Workflows**: Full-stack development, API development, data analysis, and other complete workflows
- **🎯 Plug and Play**: Seamless integration with Cursor IDE

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy environment variable template
cp .env.example .env

# Edit environment variables (optional)
# USE_BUILTIN_LLM=true          # Use built-in LLM (default)
# DEEPSEEK_API_KEY=your_key     # DeepSeek API Key (optional)
```

### 3. Start Service
```bash
python bmad_agent_mcp.py
```

### 4. Cursor Integration
Refer to `docs/CURSOR_USAGE_GUIDE.md` for Cursor IDE integration configuration.

## ⚡ Key Features

- **🎯 10 Professional Agents**: Business Analyst, Architect, Developer, Product Manager, etc.
- **🔧 25 MCP Tools**: Agent management, workflow control, task execution, template processing
- **🔄 Dual LLM Mode**: Supports dynamic switching between Cursor built-in LLM and DeepSeek API
- **📋 6 Workflows**: Full-stack development, API development, data analysis, and other complete workflows
- **🎯 Plug and Play**: Seamless integration with Cursor IDE

## 🔄 LLM Mode Switching

### Built-in LLM Mode (Default)
- ✅ Uses Cursor IDE built-in LLM
- ✅ No external API calls required
- ✅ Faster response, no network latency
- ✅ No API fees

### External API Mode
- ✅ Uses DeepSeek API
- ✅ Stronger reasoning capabilities
- ✅ Supports more complex tasks
- ⚠️ Requires API Key and network connection

### Switching Method
```python
# Use in Cursor
switch_llm_mode('builtin')   # Switch to built-in mode
switch_llm_mode('external')  # Switch to external mode
get_llm_mode_info()          # View mode information
```

## 🛠️ Main MCP Tools

### Agent Management
- `list_agents()` - List all agents
- `get_agent_details(agent_id)` - Get agent details
- `activate_agent(agent_id)` - Activate agent
- `call_agent_with_llm(agent_id, task)` - Call agent to execute task

### Workflows
- `list_workflows()` - List all workflows
- `start_workflow(workflow_id)` - Start workflow
- `get_workflow_status()` - Get workflow status
- `advance_workflow_step()` - Advance workflow step

### LLM Features
- `switch_llm_mode(mode)` - Switch LLM mode
- `get_llm_mode_info()` - Get mode information
- `get_system_status()` - Get system status

### Tasks and Templates
- `list_tasks()` - List all tasks
- `execute_task(task_id)` - Execute task
- `list_templates()` - List all templates
- `get_template(template_name)` - Get template content

## 📊 Project Structure

```
📂 Root Directory
├── 📄 bmad_agent_mcp.py      # Main service file
├── 📄 llm_client.py          # LLM client
├── 📄 utils.py               # Utility functions
├── 📄 requirements.txt       # Dependencies
├── 📂 .bmad-core/            # Core data structures
├── 📁 docs/                  # Documentation directory
├── 📁 tests/                 # Test directory
└── 📁 archive/               # Archive directory
```

## 📚 Documentation

- **📖 [Project Structure](PROJECT_STRUCTURE.md)** - Detailed project structure and file descriptions
- **🔄 [LLM Switch Guide](docs/LLM_SWITCH_GUIDE.md)** - Detailed guide for LLM mode switching
- **🎯 [Cursor Usage Guide](docs/CURSOR_USAGE_GUIDE.md)** - Cursor IDE integration guide
- **📝 [Final Solution Report](docs/FINAL_SOLUTION_REPORT.md)** - Complete solution report

## 🧪 Testing

```bash
# Run basic tests
python tests/simple_test.py

# Test MCP tools
python tests/simple_mcp_test.py

# Test LLM functionality
python tests/quick_llm_test.py
```

## 🔧 Configuration

### Cursor IDE Configuration
Add the following configuration to Cursor's `settings.json`:

```json
{
  "mcpServers": {
    "bmad-agent": {
      "command": "python",
      "args": ["D:\\234ffff\\bmad_agent_mcp.py"],
      "cwd": "D:\\234ffff",
      "env": {
        "PYTHONPATH": "D:\\234ffff",
        "USE_BUILTIN_LLM": "true",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### Environment Variables
```bash
USE_BUILTIN_LLM=true                    # Use built-in LLM
DEEPSEEK_API_KEY=your_key_here          # DeepSeek API Key (optional)
PYTHONIOENCODING=utf-8                  # Character encoding
```

## 🎯 Usage Examples

### Using in Cursor

```
User: "Please list all available BMAD agents"
AI: Calls list_agents()
Returns: List of 10 professional agents

User: "Please use Business Analyst to analyze e-commerce platform requirements"
AI: Calls call_agent_with_llm('analyst', 'Analyze e-commerce platform requirements')
Returns: Professional business analysis results

User: "Please switch to DeepSeek API mode"
AI: Calls switch_llm_mode('external')
Returns: Switched to external API mode
```

## 🤝 Contributing

1. Fork the project
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License

## 📚 Related

- 📖 View detailed documentation in the `docs/` directory
- 🧪 Run test files in the `tests/` directory
- 📋 View log files in the `logs/` directory
- 📦 View historical files in the `archive/` directory

---

**🎉 Enjoy using BMAD Agent FastMCP Service!**