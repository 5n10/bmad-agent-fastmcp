# 🤝 Contributing to BMAD Agent FastMCP Service

Thank you for your interest in the BMAD Agent FastMCP Service project! We welcome all forms of contributions.

## 🎯 Ways to Contribute

### 🐛 Report Bugs
- Use [GitHub Issues](https://github.com/your-username/bmad-agent-fastmcp/issues) to report issues
- Provide detailed error descriptions and reproduction steps
- Include system environment information (Python version, operating system, etc.)

### 💡 Feature Suggestions
- Propose new features in Issues
- Describe feature requirements and use cases in detail
- Discuss the feasibility of implementation solutions

### 🔧 Code Contributions
1. Fork the project to your GitHub account
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Create Pull Request

## 📋 Development Guide

### Environment Setup
```bash
# Clone project
git clone https://github.com/your-username/bmad-agent-fastmcp.git
cd bmad-agent-fastmcp

# Install dependencies
pip install -r requirements.txt

# Run tests
python tests/simple_test.py
```

### Code Standards
- Follow PEP 8 Python code standards
- Use meaningful variable and function names
- Add appropriate comments and docstrings
- Keep code concise and readable

### Testing Requirements
- New features must include corresponding tests
- Ensure all existing tests pass
- Test coverage should be maintained at a reasonable level

## 🏗️ Project Structure

```
📂 bmad-agent-fastmcp/
├── 📄 bmad_agent_mcp.py     # Main service file
├── 📄 llm_client.py         # LLM client
├── 📄 utils.py              # Utility functions
├── 📁 .bmad-core/           # Core data
├── 📁 docs/                 # Documentation
├── 📁 tests/                # Tests
└── 📁 archive/              # Archives
```

## 🎨 Adding New Agents

1. Create a new agent configuration file in the `.bmad-core/agents/` directory
2. Define agent properties following the existing format
3. Register the new agent in `bmad_agent_mcp.py`
4. Add corresponding tests

## 🔄 Adding New Workflows

1. Create workflow definition in the `.bmad-core/workflows/` directory
2. Define steps and dependencies
3. Implement workflow logic
4. Add documentation and tests

## 📝 Documentation Contributions

- Improve clarity and accuracy of existing documentation
- Add usage examples and best practices
- Translate documentation to other languages
- Create tutorials and guides

## 🔍 Code Review

All Pull Requests will go through code review:
- Check code quality and standards
- Verify functionality correctness
- Ensure backward compatibility
- Evaluate performance impact

## 📞 Contact

- GitHub Issues: Technical questions and feature suggestions
- Discussions: General discussions and Q&A
- Email: Private or sensitive issues

## 📜 Code of Conduct

Please follow our code of conduct:
- Respect all contributors
- Keep discussions constructive
- Welcome newcomers and learners
- Create an inclusive environment

## 🎉 Acknowledgments

Thanks to all developers who contribute to the project! Your contributions make this project better.

---

**Happy Coding! 🚀**
