# LLM Mode Switching Detailed Guide

## 🎯 Overview

BMAD Agent FastMCP Service supports two LLM modes that can be dynamically switched as needed:

1. **Built-in LLM Mode**: Uses Cursor IDE's built-in LLM
2. **External API Mode**: Uses DeepSeek API

## 🔄 Mode Comparison

| Feature | Built-in LLM Mode | External API Mode |
|------|---------------|---------------|
| **Response Speed** | ⚡ Extremely Fast | 🐌 Slower (network latency) |
| **Cost** | 🆓 Free | 💰 Pay per use |
| **Network Requirements** | ❌ No network needed | ✅ Requires network connection |
| **API Key** | ❌ Not required | ✅ Requires DeepSeek API Key |
| **Reasoning Ability** | 🔧 Depends on Cursor LLM | 🚀 DeepSeek professional capabilities |
| **Integration** | 🎯 Deep integration with Cursor | 🔌 Independent service |

## 🛠️ Switching Methods

### Method 1: Use MCP Tools (Recommended)

Chat directly with AI in Cursor:

```
User: "Switch to built-in LLM mode"
AI: Calls switch_llm_mode('builtin')
Returns: Switched to built-in LLM mode

User: "Switch to external API mode"
AI: Calls switch_llm_mode('external')
Returns: Switched to external API mode

User: "View current LLM mode"
AI: Calls get_llm_mode_info()
Returns: Current mode detailed information
```

### Method 2: Environment Variables

```bash
# Switch to built-in LLM mode
set USE_BUILTIN_LLM=true

# Switch to external API mode
set USE_BUILTIN_LLM=false

# Restart service for configuration to take effect
python bmad_agent_mcp.py
```

### Method 3: Configuration File

Edit `.env` file:

```bash
# Built-in LLM mode
USE_BUILTIN_LLM=true

# External API mode
USE_BUILTIN_LLM=false
DEEPSEEK_API_KEY=your_api_key_here
```

### Method 4: Command Line Script

```bash
# Use switching script
python switch_llm_mode.py --builtin    # Switch to built-in mode
python switch_llm_mode.py --external   # Switch to external mode
python switch_llm_mode.py --info       # View current mode
```

## 🔧 Built-in LLM Mode Details

### How It Works

1. **Agent Activation**: Returns professional role prompts to Cursor
2. **Role Playing**: Cursor LLM plays professional role based on prompts
3. **Task Execution**: Completes user tasks in professional capacity
4. **Result Return**: Displays results directly in Cursor

### Advantages

- ✅ **Zero Latency**: No network requests, instant response
- ✅ **Zero Cost**: No API call fees
- ✅ **Deep Integration**: Perfect integration with Cursor workflow
- ✅ **Offline Work**: No network connection required
- ✅ **Privacy Protection**: Data doesn't leave local environment

### Use Cases

- 🎯 **Daily Development**: Code writing, refactoring, debugging
- 🎯 **Quick Prototyping**: Quickly validate ideas and concepts
- 🎯 **Learning & Exploration**: Technical learning and experimentation
- 🎯 **Team Collaboration**: Unified development environment

## 🌐 External API Mode Details

### How It Works

1. **Request Forwarding**: Sends user requests to DeepSeek API
2. **Professional Processing**: DeepSeek model performs professional analysis
3. **Result Retrieval**: Gets professional results returned by API
4. **Formatted Output**: Formats results and returns to user

### Advantages

- 🚀 **Professional Capabilities**: DeepSeek's powerful reasoning abilities
- 🚀 **Independent Service**: Doesn't depend on IDE's LLM capabilities
- 🚀 **Consistency**: Cross-platform consistent response quality
- 🚀 **Scalable**: Supports more complex tasks

### Use Cases

- 🎯 **Complex Analysis**: Deep business analysis and architecture design
- 🎯 **Professional Consulting**: Tasks requiring professional domain knowledge
- 🎯 **Batch Processing**: Analysis and processing of large amounts of data
- 🎯 **High-Quality Output**: Strict requirements for output quality

## ⚙️ Configuration Details

### Environment Variable Configuration

```bash
# === LLM Mode Configuration ===
USE_BUILTIN_LLM=true                    # true=built-in mode, false=external mode

# === DeepSeek API Configuration ===
DEEPSEEK_API_KEY=your_api_key_here      # DeepSeek API key
DEEPSEEK_BASE_URL=https://api.deepseek.com  # API base URL
DEEPSEEK_MODEL=deepseek-chat            # Model name to use

# === Request Configuration ===
API_TIMEOUT=30                          # API timeout (seconds)
API_RETRIES=3                           # Number of retries
API_RETRY_DELAY=1                       # Retry delay (seconds)

# === Cache Configuration ===
ENABLE_CACHE=true                       # Enable response caching
CACHE_TTL=3600                          # Cache expiration time (seconds)
CACHE_SIZE=100                          # Cache size

# === Log Configuration ===
LOG_LEVEL=INFO                          # Log level
LOG_LLM_REQUESTS=false                  # Whether to log LLM requests
```

