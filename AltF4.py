import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
from datetime import datetime
import sys
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[
                       logging.FileHandler('personality_analyzer.log'),
                       logging.StreamHandler()
                   ])

# Modern color scheme
COLORS = {
    'bg': '#1E1E1E',
    'fg': '#FFFFFF',
    'accent': '#007ACC',
    'secondary': '#2D2D2D',
    'text': '#CCCCCC',
    'success': '#4CAF50',
    'warning': '#FFC107',
    'error': '#F44336'
}

class PersonalityAnalyzer:
    def __init__(self, root):
        try:
            logging.info("Initializing PersonalityAnalyzer")
            self.root = root
            self.root.title("Personality Analyzer")
            self.root.geometry("1000x700")
            self.root.configure(bg=COLORS['bg'])
            
            # Set dark theme for matplotlib
            plt.style.use('dark_background')
            
            # Initialize variables
            self.name = tk.StringVar()
            self.current_question = 0
            self.scores = {
                "📚 studying": 0,
                "🎨 hobbies": 0,
                "💪 fitness": 0
            }
            self.responses = []
            
            # Questions
            self.questions = [
                # Studying questions
                {"text": "📚 Do you enjoy studying and learning new things?", "category": "studying", "emoji": "📚"},
                {"text": "📚 Do you find yourself studying for long hours regularly?", "category": "studying", "emoji": "📚"},
                {"text": "📚 Do you prefer quiet environments for studying?", "category": "studying", "emoji": "📚"},
                {"text": "📚 Do you enjoy taking notes and organizing information?", "category": "studying", "emoji": "📚"},
                {"text": "📚 Do you often research topics outside of required coursework?", "category": "studying", "emoji": "📚"},
                
                # Hobbies questions
                {"text": "🎨 Do you have any hobbies or creative interests?", "category": "hobbies", "emoji": "🎨"},
                {"text": "🎨 Do you spend significant time on your hobbies?", "category": "hobbies", "emoji": "🎨"},
                {"text": "🎨 Do you enjoy creating art or music?", "category": "hobbies", "emoji": "🎨"},
                {"text": "🎨 Do you like trying new creative activities?", "category": "hobbies", "emoji": "🎨"},
                {"text": "🎨 Do you find joy in expressing yourself creatively?", "category": "hobbies", "emoji": "🎨"},
                
                # Fitness questions
                {"text": "💪 Do you enjoy physical exercise or sports?", "category": "fitness", "emoji": "💪"},
                {"text": "💪 Do you maintain a regular fitness routine?", "category": "fitness", "emoji": "💪"},
                {"text": "💪 Do you enjoy outdoor activities and sports?", "category": "fitness", "emoji": "💪"},
                {"text": "💪 Do you prefer team sports or individual workouts?", "category": "fitness", "emoji": "💪"},
                {"text": "💪 Do you set fitness goals and track your progress?", "category": "fitness", "emoji": "💪"}
            ]
            
            self.setup_ui()
            logging.info("PersonalityAnalyzer initialized successfully")
        except Exception as e:
            logging.error(f"Error in initialization: {str(e)}")
            logging.error(traceback.format_exc())
            messagebox.showerror("Initialization Error", 
                               f"An error occurred while starting the application:\n{str(e)}")
            self.root.quit()

    def setup_ui(self):
        try:
            logging.info("Setting up UI")
            # Create main frame
            self.main_frame = ttk.Frame(self.root, padding="20")
            self.main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Configure style
            style = ttk.Style()
            style.configure('TFrame', background=COLORS['bg'])
            style.configure('TLabel', background=COLORS['bg'], foreground=COLORS['fg'], font=('Segoe UI', 10))
            
            # Configure default button style
            style.configure('TButton', 
                          background=COLORS['accent'],
                          foreground=COLORS['fg'],
                          font=('Segoe UI', 10, 'bold'),
                          padding=10,
                          relief='flat')
            
            # Configure Start Analysis button style (blue)
            style.configure('Start.TButton',
                          background='#1976D2',  # Material Blue
                          foreground=COLORS['fg'],
                          font=('Segoe UI', 12, 'bold'),
                          padding=15,
                          relief='flat')
            style.map('Start.TButton',
                     background=[('active', '#2196F3'),  # Lighter blue on hover
                               ('pressed', '#0D47A1')],  # Darker blue when pressed
                     foreground=[('active', COLORS['fg']),
                               ('pressed', COLORS['fg'])])
            
            # Configure Yes button style (green)
            style.configure('Yes.TButton',
                          background='#2E7D32',  # Dark green
                          foreground=COLORS['fg'],
                          font=('Segoe UI', 10, 'bold'),
                          padding=10,
                          relief='flat')
            style.map('Yes.TButton',
                     background=[('active', '#4CAF50'),  # Lighter green on hover
                               ('pressed', '#1B5E20')],  # Darker green when pressed
                     foreground=[('active', COLORS['fg']),
                               ('pressed', COLORS['fg'])])
            
            # Configure No button style (red)
            style.configure('No.TButton',
                          background='#C62828',  # Dark red
                          foreground=COLORS['fg'],
                          font=('Segoe UI', 10, 'bold'),
                          padding=10,
                          relief='flat')
            style.map('No.TButton',
                     background=[('active', '#F44336'),  # Lighter red on hover
                               ('pressed', '#B71C1C')],  # Darker red when pressed
                     foreground=[('active', COLORS['fg']),
                               ('pressed', COLORS['fg'])])
            
            # Configure Checkbutton style
            style.configure('TCheckbutton',
                          background=COLORS['bg'],
                          foreground=COLORS['fg'],
                          indicatorbackground=COLORS['secondary'],
                          indicatorcolor=COLORS['accent'],
                          relief='flat')
            style.map('TCheckbutton',
                     background=[('active', COLORS['bg']),
                               ('pressed', COLORS['bg'])],
                     foreground=[('active', COLORS['fg']),
                               ('pressed', COLORS['fg'])],
                     indicatorcolor=[('selected', COLORS['success']),
                                   ('!selected', COLORS['secondary'])])
            
            # Configure progress bar style
            style.configure('TProgressbar',
                          background=COLORS['accent'],
                          troughcolor=COLORS['secondary'],
                          borderwidth=0,
                          thickness=20)
            
            # Create menu bar
            self.create_menu()
            
            # Welcome screen
            self.welcome_frame = ttk.Frame(self.main_frame)
            self.welcome_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(self.welcome_frame, text="👋 Welcome to Personality Analyzer!", 
                     font=('Segoe UI', 24, 'bold'), foreground=COLORS['fg']).pack(pady=40)
            
            ttk.Label(self.welcome_frame, text="Enter your name to begin:",
                     font=('Segoe UI', 12), foreground=COLORS['fg']).pack(pady=20)
            
            # Create a custom entry widget with visible text
            entry_frame = ttk.Frame(self.welcome_frame)
            entry_frame.pack(pady=20)
            
            entry = tk.Entry(entry_frame, textvariable=self.name, width=30,
                           font=('Segoe UI', 12),
                           bg=COLORS['secondary'],
                           fg=COLORS['fg'],
                           insertbackground=COLORS['fg'],
                           selectbackground=COLORS['accent'],
                           selectforeground=COLORS['fg'])
            entry.pack()
            
            start_button = ttk.Button(self.welcome_frame, text="Start Analysis", 
                                    command=self.start_analysis,
                                    style='Start.TButton',
                                    width=20)
            start_button.pack(pady=30)
            
            # Question screen
            self.question_frame = ttk.Frame(self.main_frame)
            
            self.question_label = ttk.Label(self.question_frame, 
                                          font=('Segoe UI', 14),
                                          wraplength=600,
                                          foreground=COLORS['fg'])
            self.question_label.pack(pady=30)
            
            self.answer_frame = ttk.Frame(self.question_frame)
            self.answer_frame.pack(pady=20)
            
            yes_button = ttk.Button(self.answer_frame, text="Yes", 
                                  command=lambda: self.process_answer(True),
                                  width=10,
                                  style='Yes.TButton')
            yes_button.pack(side=tk.LEFT, padx=20)
            
            no_button = ttk.Button(self.answer_frame, text="No", 
                                 command=lambda: self.process_answer(False),
                                 width=10,
                                 style='No.TButton')
            no_button.pack(side=tk.LEFT, padx=20)
            
            # Progress bar
            self.progress = ttk.Progressbar(self.question_frame, 
                                          length=400, 
                                          mode='determinate',
                                          style='TProgressbar')
            self.progress.pack(pady=30)
            
            # Results screen
            self.results_frame = ttk.Frame(self.main_frame)
            
            self.category_label = ttk.Label(self.results_frame, 
                                          font=('Segoe UI', 20, 'bold'),
                                          foreground=COLORS['fg'])
            self.category_label.pack(pady=20)
            
            self.description_label = ttk.Label(self.results_frame, 
                                             wraplength=600,
                                             font=('Segoe UI', 12),
                                             foreground=COLORS['fg'])
            self.description_label.pack(pady=20)
            
            # Chart frame
            self.chart_frame = ttk.Frame(self.results_frame)
            self.chart_frame.pack(pady=20)
            
            # Action buttons
            self.action_frame = ttk.Frame(self.results_frame)
            self.action_frame.pack(pady=20)
            
            save_button = ttk.Button(self.action_frame, text="Save Results", 
                                   command=self.save_results,
                                   width=15)
            save_button.pack(side=tk.LEFT, padx=20)
            
            start_over_button = ttk.Button(self.action_frame, text="Start Over", 
                                         command=self.start_over,
                                         width=15)
            start_over_button.pack(side=tk.LEFT, padx=20)
            
            logging.info("UI setup completed successfully")
        except Exception as e:
            logging.error(f"Error in UI setup: {str(e)}")
            logging.error(traceback.format_exc())
            messagebox.showerror("UI Setup Error", 
                               f"An error occurred while setting up the interface:\n{str(e)}")
            self.root.quit()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_command(label="Load Results", command=self.load_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Help", command=self.show_help)
        
    def start_analysis(self):
        if not self.name.get().strip():
            messagebox.showerror("Error", "Please enter your name")
            return
            
        self.welcome_frame.pack_forget()
        self.question_frame.pack(fill=tk.BOTH, expand=True)
        self.show_question()
        
        # Load any existing task progress
        self.load_task_progress()
        
    def show_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.question_label.config(text=question["text"])
            self.progress["value"] = (self.current_question / len(self.questions)) * 100
        else:
            self.show_results()
            
    def process_answer(self, answer):
        question = self.questions[self.current_question]
        if answer:
            self.scores[f"{question['emoji']} {question['category']}"] += 1
        self.responses.append({
            "question": question["text"],
            "answer": "Yes" if answer else "No"
        })
        self.current_question += 1
        self.show_question()
        
    def show_results(self):
        self.question_frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        category, description, tasks = self.analyze_results()
        self.category_label.config(text=f"Category: {category}")
        self.description_label.config(text=description)
        
        # Create a container frame for centered content
        container_frame = ttk.Frame(self.results_frame)
        container_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)
        
        # Create tasks frame with a title
        tasks_title = ttk.Label(container_frame, 
                              text="Your Personalized Tasks",
                              font=('Segoe UI', 16, 'bold'),
                              foreground=COLORS['fg'])
        tasks_title.pack(pady=(0, 20))
        
        tasks_frame = ttk.Frame(container_frame)
        tasks_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas with scrollbar for tasks
        canvas = tk.Canvas(tasks_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(tasks_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Initialize task tracking variables
        self.task_vars = []
        self.task_checkboxes = []
        
        # Add tasks to the scrollable frame
        for task in tasks:
            if task:  # Skip empty lines
                if task.endswith(":"):  # Category headers
                    ttk.Label(scrollable_frame, text=task, 
                             font=('Segoe UI', 12, 'bold'),
                             foreground=COLORS['fg']).pack(pady=(15, 5))
                else:  # Task items
                    var = tk.BooleanVar(value=False)
                    self.task_vars.append(var)
                    cb = ttk.Checkbutton(scrollable_frame, text=task, 
                                      variable=var, 
                                      command=lambda v=var, t=task: self.update_task_progress(v, t),
                                      style='TCheckbutton')
                    cb.pack(anchor="w", padx=20, pady=5)
                    self.task_checkboxes.append(cb)
        
        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add progress tracking
        self.progress_frame = ttk.Frame(container_frame)
        self.progress_frame.pack(pady=20)
        
        self.progress_label = ttk.Label(self.progress_frame, 
                                      text="Task Progress: 0/12",
                                      font=('Segoe UI', 12),
                                      foreground=COLORS['fg'])
        self.progress_label.pack(side=tk.LEFT, padx=5)
        
        self.create_chart()
        
    def update_task_progress(self, var, task):
        completed = sum(1 for v in self.task_vars if v.get())
        total = len(self.task_vars)
        self.progress_label.config(text=f"Task Progress: {completed}/{total}")
        
        # Update the task in responses
        for response in self.responses:
            if response.get("task") == task:
                response["completed"] = var.get()
                break
        
        # Auto-save progress
        self.save_task_progress()
        
    def save_task_progress(self):
        try:
            progress = {
                "name": self.name.get(),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tasks": []
            }
            
            for i, (var, cb) in enumerate(zip(self.task_vars, self.task_checkboxes)):
                progress["tasks"].append({
                    "text": cb.cget("text"),
                    "completed": var.get()
                })
            
            # Save to a hidden file in the user's directory
            save_path = os.path.join(os.path.expanduser("~"), 
                                   ".personality_analyzer_tasks.json")
            with open(save_path, 'w') as f:
                json.dump(progress, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving task progress: {str(e)}")
            
    def load_task_progress(self):
        try:
            save_path = os.path.join(os.path.expanduser("~"), 
                                   ".personality_analyzer_tasks.json")
            if os.path.exists(save_path):
                with open(save_path, 'r') as f:
                    progress = json.load(f)
                
                # Only load if it's for the current user
                if progress.get("name") == self.name.get():
                    for task_data, var in zip(progress["tasks"], self.task_vars):
                        var.set(task_data["completed"])
                    
                    completed = sum(1 for v in self.task_vars if v.get())
                    total = len(self.task_vars)
                    self.progress_label.config(text=f"Task Progress: {completed}/{total}")
        except Exception as e:
            logging.error(f"Error loading task progress: {str(e)}")
        
    def analyze_results(self):
        if self.scores["📚 studying"] >= 1 and self.scores["🎨 hobbies"] == 0 and self.scores["💪 fitness"] == 0:
            return ("1. 📚 The Border Collie Scholar", 
                   "Like a Border Collie, you're highly intelligent and focused on learning. You excel in academic pursuits and enjoy mental challenges, but might need encouragement to take breaks and explore other activities.",
                   [
                       "🎨 Creative Tasks:",
                       "1. Try painting or drawing for 30 minutes",
                       "2. Learn to play a musical instrument",
                       "3. Write a short story or poem",
                       "4. Take a photography walk",
                       "",
                       "💪 Fitness Tasks:",
                       "5. Go for a 20-minute walk",
                       "6. Try yoga or stretching",
                       "7. Join a beginner's sports class",
                       "8. Do 10 minutes of home exercises",
                       "",
                       "📚 Study Balance:",
                       "9. Take regular study breaks",
                       "10. Set a timer for study sessions",
                       "11. Create a balanced daily schedule",
                       "12. Try studying in different environments"
                   ])
        elif self.scores["🎨 hobbies"] >= 1 and self.scores["📚 studying"] == 0 and self.scores["💪 fitness"] == 0:
            return ("2. 🎨 The Golden Retriever Creative", 
                   "Like a Golden Retriever, you're friendly, enthusiastic, and love engaging in creative activities. You bring joy to others through your hobbies and artistic pursuits, always ready to try something new and fun.",
                   [
                       "📚 Study Tasks:",
                       "1. Read a non-fiction book for 30 minutes",
                       "2. Take an online course in a new subject",
                       "3. Learn a new language basics",
                       "4. Study a topic you're curious about",
                       "5. Watch educational documentaries",
                       "6. Practice mental math exercises",
                       "",
                       "💪 Fitness Tasks:",
                       "7. Start with 10 minutes of daily exercise",
                       "8. Try a new sport or physical activity",
                       "9. Join a fitness class",
                       "",
                       "🎨 Creative Balance:",
                       "10. Set time limits for creative projects",
                       "11. Schedule regular study breaks",
                       "12. Create a balanced weekly routine"
                   ])
        elif self.scores["💪 fitness"] >= 1 and self.scores["📚 studying"] == 0 and self.scores["🎨 hobbies"] == 0:
            return ("3. 💪 The Siberian Husky Athlete", 
                   "Like a Siberian Husky, you're energetic, athletic, and love physical challenges. You thrive on exercise and outdoor activities, always ready for the next adventure or workout.",
                   [
                       "📚 Study Tasks:",
                       "1. Read for 20 minutes daily",
                       "2. Take an online course",
                       "3. Learn about nutrition and health",
                       "4. Study exercise science basics",
                       "5. Watch educational fitness videos",
                       "6. Read sports psychology articles",
                       "",
                       "🎨 Creative Tasks:",
                       "7. Try a creative hobby",
                       "8. Learn to cook healthy meals",
                       "9. Start a fitness journal",
                       "",
                       "💪 Fitness Balance:",
                       "10. Schedule rest days",
                       "11. Try different types of exercise",
                       "12. Set realistic fitness goals"
                   ])
        elif self.scores["📚 studying"] >= 1 and self.scores["🎨 hobbies"] >= 1 and self.scores["💪 fitness"] == 0:
            return ("4. 📚🎨 The Poodle Polymath", 
                   "Like a Poodle, you're both intelligent and creative. You excel in both academic and artistic pursuits, showing versatility and adaptability in your interests. You might need a nudge to get more physically active.",
                   [
                       "💪 Fitness Tasks:",
                       "1. Start with 10 minutes of daily exercise",
                       "2. Try yoga or stretching",
                       "3. Go for a 20-minute walk",
                       "4. Join a beginner's fitness class",
                       "5. Try home workout videos",
                       "6. Set step goals for the day",
                       "",
                       "📚 Study Balance:",
                       "7. Take active study breaks",
                       "8. Try studying while walking",
                       "9. Create an exercise schedule",
                       "",
                       "🎨 Creative Balance:",
                       "10. Combine art with movement",
                       "11. Try outdoor photography",
                       "12. Set fitness-related creative goals"
                   ])
        elif self.scores["📚 studying"] >= 1 and self.scores["💪 fitness"] >= 1 and self.scores["🎨 hobbies"] == 0:
            return ("5. 📚💪 The German Shepherd Scholar-Athlete", 
                   "Like a German Shepherd, you're both intelligent and physically capable. You excel in both academic and physical pursuits, showing discipline and dedication in everything you do. You might want to explore more creative outlets.",
                   [
                       "🎨 Creative Tasks:",
                       "1. Try drawing or painting",
                       "2. Learn to play an instrument",
                       "3. Start a creative journal",
                       "4. Take a photography class",
                       "5. Try creative writing",
                       "6. Explore digital art",
                       "",
                       "📚 Study Balance:",
                       "7. Study in creative environments",
                       "8. Try mind mapping for notes",
                       "9. Use creative study techniques",
                       "",
                       "💪 Fitness Balance:",
                       "10. Try creative movement",
                       "11. Join a dance class",
                       "12. Combine art with exercise"
                   ])
        elif self.scores["🎨 hobbies"] >= 1 and self.scores["💪 fitness"] >= 1 and self.scores["📚 studying"] == 0:
            return ("6. 🎨💪 The Labrador Adventurer", 
                   "Like a Labrador, you're both creative and athletic. You love exploring new hobbies and staying active, bringing energy and enthusiasm to everything you do. You might want to balance your activities with some academic pursuits.",
                   [
                       "📚 Study Tasks:",
                       "1. Read for 30 minutes daily",
                       "2. Take an online course",
                       "3. Learn about a new subject",
                       "4. Study exercise science",
                       "5. Read about art history",
                       "6. Learn about nutrition",
                       "7. Study time management",
                       "8. Read about psychology",
                       "",
                       "🎨 Creative Balance:",
                       "9. Set study goals",
                       "10. Create a study schedule",
                       "",
                       "💪 Fitness Balance:",
                       "11. Study while walking",
                       "12. Take active study breaks"
                   ])
        else:
            return ("🌟 The Mixed Breed All-Rounder", 
                   "Like a well-balanced mixed breed, you show interest in multiple areas, making you a versatile and well-rounded individual! You adapt well to different situations and can excel in various pursuits.",
                   [
                       "📚 Study Tasks:",
                       "1. Set specific learning goals",
                       "2. Try new study techniques",
                       "",
                       "🎨 Creative Tasks:",
                       "3. Explore new creative outlets",
                       "4. Challenge your artistic skills",
                       "",
                       "💪 Fitness Tasks:",
                       "5. Try new physical activities",
                       "6. Set fitness challenges",
                       "",
                       "🌟 Balance Tasks:",
                       "7. Create a weekly schedule",
                       "8. Track your progress",
                       "9. Set new goals regularly",
                       "10. Try cross-training activities",
                       "11. Maintain variety in activities",
                       "12. Review and adjust your routine"
                   ])
        
    def create_chart(self):
        # Clear previous chart if exists
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        fig = plt.figure(figsize=(8, 4), facecolor=COLORS['bg'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(COLORS['bg'])
        
        bars = ax.bar(self.scores.keys(), self.scores.values(), 
                     color=[COLORS['accent'], COLORS['success'], COLORS['warning']])
        
        plt.xticks(rotation=45, ha='right', color=COLORS['fg'])
        plt.yticks(color=COLORS['fg'])
        ax.set_ylabel("Interest Level", fontsize=10, color=COLORS['fg'])
        ax.set_title(f"{self.name.get()}'s Activity Preferences", 
                    fontsize=12, pad=20, color=COLORS['fg'])
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', color=COLORS['fg'])
        
        ax.grid(axis='y', linestyle='--', alpha=0.3, color=COLORS['fg'])
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def save_results(self):
        results = {
            "name": self.name.get(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": self.category_label.cget("text"),
            "description": self.description_label.cget("text"),
            "scores": self.scores,
            "responses": self.responses
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"personality_analysis_{self.name.get()}.json"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(results, f, indent=4)
                messagebox.showinfo("Success", "Results saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save results: {str(e)}")
                
    def load_results(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    results = json.load(f)
                
                self.name.set(results["name"])
                self.scores = results["scores"]
                self.responses = results["responses"]
                
                self.welcome_frame.pack_forget()
                self.question_frame.pack_forget()
                self.results_frame.pack(fill=tk.BOTH, expand=True)
                
                self.category_label.config(text=results["category"])
                self.description_label.config(text=results["description"])
                self.create_chart()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load results: {str(e)}")
                
    def start_over(self):
        self.current_question = 0
        self.scores = {
            "📚 studying": 0,
            "🎨 hobbies": 0,
            "💪 fitness": 0
        }
        self.responses = []
        
        self.results_frame.pack_forget()
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)
        
    def show_about(self):
        messagebox.showinfo("About", 
                          "Personality Analyzer v1.0\n\n"
                          "A tool to analyze your personality based on your preferences\n"
                          "for studying, hobbies, and fitness activities.")
        
    def show_help(self):
        help_text = """
        Personality Analyzer Help
        
        1. Enter your name and click 'Start Analysis'
        2. Answer each question with Yes or No
        3. View your results and category
        4. Save your results for future reference
        5. Load previous results if needed
        
        The analysis is based on your preferences in three areas:
        - 📚 Studying and learning
        - 🎨 Hobbies and creative activities
        - 💪 Fitness and physical activities
        """
        messagebox.showinfo("Help", help_text)

def main():
    try:
        logging.info("Starting application")
        root = tk.Tk()
        app = PersonalityAnalyzer(root)
        root.mainloop()
except Exception as e:
        logging.error(f"Critical error in main: {str(e)}")
        logging.error(traceback.format_exc())
        print(f"An error occurred: {str(e)}")
    traceback.print_exc()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()