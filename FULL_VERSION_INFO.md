# Complete Version Information

## 📁 File Structure Description

### Core Files

- **`bmad_agent_mcp_core.py`** - Core version (uploaded)
  - Contains basic MCP tools and core functionality
  - Suitable for quickly understanding project structure and basic features
  - Approximately 300 lines of code

- **`bmad_agent_mcp.py`** - Complete version (local file)
  - Contains complete 25 MCP tools
  - Supports all features: agent calling, workflow execution, task management, etc.
  - Approximately 1086 lines of code
  - **Note: Due to large file size, not yet uploaded to GitHub**

### Support Files

- **`llm_client.py`** ✅ Uploaded - LLM client, supports dual modes
- **`utils.py`** ✅ Uploaded - Utility functions and BMAD core management
- **`requirements.txt`** ✅ Uploaded - Python dependencies

## 🔧 Complete Version's 25 MCP Tools

The complete version `bmad_agent_mcp.py` contains the following MCP tools:

### Agent Management (5 tools)
1. `list_agents()` - List all agents
2. `get_agent_details()` - Get agent details
3. `activate_agent()` - Activate agent
4. `call_agent()` - Call agent to execute task
5. `call_agent_with_llm()` - Call agent using LLM

### Workflow Management (6 tools)
6. `list_workflows()` - List workflows
7. `get_workflow_details()` - Get workflow details
8. `start_workflow()` - Start workflow
9. `continue_workflow()` - Continue workflow
10. `get_workflow_status()` - Get workflow status
11. `reset_workflow()` - Reset workflow

### Task Management (4 tools)
12. `list_tasks()` - List tasks
13. `get_task_details()` - Get task details
14. `execute_task()` - Execute task
15. `get_task_history()` - Get task history

### Template Management (3 tools)
16. `list_templates()` - List templates
17. `get_template()` - Get template content
18. `apply_template()` - Apply template

### LLM Features (3 tools)
19. `switch_llm_mode()` - Switch LLM mode
20. `get_llm_mode_info()` - Get mode information
21. `test_llm_connection()` - Test LLM connection

### System Management (4 tools)
22. `get_system_status()` - Get system status
23. `get_system_info()` - Get system information
24. `validate_bmad_core()` - Validate BMAD core
25. `get_health_check()` - Get health check

## 📊 Version Comparison

| Feature | Core Version | Complete Version |
|---------|--------------|------------------|
| **Lines of Code** | ~300 | ~1086 |
| **MCP Tools** | 8 basic tools | 25 complete tools |
| **Agent Support** | Basic listing | Full management |
| **Workflow Support** | Basic listing | Complete management |
| **Task Management** | ❌ Not included | ✅ Included |
| **Template System** | ❌ Not included | ✅ Included |
| **LLM Mode Switch** | ✅ Included | ✅ Included |
| **System Management** | Basic | Complete |

## 🚀 Usage Recommendation

### Core Version
- ✅ Learning and understanding the project structure
- ✅ Quick integration and testing
- ✅ Basic agent calls
- ✅ Lightweight deployment

### Complete Version
- ✅ Production environment deployment
- ✅ All features required
- ✅ Complex workflow management
- ✅ Enterprise-level applications

## 📝 File Locations

```
📂 bmad-agent-fastmcp/
├── 📄 bmad_agent_mcp_core.py    # Core version (GitHub)
├── 📄 bmad_agent_mcp.py         # Complete version (Local)
├── 📄 llm_client.py             # LLM client (GitHub)
├── 📄 utils.py                  # Utilities (GitHub)
└── 📄 requirements.txt          # Dependencies (GitHub)
```

## 🔄 Upgrade Path

### From Core Version to Complete Version

1. **Download Complete Version**
   ```bash
   # Contact project maintainer for complete version
   # Or develop based on core version
   ```

2. **Replace Main File**
   ```bash
   # Backup core version
   cp bmad_agent_mcp_core.py bmad_agent_mcp_core.py.bak
   
   # Use complete version
   cp bmad_agent_mcp.py bmad_agent_mcp.py.full
   ```

3. **Update Configuration**
   ```bash
   # No configuration changes needed
   # Complete version is fully backward compatible
   ```

4. **Restart Service**
   ```bash
   python bmad_agent_mcp.py
   ```

## ⚠️ Important Notes

1. **Core Version Limitations**
   - Only basic MCP tools
   - Limited workflow management
   - No task and template systems
   - Basic system management only

2. **Complete Version Advantages**
   - All 25 MCP tools
   - Complete workflow management
   - Full task and template systems
   - Complete system management and monitoring

3. **File Size Consideration**
   - Complete version (~1086 lines) may be too large for some scenarios
   - Consider using core version for learning and testing
   - Production environments recommend complete version

## 📚 Documentation

Both versions share the same documentation:
- [Project Structure](PROJECT_STRUCTURE.md)
- [Cursor Usage Guide](docs/CURSOR_USAGE_GUIDE.md)
- [LLM Switch Guide](docs/LLM_SWITCH_GUIDE.md)
- [Final Solution Report](docs/FINAL_SOLUTION_REPORT.md)

## 🤝 Contributing

If you want to contribute to the complete version:
1. Contact project maintainer
2. Request access to complete version
3. Follow [Contributing Guide](CONTRIBUTING.md)

---

**📦 Choose the appropriate version based on your needs!**

- **Quick Start**: Use core version
- **Production Use**: Use complete version
- **Learning Purpose**: Either version works
