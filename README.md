# 📚 Smart Timetable Generator

A robust, conflict-free class timetable generator built with Flask and modern JavaScript.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features
- **Automatic Scheduling**: Generates conflict-free schedules in milliseconds.
- **Premium UI**: Glassmorphism design with responsive tables.
- **Worker Statistics**: Real-time tracking of teacher load.
- **Export**: Download timetables as CSV files.
- **Robust Backend**: Type-safe architecture with comprehensive error handling.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Pip

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App
Double-click `run.bat` or execute:
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

## 🛠️ Development

### Project Structure
```
├── app.py              # Application entry point
├── scheduler.py        # Core algorithm engine
├── models.py           # Data structures
├── config.py           # Configuration
├── static/             # Frontend assets (CSS/JS)
├── templates/          # HTML templates
└── tests/              # Test suite
```

### Running Tests
Double-click `test.bat` or execute:
```bash
pytest
```

### Docker Support
Run nicely in a container:
```bash
docker build -t timetable-app .
docker run -p 5000:5000 timetable-app
```

## 🤝 Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🧪 Running Tests
To run the test suite:
```bash
pytest
```
