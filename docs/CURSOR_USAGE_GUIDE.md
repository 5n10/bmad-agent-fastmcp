# Using BMAD Agent FastMCP Service in Cursor

## 🎯 Dual Mode Support

BMAD Agent now supports two LLM modes:

### 🔧 Built-in LLM Mode (Recommended)
- ✅ **Uses Cursor Built-in LLM**: Directly leverages Cursor IDE's LLM capabilities
- ✅ **No External API Needed**: No network connection or API fees required
- ✅ **Faster Response**: Instant response, no network latency
- ✅ **Deep Integration**: Perfect integration with Cursor
- 🔧 **How it Works**: Agent tools return role prompts, letting Cursor LLM play professional roles

### 🌐 External API Mode (Alternative)
- ✅ **DeepSeek API**: Uses dedicated LLM model
- ✅ **Independent Service**: Doesn't depend on IDE's LLM capabilities
- ⚠️ **Requires Network**: Needs API Key and network connection
- 🔧 **How it Works**: Directly calls external API to get agent responses

## 🔄 Mode Switching

### Quick Switch
```bash
# Switch to built-in LLM mode (recommended)
python switch_llm_mode.py --builtin

# Switch to external API mode
python switch_llm_mode.py --external

# View current mode information
python switch_llm_mode.py --info
```

### Environment Variable Control
```bash
# Set to use built-in LLM
set USE_BUILTIN_LLM=true

# Set to use external API
set USE_BUILTIN_LLM=false
```

## 🚀 Quick Start

### 1. Start FastMCP Service

Run in Cursor's terminal:

```bash
# Ensure you're in the project directory
cd D:\234ffff

# Start service (built-in LLM mode)
python bmad_agent_mcp.py
```

### 2. Configure Cursor MCP

Add MCP server configuration in Cursor settings:

**Method 1: Use Configuration Script (Recommended)**
```bash
python setup_cursor_mcp.py
```

**Method 2: Manual Configuration**

Open Cursor Settings → MCP Servers, add the following configuration:

```json
{
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
```

### 3. Restart Cursor

After configuration is complete, restart Cursor IDE to make the MCP configuration effective.

## 🎯 Usage Examples

### Basic Usage

When talking with AI in Cursor, you can directly use BMAD agents:

```
User: "Please list all available BMAD agents"
AI: Calls list_agents() tool
Returns: Detailed list of 10 professional agents

User: "Use Product Manager to analyze e-commerce platform requirements"
AI: Calls call_agent_with_llm('pm', 'Analyze e-commerce platform requirements') tool
Returns: Professional product requirement analysis
```

### Workflow Usage

```
User: "Start full-stack development workflow"
AI: Calls start_workflow('greenfield-fullstack') tool
Returns: Workflow started, showing current step

User: "Advance to next step"
AI: Calls advance_workflow_step() tool
Returns: Workflow advanced to next step
```

### LLM Mode Switching

```
User: "Switch to DeepSeek API mode"
AI: Calls switch_llm_mode('external') tool
Returns: Switched to external API mode

User: "View current LLM mode information"
AI: Calls get_llm_mode_info() tool
Returns: Current mode detailed information
```

## 🔧 Advanced Configuration

### Environment Variable Configuration

Create `.env` file:

```bash
# LLM mode configuration
USE_BUILTIN_LLM=true

# DeepSeek API configuration (optional)
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Character encoding configuration
PYTHONIOENCODING=utf-8
PYTHONUNBUFFERED=1

# Log configuration
LOG_LEVEL=INFO
LOG_FILE=logs/bmad_agent.log
```

### Cursor Settings Optimization

Add in Cursor's `settings.json`:

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
  },
  "mcp.timeout": 30000,
  "mcp.retries": 3
}
```

## 🐛 Troubleshooting

### Common Issues

**1. Cannot Find Agents**
```bash
# Check service status
python bmad_agent_mcp.py --test

# Verify .bmad-core directory
python validate_bmad_core.py
```

**2. Encoding Issues**
```bash
# Set correct encoding
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
```

**3. Path Issues**
```bash
# Check Python path
echo %PYTHONPATH%

# Set correct path
set PYTHONPATH=D:\234ffff
```

### Debug Mode

Enable detailed logging:

```bash
# Start debug mode
python bmad_agent_mcp.py --debug

# View logs
type logs\bmad_agent.log
```

### Test Connection

```bash
# Test MCP connection
python test_mcp_connection.py

# Test agent functionality
python test_agent_functionality.py

# Test LLM integration
python test_llm_integration.py
```

## 📊 Performance Optimization

### Built-in LLM Mode Optimization

- ✅ **Fast Response**: Average response time < 1 second
- ✅ **Low Resource Usage**: Memory usage < 100MB
- ✅ **High Concurrency Support**: Supports multiple concurrent requests

### External API Mode Optimization

- 🔧 **Connection Pool**: Reuse HTTP connections
- 🔧 **Caching Mechanism**: Cache common responses
- 🔧 **Retry Mechanism**: Automatically retry failed requests

## 🎯 Best Practices

### 1. Mode Selection

- **Daily Development**: Use built-in LLM mode
- **Complex Analysis**: Can switch to external API mode
- **Team Collaboration**: Unified use of built-in mode

### 2. Workflows

- **New Project**: Use greenfield workflow
- **Existing Project**: Use brownfield workflow
- **Specific Needs**: Select corresponding professional agent

### 3. Performance Optimization

- **Batch Operations**: Use workflows rather than individual agents
- **Cache Utilization**: Reuse same agent configurations
- **Resource Management**: Regularly clean logs and cache

## 🔗 Related Links

- [Project Structure](../PROJECT_STRUCTURE.md)
- [LLM Switch Guide](LLM_SWITCH_GUIDE.md)
- [Final Solution](FINAL_SOLUTION_REPORT.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

---

**🎉 Enjoy the powerful features of BMAD Agent FastMCP Service in Cursor!**
