# Contributing to Traffic Signal RL

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 🎯 Ways to Contribute

### 🐛 Reporting Bugs
- Use the GitHub Issues tab
- Check if the issue already exists
- Include:
  - Python version
  - Operating system
  - Steps to reproduce
  - Expected vs actual behavior
  - Error messages/screenshots

### 💡 Suggesting Enhancements
- Open a GitHub Issue with the `enhancement` label
- Clearly describe the feature
- Explain why it would be useful
- Provide examples if possible

### 📝 Improving Documentation
- Fix typos or clarify explanations
- Add examples
- Improve README or guides
- Add comments to code

### 🔧 Code Contributions
- Bug fixes
- New features
- Performance improvements
- Test coverage

## 🚀 Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/traffic-signal-rl.git
cd traffic-signal-rl
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r traffic_rl_project/requirements.txt
pip install -r gradio_app/requirements_gradio.txt

# Install development dependencies
pip install black pylint pytest
```

### 3. Create a Branch
```bash
# Create a descriptive branch name
git checkout -b feature/add-sumo-integration
# or
git checkout -b fix/queue-overflow-bug
```

## 💻 Development Guidelines

### Code Style
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Format code with `black`:
  ```bash
  black your_file.py
  ```

### Code Quality
- Run linting before committing:
  ```bash
  pylint your_file.py
  ```
- Add type hints where appropriate
- Keep functions focused and small
- Write self-documenting code

### Testing
- Add tests for new features
- Ensure existing tests pass
- Run tests before submitting:
  ```bash
  pytest
  ```

### Documentation
- Update README if you change functionality
- Add docstrings to new functions
- Update relevant guides (VSCODE_GUIDE.md, etc.)
- Include examples for new features

## 📤 Submitting Changes

### 1. Commit Your Changes
```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add SUMO integration for realistic traffic simulation"
```

### Commit Message Guidelines
- Use present tense ("Add feature" not "Added feature")
- First line: brief summary (50 chars or less)
- Blank line, then detailed description if needed
- Reference issues: "Fixes #123" or "Relates to #456"

Examples:
```
Add SUMO integration module

- Implement TraCI interface
- Add configuration parser
- Update documentation
Fixes #42
```

### 2. Push to Your Fork
```bash
git push origin feature/add-sumo-integration
```

### 3. Create Pull Request
1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR template:
   - Description of changes
   - Motivation and context
   - Type of change (bug fix, feature, etc.)
   - Testing performed
   - Checklist items

### Pull Request Checklist
- [ ] Code follows style guidelines
- [ ] Self-review performed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings
- [ ] Appropriate labels added

## 🎨 Project Areas

### Easy First Issues
Good for newcomers:
- Documentation improvements
- Adding examples
- Fixing typos
- Small bug fixes

### Medium Difficulty
- Adding new baseline controllers
- Improving visualizations
- Adding new metrics
- Performance optimizations

### Advanced
- Multi-intersection coordination
- SUMO integration
- Advanced RL algorithms
- Real-time learning

## 🔍 Code Review Process

1. **Automated Checks**: CI/CD will run tests and linting
2. **Maintainer Review**: A maintainer will review your code
3. **Feedback**: You may receive requests for changes
4. **Approval**: Once approved, your PR will be merged
5. **Recognition**: Your contribution will be acknowledged!

## 📋 Development Setup Tips

### VS Code Setup
- Use the provided workspace: `traffic_rl.code-workspace`
- Install recommended extensions
- Enable format on save

### Testing Locally
```bash
# Test Gradio app
python gradio_app/gradio_traffic_app.py

# Test notebooks
jupyter notebook traffic_rl_project/traffic_signal_rl.ipynb

# Run verification
python traffic_rl_project/test_setup.py
```

### Common Tasks
```bash
# Format all Python files
black .

# Run linting
pylint traffic_rl_project/*.py
pylint gradio_app/*.py

# Run tests
pytest tests/

# Build documentation
# (if we add Sphinx later)
cd docs
make html
```

## 🐛 Debugging Tips

- Use VS Code debugger (F5)
- Add print statements or logging
- Check Jupyter notebook outputs
- Review Gradio app logs in terminal
- Test with simple scenarios first

## 📚 Resources

### Learning Resources
- [Stable-Baselines3 Docs](https://stable-baselines3.readthedocs.io/)
- [Gymnasium Docs](https://gymnasium.farama.org/)
- [Gradio Docs](https://gradio.app/docs/)

### Project Documentation
- [Main README](README.md)
- [VS Code Guide](VSCODE_GUIDE.md)
- [Deployment Guide](gradio_app/DEPLOYMENT_GUIDE.md)

## 🤝 Community

- Be respectful and inclusive
- Help others learn
- Ask questions if unclear
- Provide constructive feedback
- Celebrate contributions!

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Security Issues**: Email directly (don't open public issue)

## 🎉 Recognition

Contributors will be:
- Listed in the README
- Mentioned in release notes
- Credited in documentation

Thank you for contributing to Traffic Signal RL! 🚦

---

*This guide is adapted from various open-source projects. Feel free to suggest improvements!*