### Dynamic Configuration

```python
# Switch dynamically at runtime
from llm_client import LLMClient

client = LLMClient()

# Switch to built-in mode
client.switch_mode('builtin')

# Switch to external mode
client.switch_mode('external')

# Get current mode information
info = client.get_mode_info()
print(f"Current mode: {info['mode']}")
print(f"Status: {info['status']}")
```

## 🧪 Testing and Validation

### Mode Switching Tests

```bash
# Test built-in mode
python test_builtin_mode.py

# Test external mode
python test_external_mode.py

# Test mode switching
python test_mode_switching.py
```

### Performance Comparison Tests

```bash
# Run performance comparison
python benchmark_llm_modes.py

# View test results
cat logs/performance_comparison.log
```

### Functionality Verification

```python
# Verify agent functionality
def test_agent_functionality():
    # Test built-in mode
    switch_llm_mode('builtin')
    result1 = call_agent_with_llm('analyst', 'Analyze market trends')
    
    # Test external mode
    switch_llm_mode('external')
    result2 = call_agent_with_llm('analyst', 'Analyze market trends')
    
    # Compare results
    compare_results(result1, result2)
```

## 🚨 Troubleshooting

### Built-in Mode Issues

**Issue: Agent not responding**
```bash
# Check Cursor LLM status
# Ensure Cursor's AI functionality is working properly

# Verify agent configuration
python validate_agents.py

# Check role prompts
python check_role_prompts.py
```

**Issue: Inaccurate role playing**
```bash
# Update agent configuration
python update_agent_configs.py

# Reload agents
python reload_agents.py
```

### External Mode Issues

**Issue: API connection failure**
```bash
# Check network connection
ping api.deepseek.com

# Verify API Key
python test_api_key.py

# Check API configuration
python check_api_config.py
```

**Issue: Request timeout**
```bash
# Increase timeout
set API_TIMEOUT=60

# Enable retry mechanism
set API_RETRIES=5

# Check network quality
python test_network_quality.py
```

### Switching Issues

**Issue: Mode switch not taking effect**
```bash
# Restart service
python bmad_agent_mcp.py --restart

# Clear cache
python clear_cache.py

# Reload configuration
python reload_config.py
```

## 📊 Monitoring and Logging

### Mode Usage Statistics

```python
# View mode usage statistics
from utils import get_usage_stats

stats = get_usage_stats()
print(f"Built-in mode usage count: {stats['builtin_count']}")
print(f"External mode usage count: {stats['external_count']}")
print(f"Average response time: {stats['avg_response_time']}ms")
```

### Performance Monitoring

```bash
# Enable performance monitoring
set ENABLE_PERFORMANCE_MONITORING=true

# View performance report
python generate_performance_report.py

# Real-time monitoring
python monitor_performance.py
```

### Log Analysis

```bash
# Analyze LLM request logs
python analyze_llm_logs.py

# Generate usage report
python generate_usage_report.py

# Export statistics
python export_stats.py --format csv
```

## 🎯 Best Practices

### 1. Mode Selection Strategy

```python
# Intelligent mode selection
def choose_optimal_mode(task_type, complexity, network_available):
    if not network_available:
        return 'builtin'
    
    if task_type in ['coding', 'debugging', 'refactoring']:
        return 'builtin'  # Fast response more important
    
    if complexity == 'high' and task_type in ['analysis', 'architecture']:
        return 'external'  # Professional capabilities more important
    
    return 'builtin'  # Default to built-in mode
```

### 2. Performance Optimization

```python
# Caching strategy
def optimize_performance():
    # Enable intelligent caching
    enable_smart_cache()
    
    # Preload common agents
    preload_common_agents()
    
    # Optimize network settings
    optimize_network_settings()
```

### 3. Error Handling

```python
# Graceful degradation
def handle_llm_error(error, current_mode):
    if current_mode == 'external' and is_network_error(error):
        # Auto switch to built-in mode on network issues
        switch_llm_mode('builtin')
        return retry_with_builtin_mode()
    
    return handle_generic_error(error)
```

## 🔗 Related Resources

- [Cursor IDE Official Documentation](https://cursor.sh/docs)
- [DeepSeek API Documentation](https://platform.deepseek.com/docs)
- [FastMCP Framework Documentation](https://github.com/jlowin/fastmcp)
- [BMAD Methodology](https://github.com/bmadcode/BMAD-METHOD)

---

**🎉 Maximize the power of BMAD Agent through proper mode selection and configuration!**
