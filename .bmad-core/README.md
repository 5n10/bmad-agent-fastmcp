# BMAD Core Configuration

This directory contains the core configuration files for the BMAD (Business Model and Architecture Development) system.

## 📁 Directory Structure

- **`agents/`** - Agent definition files (10 professional agents)
- **`workflows/`** - Workflow configurations (6 complete workflows)
- **`tasks/`** - Task definition files (19 task configurations)
- **`templates/`** - Document templates (11 professional templates)
- **`checklists/`** - Checklists
- **`utils/`** - Tools and utilities
- **`data/`** - Knowledge base and technology preferences
- **`agent-teams/`** - Agent team configurations

## 🤖 Agent List

1. **pm** 📋 - Product Manager
2. **analyst** 📊 - Business Analyst
3. **architect** 🏗️ - System Architect
4. **dev** 💻 - Development Engineer
5. **qa** 🧪 - Quality Assurance Engineer
6. **ux-expert** 🎨 - User Experience Expert
7. **po** 📝 - Product Owner
8. **sm** 🏃 - Scrum Master
9. **bmad-master** 🎯 - BMAD Master
10. **bmad-orchestrator** 🎼 - BMAD Orchestrator

## 🔄 Workflow Types

1. **greenfield-fullstack** - Full-stack new project
2. **greenfield-service** - Backend new project
3. **greenfield-ui** - Frontend new project
4. **brownfield-fullstack** - Full-stack existing project
5. **brownfield-service** - Backend existing project
6. **brownfield-ui** - Frontend existing project

## 📋 Core Tasks

- Requirements analysis and document creation
- Architecture design and technology selection
- Project planning and workflow management
- Code generation and quality assurance
- User experience design and optimization

## 📄 Document Templates

- PRD (Product Requirements Document)
- Architecture design document
- Technical specification document
- Project brief template
- Competitive analysis template
- Market research template
- User story template

## 🚀 Usage

Call these configurations through BMAD Agent FastMCP Service:

```python
# List all agents
result = list_agents()

# Activate Product Manager
result = activate_agent("pm")

# Call agent to execute task
result = call_agent("pm", "Create product requirements document")

# Start workflow
result = start_workflow("greenfield-fullstack", "web-app")
```

## 📚 More Information

For detailed usage guides, refer to the documentation in the project root directory:
- `README.md` - Project overview
- `docs/CURSOR_USAGE_GUIDE.md` - Cursor IDE usage guide
- `docs/LLM_SWITCH_GUIDE.md` - LLM mode switching guide
- `FULL_VERSION_INFO.md` - Complete version information
