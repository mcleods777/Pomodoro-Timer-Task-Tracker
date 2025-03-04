# Pomodoro Timer User Guide

This guide explains how to use all features of the Pomodoro Timer application.

## The Pomodoro Technique

The Pomodoro Technique is a time management method developed by Francesco Cirillo in the late 1980s. It involves:

1. Breaking work into 25-minute intervals (called "Pomodoros")
2. Taking short 5-minute breaks between Pomodoros
3. Taking a longer 15-minute break after completing 4 Pomodoros

## Application Overview

![Application Interface](screenshot.png)

The interface is divided into several sections:

### Timer Section
- **Timer Display**: Shows the remaining time in minutes and seconds
- **Mode Indicator**: Shows current mode (Pomodoro, Short Break, or Long Break)
- **Start Button**: Begins the timer countdown
- **Pause Button**: Temporarily stops the timer
- **Reset Button**: Resets the current timer phase

### Task Information Section
- **Project Field**: Select or create a project
- **Task Field**: Select or create a task within the selected project
- **Add/Delete Buttons**: Manage your projects and tasks

### Task Sessions Section
- **Date Range Selector**: Choose which sessions to display
- **Sessions Table**: Shows recorded work sessions with details
- **Refresh Button**: Updates the sessions display

### Controls Section
- **Export Reports**: Generate CSV reports of your work history
- **View Data File**: Open the raw data file in your text editor
- **Enable Sounds**: Toggle sound notifications

## Common Workflows

### Starting Your First Pomodoro
1. Add a project (e.g., "Work")
2. Add a task (e.g., "Email")
3. Select the project and task from the dropdowns
4. Click "Start"
5. Work on your task until the timer ends
6. Take a break when prompted

### Managing Multiple Tasks
1. Create different projects for various areas of responsibility
2. Add specific tasks under each project
3. Select the appropriate project and task before each Pomodoro
4. Track your progress in the Sessions table

### Reviewing Your Productivity
1. Use the date range selector to view sessions from different periods
2. Export reports for more detailed analysis
3. Review which tasks are taking the most time

## Tips for Effective Use

1. **Be Specific**: Create clear, specific task descriptions
2. **Stay Focused**: During a Pomodoro, work only on the designated task
3. **Respect the Breaks**: Take all scheduled breaks to maintain productivity
4. **Adjust as Needed**: If 25 minutes isn't working for you, consider changing the timer settings in the code
5. **Review Regularly**: Use the reporting features to analyze your work patterns

## Troubleshooting

### Common Issues
- **No Sound**: Check if "Enable Sounds" is checked
- **Missing Sessions**: Verify you've selected the correct date range
- **Task Not Saving**: Ensure you click "Add Task" after typing in the task name

### Data Management
- The application stores all data in `pomodoro_data.json`
- If you need to reset all data, close the application and delete this file
- Consider backing up this file periodically to avoid data loss
