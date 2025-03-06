import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import time
from datetime import datetime, timedelta
import webbrowser
import csv

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer with Task Tracking")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        # Configure logging
        import logging
        logging.basicConfig(
            filename='pomodoro_app.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('pomodoro')
        
        # Add console handler to show logs in console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        
        self.logger.info("Application started")
        
        # Timer settings
        self.pomodoro_time = 25 * 60  # 25 minutes in seconds
        self.short_break_time = 5 * 60  # 5 minutes
        self.long_break_time = 15 * 60  # 15 minutes
        self.current_time = self.pomodoro_time
        self.timer_running = False
        self.current_mode = "Pomodoro"
        self.completed_pomodoros = 0
        
        # Sound settings
        self.enable_sounds = tk.BooleanVar(value=True)
        
        # Task tracking
        self.data_file = "pomodoro_data.json"
        self.projects = []
        self.tasks = []
        self.current_task = None
        self.current_project = None
        self.task_start_time = None
        self.task_sessions = []
        
        # Load existing data
        self.load_data()
        self.logger.info(f"Loaded {len(self.projects)} projects and {len(self.tasks)} tasks")
        self.logger.info(f"Loaded {len(self.task_sessions)} previous sessions")
        
        # Create the interface
        self.create_widgets()
        self.update_timer_display()
    
    def create_widgets(self):
        # Main container frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Timer section
        timer_frame = ttk.LabelFrame(main_frame, text="Timer", padding="10")
        timer_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.timer_label = ttk.Label(timer_frame, text="25:00", font=("Arial", 48))
        self.timer_label.pack(pady=10)
        
        self.mode_label = ttk.Label(timer_frame, text="Pomodoro Mode")
        self.mode_label.pack(pady=5)
        
        timer_buttons_frame = ttk.Frame(timer_frame)
        timer_buttons_frame.pack(pady=10)
        
        self.start_button = ttk.Button(timer_buttons_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.pause_button = ttk.Button(timer_buttons_frame, text="Pause", command=self.pause_timer, state=tk.DISABLED)
        self.pause_button.grid(row=0, column=1, padx=5)
        
        self.reset_button = ttk.Button(timer_buttons_frame, text="Reset", command=self.reset_timer)
        self.reset_button.grid(row=0, column=2, padx=5)
        
        # Task input section
        task_frame = ttk.LabelFrame(main_frame, text="Task Information", padding="10")
        task_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(task_frame, text="Project:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.project_combo = ttk.Combobox(task_frame, width=30)
        self.project_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.project_combo['values'] = self.projects
        self.project_combo.bind('<Return>', self.add_project)
        
        ttk.Button(task_frame, text="Add Project", command=self.add_project).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(task_frame, text="Delete Project", command=self.delete_project).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(task_frame, text="Task:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.task_combo = ttk.Combobox(task_frame, width=30)
        self.task_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.task_combo['values'] = self.tasks
        self.task_combo.bind('<Return>', self.add_task)
        
        ttk.Button(task_frame, text="Add Task", command=self.add_task).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(task_frame, text="Delete Task", command=self.delete_task).grid(row=1, column=3, padx=5, pady=5)
        
        # Task sessions section
        sessions_frame = ttk.LabelFrame(main_frame, text="Task Sessions", padding="10")
        sessions_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Date selection
        date_frame = ttk.Frame(sessions_frame)
        date_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(date_frame, text="View sessions for:").pack(side=tk.LEFT, padx=5)
        
        # Create date options
        self.date_var = tk.StringVar(value="Today")
        date_options = ["Today", "Yesterday", "Last 7 Days", "Last 30 Days", "All Time"]
        date_dropdown = ttk.Combobox(date_frame, textvariable=self.date_var, values=date_options, width=15, state="readonly")
        date_dropdown.pack(side=tk.LEFT, padx=5)
        date_dropdown.bind("<<ComboboxSelected>>", lambda e: self.populate_sessions_tree())
        
        refresh_button = ttk.Button(date_frame, text="Refresh", command=self.populate_sessions_tree)
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Create Treeview for session history
        columns = ("Date", "Time", "Project", "Task", "Duration")
        self.sessions_tree = ttk.Treeview(sessions_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.sessions_tree.heading(col, text=col)
            self.sessions_tree.column(col, width=100)
        
        self.sessions_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Add scrollbar
        sessions_scrollbar = ttk.Scrollbar(sessions_frame, orient=tk.VERTICAL, command=self.sessions_tree.yview)
        sessions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sessions_tree.configure(yscrollcommand=sessions_scrollbar.set)
        
        # Reports and settings frame
        controls_frame = ttk.Frame(main_frame, padding="5")
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Export Daily Report", command=self.export_daily_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Export Weekly Report", command=self.export_weekly_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="View Data File", command=self.view_data_file).pack(side=tk.LEFT, padx=5)
        
        # Sound toggle
        sound_frame = ttk.Frame(controls_frame)
        sound_frame.pack(side=tk.RIGHT, padx=5)
        sound_check = ttk.Checkbutton(sound_frame, text="Enable Sounds", variable=self.enable_sounds)
        sound_check.pack(side=tk.RIGHT)
        
        # Populate the session tree
        self.populate_sessions_tree()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as file:
                    data = json.load(file)
                    self.projects = data.get("projects", [])
                    self.tasks = data.get("tasks", [])
                    self.task_sessions = data.get("sessions", [])
            except (json.JSONDecodeError, FileNotFoundError):
                self.projects = []
                self.tasks = []
                self.task_sessions = []
    
    def save_data(self):
        data = {
            "projects": self.projects,
            "tasks": self.tasks,
            "sessions": self.task_sessions
        }
        with open(self.data_file, "w") as file:
            json.dump(data, file, indent=4, sort_keys=True)
        
        self.logger.info(f"Saved data with {len(self.projects)} projects, {len(self.tasks)} tasks, and {len(self.task_sessions)} sessions")
    
    def add_project(self, event=None):
        project = self.project_combo.get().strip()
        if project and project not in self.projects:
            self.projects.append(project)
            self.project_combo['values'] = self.projects
            self.save_data()
    
    def delete_project(self):
        project = self.project_combo.get()
        if project and project in self.projects:
            if messagebox.askyesno("Confirm", f"Delete project '{project}'? This will remove all associated task records."):
                self.projects.remove(project)
                
                # Remove task sessions associated with the project
                self.task_sessions = [session for session in self.task_sessions 
                                      if session.get("project") != project]
                
                # Remove tasks associated with the project
                self.tasks = [task for task in self.tasks 
                              if not task.startswith(f"{project}:")]
                
                self.project_combo['values'] = self.projects
                self.project_combo.set('')
                self.task_combo['values'] = self.tasks
                self.populate_sessions_tree()
                self.save_data()
    
    def add_task(self, event=None):
        project = self.project_combo.get()
        task = self.task_combo.get().strip()
        
        if not project:
            messagebox.showwarning("Warning", "Please select or add a project first.")
            return
        
        if task:
            task_key = f"{project}: {task}"
            if task_key not in self.tasks:
                self.tasks.append(task_key)
                self.task_combo['values'] = self.tasks
                self.save_data()
    
    def delete_task(self):
        task_key = self.task_combo.get()
        if task_key and task_key in self.tasks:
            if messagebox.askyesno("Confirm", f"Delete task '{task_key}'? This will remove all associated records."):
                self.tasks.remove(task_key)
                
                # Remove task sessions associated with the task
                self.task_sessions = [session for session in self.task_sessions 
                                      if session.get("task_key") != task_key]
                
                self.task_combo['values'] = self.tasks
                self.task_combo.set('')
                self.populate_sessions_tree()
                self.save_data()
    
    def update_timer_display(self):
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        time_string = f"{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=time_string)
        
        # Update mode label
        if self.current_mode == "Pomodoro":
            pomodoro_count = self.completed_pomodoros
            self.mode_label.config(text=f"Pomodoro Mode ({pomodoro_count}/4)")
        elif self.current_mode == "Short Break":
            self.mode_label.config(text="Short Break")
        else:
            self.mode_label.config(text="Long Break")
    
    def start_timer(self):
        if not self.timer_running:
            # Validate task and project selection for Pomodoro mode
            if self.current_mode == "Pomodoro":
                self.current_task = self.task_combo.get()
                self.current_project = self.project_combo.get()
                
                if not self.current_project:
                    messagebox.showwarning("Warning", "Please select a project before starting the timer.")
                    return
                    
                if not self.current_task:
                    messagebox.showwarning("Warning", "Please select a task before starting the timer.")
                    return
            
            self.timer_running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            
            # If we're starting a Pomodoro, record the start time
            if self.current_mode == "Pomodoro":
                self.task_start_time = datetime.now()
                print(f"Started session for {self.current_project}: {self.current_task} at {self.task_start_time}")
            
            self.tick()
    
    def play_sound(self, sound_type):
        """Play a sound based on the type of notification"""
        if not self.enable_sounds.get():
            return
            
        try:
            if sound_type == "pomodoro_complete":
                # High-pitched beep for Pomodoro completion
                winsound.Beep(1000, 500)  # 1000 Hz for 500 milliseconds
                time.sleep(0.2)
                winsound.Beep(1000, 500)
                time.sleep(0.2)
                winsound.Beep(1000, 500)
            elif sound_type == "break_complete":
                # Lower-pitched beep for break completion
                winsound.Beep(800, 800)  # 800 Hz for 800 milliseconds
                time.sleep(0.3)
                winsound.Beep(800, 800)
            else:
                # Generic notification sound
                winsound.Beep(600, 500)
                
            self.logger.info(f"Played sound: {sound_type}")
        except Exception as e:
            self.logger.error(f"Error playing sound: {str(e)}")
            
    def tick(self):
        if self.timer_running and self.current_time > 0:
            self.current_time -= 1
            self.update_timer_display()
            self.root.after(1000, self.tick)
        elif self.timer_running and self.current_time <= 0:
            self.timer_running = False
            
            # Actions when timer completes
            if self.current_mode == "Pomodoro":
                # Play completion sound
                self.play_sound("pomodoro_complete")
                
                # Record task session when Pomodoro completes
                if self.task_start_time and self.current_task:
                    print(f"Pomodoro completed for {self.current_project}: {self.current_task}")
                    self.record_task_session()
                
                self.completed_pomodoros += 1
                
                # Decide whether to take a short break or long break
                if self.completed_pomodoros % 4 == 0:
                    self.current_mode = "Long Break"
                    self.current_time = self.long_break_time
                else:
                    self.current_mode = "Short Break"
                    self.current_time = self.short_break_time
                
                messagebox.showinfo("Pomodoro Complete", "Time to take a break!")
            else:
                # Play break completion sound
                self.play_sound("break_complete")
                
                # Break is over, start a new Pomodoro
                self.current_mode = "Pomodoro"
                self.current_time = self.pomodoro_time
                messagebox.showinfo("Break Complete", "Time to focus!")
            
            self.update_timer_display()
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            
            # Reset task start time after completion
            self.task_start_time = None
    
    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            
            # If we're pausing a Pomodoro (not a break), record the session
            if self.current_mode == "Pomodoro" and self.task_start_time:
                self.record_task_session()
                # Reset task start time to prevent double-recording
                self.task_start_time = None
    
    def reset_timer(self):
        # If we're resetting a running Pomodoro, record the session
        if self.timer_running and self.current_mode == "Pomodoro" and self.task_start_time:
            self.record_task_session()
        
        self.timer_running = False
        
        # Only reset the time based on the current mode
        if self.current_mode == "Pomodoro":
            self.current_time = self.pomodoro_time
        elif self.current_mode == "Short Break":
            self.current_time = self.short_break_time
        else:
            self.current_time = self.long_break_time
        
        self.update_timer_display()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        
        # Reset task start time
        self.task_start_time = None
    
    def record_task_session(self):
        # Only record if we have a valid start time and task
        if not self.task_start_time or not self.current_task or not self.current_project:
            return
            
        end_time = datetime.now()
        duration = end_time - self.task_start_time
        
        # Only record sessions that are at least 1 minute long
        if duration.total_seconds() < 60:
            return
            
        # Create session record
        session = {
            "start_time": self.task_start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "project": self.current_project,
            "task": self.current_task.replace(f"{self.current_project}: ", ""),
            "task_key": self.current_task,
            "duration_seconds": duration.total_seconds()
        }
        
        # Add to sessions and save
        self.task_sessions.append(session)
        self.save_data()
        
        # Update the sessions tree
        self.populate_sessions_tree()
        
        # Display confirmation message
        messagebox.showinfo("Session Recorded", 
                           f"Session recorded:\nProject: {self.current_project}\nTask: {session['task']}\nDuration: {self.format_duration(duration.total_seconds())}")
    
    def format_duration(self, seconds):
        """Format duration in seconds to mm:ss format"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def populate_sessions_tree(self):
        """Populate the sessions tree with filtered sessions based on selected date range"""
        # Clear existing items
        for item in self.sessions_tree.get_children():
            self.sessions_tree.delete(item)
        
        # Determine date range based on selection
        today = datetime.now().date()
        date_filter = self.date_var.get()
        
        start_date = None
        if date_filter == "Today":
            start_date = today
        elif date_filter == "Yesterday":
            start_date = today - timedelta(days=1)
            end_date = start_date
        elif date_filter == "Last 7 Days":
            start_date = today - timedelta(days=6)
        elif date_filter == "Last 30 Days":
            start_date = today - timedelta(days=29)
        # All Time has no start date filter
        
        # Filter sessions based on date range
        filtered_sessions = []
        for session in self.task_sessions:
            session_date = datetime.fromisoformat(session["start_time"]).date()
            
            if date_filter == "Today" and session_date == today:
                filtered_sessions.append(session)
            elif date_filter == "Yesterday" and session_date == start_date:
                filtered_sessions.append(session)
            elif date_filter == "Last 7 Days" and start_date <= session_date <= today:
                filtered_sessions.append(session)
            elif date_filter == "Last 30 Days" and start_date <= session_date <= today:
                filtered_sessions.append(session)
            elif date_filter == "All Time":
                filtered_sessions.append(session)
        
        # Sort sessions by start time (most recent first)
        filtered_sessions.sort(key=lambda x: x["start_time"], reverse=True)
        
        # Add sessions to tree
        for session in filtered_sessions:
            start_time = datetime.fromisoformat(session["start_time"])
            date_str = start_time.strftime("%Y-%m-%d")
            time_str = start_time.strftime("%H:%M")
            project = session["project"]
            task = session["task"]
            duration = self.format_duration(session["duration_seconds"])
            
            self.sessions_tree.insert("", tk.END, values=(date_str, time_str, project, task, duration))
        
        # Update the label to show count
        count = len(filtered_sessions)
        range_text = date_filter
        if count == 0:
            self.logger.info(f"No sessions found for {range_text}")
        else:
            self.logger.info(f"Showing {count} sessions for {range_text}")
    
    def export_daily_report(self):
        today = datetime.now().date()
        self.export_report(today, today, "daily")
    
    def export_weekly_report(self):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        self.export_report(start_of_week, today, "weekly")
    
    def view_data_file(self):
        """Open the JSON data file in the default text editor"""
        try:
            # Check if file exists first
            if not os.path.exists(self.data_file):
                messagebox.showinfo("File Not Found", "The data file has not been created yet.")
                return
                
            # Open the JSON file in the default application
            webbrowser.open(self.data_file)
            self.logger.info(f"Opened data file for viewing: {self.data_file}")
        except Exception as e:
            self.logger.error(f"Error opening data file: {str(e)}")
            messagebox.showerror("Error", f"Could not open data file: {str(e)}")
            
    def export_report(self, start_date, end_date, report_type):
        # Filter sessions in the given date range
        filtered_sessions = []
        
        for session in self.task_sessions:
            session_date = datetime.fromisoformat(session["start_time"]).date()
            if start_date <= session_date <= end_date:
                filtered_sessions.append(session)
        
        if not filtered_sessions:
            messagebox.showinfo("No Data", f"No task sessions found for the {report_type} report period.")
            return
        
        # Ask for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"pomodoro_{report_type}_report_{start_date}.csv"
        )
        
        if not filename:
            return
        
        # Write to CSV
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Date', 'Start Time', 'End Time', 'Project', 'Task', 'Duration (min)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for session in filtered_sessions:
                start_time = datetime.fromisoformat(session["start_time"])
                end_time = datetime.fromisoformat(session["end_time"])
                duration_min = session["duration_seconds"] / 60
                
                writer.writerow({
                    'Date': start_time.strftime("%Y-%m-%d"),
                    'Start Time': start_time.strftime("%H:%M:%S"),
                    'End Time': end_time.strftime("%H:%M:%S"),
                    'Project': session["project"],
                    'Task': session["task"],
                    'Duration (min)': f"{duration_min:.1f}"
                })
        
        messagebox.showinfo("Report Exported", f"The {report_type} report has been exported to {filename}")
        self.logger.info(f"Exported {report_type} report with {len(filtered_sessions)} sessions to {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
