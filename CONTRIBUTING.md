# Contributing to Smart Timetable Generator

We welcome contributions! Please follow these guidelines to keep the codebase clean and robust.

## Code Standards
- **Python**: Follow PEP 8. Use type hints for all function arguments and return values.
- **JavaScript**: Use modern ES6+ syntax and modular imports.

## Architecture
This project follows a modular architecture:
- **`scheduler.py`**: Contains strictly the algorithm logic. Do not put HTTP logic here.
- **`app.py`**: Contains strictly routing logic. Delegate complexities to `utils.py`.
- **`models.py`**: Define all data structures here.

## Testing
- Add unit tests for any new logic in `scheduler.py`.
- Add integration tests for new API endpoints.
- Ensure all tests pass (`test.bat`) before submitting a PR.

## Pull Request Process
1. Update README with behavioral changes.
2. Increase version numbers if applicable.
3. Merge after CI passes.
