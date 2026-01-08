# Contributing to BI Analyst

Thank you for your interest in contributing! This document provides guidelines and instructions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/bi-analyst.git
   cd bi-analyst
   ```

3. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### Code Style

1. **PEP 8 Compliance**: Use `black`
   ```bash
   black bi_analyst/ tests/
   ```

2. **Linting**: Use `flake8`
   ```bash
   flake8 bi_analyst/ tests/
   ```

3. **Type Hints**: Use type annotations
   ```python
   def analyze_data(df: pd.DataFrame) -> dict:
       ...
   ```

4. **Docstrings**: Use Google-style docstrings
   ```python
   def my_function(param1: int) -> str:
       """
       Brief description.
       
       Longer description if needed.
       
       Args:
           param1 (int): Description of param1
           
       Returns:
           str: Description of return value
       """
   ```

### Testing

1. **Write Tests**: Add tests to `test_sales_analyzer.py`
   ```python
   def test_your_feature(analyzer):
       """Test your new feature."""
       result = analyzer.your_method()
       assert result is not None
   ```

2. **Run Tests**:
   ```bash
   pytest
   pytest --cov=bi_analyst  # With coverage
   ```

### Commit Messages

```
feat: Add customer segmentation feature

- Implement RFM analysis
- Add segment classification
- Update documentation
```

Guidelines:
- Use imperative mood ("Add feature" not "Added feature")
- Start with type (feat, fix, docs, test, refactor)
- Keep summary under 50 characters
- Wrap description at 72 characters

### Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** with:
   - Clear title
   - Description of changes
   - Related issues
   - Screenshots if applicable

3. **PR Checklist**:
   - [ ] Code follows PEP 8 style
   - [ ] All tests pass
   - [ ] New tests added for new features
   - [ ] Documentation updated
   - [ ] Commits are clean and well-described

## Reporting Issues

When reporting bugs:

1. **Check existing issues** first
2. **Include details**:
   - Python version
   - pandas/numpy versions
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages

3. **Example Issue**:
   ```
   Title: analyze() fails with large datasets
   
   Python: 3.9
   pandas: 1.3.0
   
   Steps to reproduce:
   1. Load dataset with 100k+ records
   2. Call analyzer.get_regional_analysis()
   
   Expected: Results in < 5 seconds
   Actual: MemoryError after 10 seconds
   ```

## Feature Requests

Suggest enhancements by:
1. Describing the use case
2. Providing examples
3. Discussing implementation approach

## Areas for Contribution

- **Features**: New analysis methods, export formats
- **Bug fixes**: Issues labeled "bug"
- **Documentation**: Examples, API docs, tutorials
- **Tests**: Increase coverage, edge cases
- **Performance**: Optimize algorithms

## Project Structure

```
bi-analyst/
├── bi_analyst/
│   ├── __init__.py
│   ├── sales_analyzer.py     # Core analysis
│   └── dashboard.py          # Visualizations
├── tests/
│   └── test_sales_analyzer.py
├── examples.py               # Usage examples
├── setup.py                  # Package setup
├── README.md                 # Documentation
├── CONTRIBUTING.md           # This file
├── CHANGELOG.md              # Version history
├── LICENSE                   # MIT License
└── .gitignore                # Git ignore rules
```

## Code Review Process

All submissions require review. We look for:
- ✅ Clear, well-tested code
- ✅ Good documentation
- ✅ Performance considerations
- ✅ Backward compatibility

## Questions?

- Open an issue with "question" label
- Check documentation
- Review existing code for examples

## License

By contributing, you agree your contributions are licensed under MIT License.

---

Thank you for contributing! 🎉
