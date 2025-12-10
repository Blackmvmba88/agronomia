# Contributing to Agronomia

Thank you for your interest in contributing to Agronomia! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment for all contributors

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, versions, etc.)
   - Logs or screenshots if applicable

### Suggesting Features

1. Check existing issues and discussions
2. Create a feature request with:
   - Use case description
   - Proposed solution
   - Alternative approaches considered
   - Impact on existing functionality

### Code Contributions

#### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/Blackmvmba88/agronomia.git
cd agronomia

# Backend setup
cd backend/api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend setup
cd frontend/web
# Open index.html in browser or use a local server

# AI/ML setup
cd ai-ml/training
pip install -r requirements.txt
```

#### Coding Standards

**Python:**
- Follow PEP 8
- Use type hints
- Write docstrings for functions/classes
- Maximum line length: 100 characters

**JavaScript/HTML:**
- Use ES6+ features
- Consistent indentation (2 spaces)
- Meaningful variable names

**Arduino/C++:**
- Follow Arduino style guide
- Comment complex logic
- Use meaningful constant names

#### Making Changes

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Add tests if applicable
5. Commit with clear messages:
   ```
   feat: Add pH calibration auto-save
   fix: Correct EC sensor reading calculation
   docs: Update hardware setup guide
   ```
6. Push to your fork
7. Create a Pull Request

#### Pull Request Process

1. Update documentation for any changed functionality
2. Add tests for new features
3. Ensure all tests pass
4. Update README.md if needed
5. Reference related issues
6. Wait for review and address feedback

### Documentation

- Keep documentation up-to-date
- Use clear, concise language
- Include examples and screenshots
- Update hardware docs for new components
- Add API documentation for new endpoints

### Hardware Contributions

If contributing hardware designs:
- Provide schematics (Fritzing or KiCad)
- Include bill of materials (BOM)
- Document assembly instructions
- Test with actual components
- Photos of working prototype

### Dataset Contributions

When contributing datasets:
- Anonymize sensitive information
- Follow data format guidelines
- Include metadata file
- Describe collection conditions
- Document any preprocessing

## Testing

### Backend Tests
```bash
cd backend/api
pytest tests/
```

### Firmware Tests
```bash
# Flash to test device
pio test
```

### AI/ML Model Tests
```bash
cd ai-ml/training
python -m pytest tests/
```

## Documentation Style

- Use Markdown format
- Include code examples
- Add diagrams where helpful
- Keep language simple and accessible
- Provide troubleshooting tips

## Community

- GitHub Discussions for questions
- Issues for bugs and features
- Pull Requests for code contributions
- Be patient and respectful

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Open a GitHub Discussion
- Create an issue with the "question" label
- Check existing documentation

## Thank You!

Your contributions help make sustainable agriculture more accessible. Every contribution, no matter how small, is valuable!

---

**Happy Contributing! 🌱**
