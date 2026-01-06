# Smart Timetable Generator

Automatically generates class timetables with minimal manual effort.

## Features

- 🎯 Automatic timetable generation
- 📚 Support for multiple subjects and teachers
- ⏰ Configurable time slots and days
- 🚫 Conflict-free scheduling
- 🌐 Simple web-based interface

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Algorithm:** Constraint-based scheduling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rithika5656/Smart-Timetable-Generator.git
cd Smart-Timetable-Generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter the subjects (comma-separated)
2. Enter the teachers (comma-separated)
3. Select the number of periods per day
4. Click "Generate Timetable"
5. View and download your generated timetable

## How It Works

The algorithm uses a constraint-based approach to:
- Distribute subjects evenly across the week
- Ensure no teacher has conflicting time slots
- Balance the workload across all days

## License

MIT License
