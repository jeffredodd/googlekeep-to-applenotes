# 🤝 Contributing to Keep to Notes Converter

First off, thank you for considering contributing to Keep to Notes Converter! It's people like you that make this tool better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Code Contributions](#code-contributions)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guides](#style-guides)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Style Guide](#python-style-guide)
  - [Documentation Style Guide](#documentation-style-guide)
- [Community](#community)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior.

## 🚀 How Can I Contribute?

### 🐛 Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

**Before Submitting A Bug Report:**
- Check the [issues](https://github.com/jeffredodd/googlekeep-to-applenotes/issues) to see if the bug has already been reported
- Try the latest version to see if the bug has been fixed
- Collect information about the bug:
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Screenshots if applicable
  - Your environment (OS, Python version, etc.)

**How to Submit A Bug Report:**
1. Use a clear and descriptive title
2. Describe the exact steps to reproduce the problem
3. Provide specific examples to demonstrate the steps
4. Describe the behavior you observed and what you expected to see
5. Include details about your configuration and environment

### 💡 Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

**Before Submitting An Enhancement Suggestion:**
- Check if the enhancement has already been suggested or implemented
- Consider whether your idea fits with the scope and aims of the project

**How to Submit An Enhancement Suggestion:**
1. Use a clear and descriptive title
2. Provide a step-by-step description of the suggested enhancement
3. Explain why this enhancement would be useful to most users
4. List some other applications where this enhancement exists, if applicable

### 💻 Code Contributions

#### Local Development

1. Fork the repository
2. Clone your fork locally
3. Create a branch for your feature or fix
4. Make your changes
5. Run tests to ensure your changes don't break existing functionality
6. Commit your changes
7. Push to your fork
8. Submit a pull request

## 🔧 Development Setup

1. Install Python 3.8 or higher
2. Clone the repository:
   ```bash
   git clone https://github.com/jeffredodd/googlekeep-to-applenotes.git
   cd googlekeep-to-applenotes
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r dev-requirements.txt  # If exists
   ```
5. Run tests to ensure everything is working:
   ```bash
   pytest
   ```

## 📤 Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the tests to cover your changes
3. Ensure all tests pass
4. The PR should work for Python 3.8 and above
5. Include a description of the changes and why they should be included

## 📝 Style Guides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Python Style Guide

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use 4 spaces for indentation
* Use docstrings for all public methods and classes
* Keep line length to 88 characters (compatible with Black formatter)

### Documentation Style Guide

* Use Markdown for documentation
* Include code examples where appropriate
* Keep documentation up to date with code changes

## 👥 Community

* Feel free to join discussions in the issues section
* Respect the opinions and time of others
* Help others who are contributing to the project

---

Thank you for contributing to Keep to Notes Converter! Your efforts help make this tool better for everyone. 