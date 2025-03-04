# Pomodoro Timer

A customizable Pomodoro Timer application with task tracking, reporting, and session management features.

![Pomodoro Timer Screenshot](docs/screenshot.png)

## Features

- **Pomodoro Timer**: 25-minute work sessions, 5-minute short breaks, 15-minute long breaks
- **Task Management**: Track projects and tasks with dropdown menus
- **Session Tracking**: Automatically records timestamps and durations for each work session
- **Reporting**: Export daily and weekly reports as CSV files
- **Data Visualization**: View past sessions organized by date range
- **Sound Notifications**: Audio alerts when sessions and breaks end

## Installation

### Prerequisites

- Python 3.6 or higher
- Pip (Python package installer)

### Installation Steps

1. Clone this repository:
   ```
   git clone https://github.com/your-username/pomodoro-timer.git
   cd pomodoro-timer
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run directly with Python:
   ```
   python pomodoro_timer.py
   ```

4. (Optional) Build an executable:
   ```
   pyinstaller --onefile --windowed pomodoro_timer.py
   ```

## Usage

### Timer Functions
- **Start**: Begin the Pomodoro timer
- **Pause**: Temporarily stop the timer (automatically saves the current session)
- **Reset**: Reset the current timer phase

### Task Tracking
1. Add a project using the Project field and "Add Project" button
2. Add a task for the project using the Task field and "Add Task" button
3. Select a project and task before starting a Pomodoro
4. The application automatically tracks completed Pomodoros

### Viewing Sessions
- Use the dropdown to select different date ranges: Today, Yesterday, Last 7 Days, etc.
- All sessions appear in the table with date, time, project, task, and duration

### Reporting
- Use "Export Daily Report" to generate a CSV report of today's activity
- Use "Export Weekly Report" to generate a CSV report of this week's activity
- Use "View Data File" to directly view the JSON file storing all data

## Data Storage
All data is stored in `pomodoro_data.json` in the same directory as the application. A log file (`pomodoro_app.log`) is also created to track application events.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Pomodoro Technique was developed by Francesco Cirillo
- Built with Python and Tkinter
