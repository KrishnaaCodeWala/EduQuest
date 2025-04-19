import tkinter as tk
from tkinter import messagebox, ttk
import json

class StudentForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Academic Questionnaire")
        self.geometry("700x700")
        self.entries = {}
        self.create_form()

    def create_form(self):
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        row = 0

        def add_entry(label, key, is_multiline=False):
            nonlocal row
            tk.Label(scrollable_frame, text=label, anchor='w').grid(row=row, column=0, sticky='w', pady=4)
            if is_multiline:
                entry = tk.Text(scrollable_frame, height=4, width=60)
            else:
                entry = tk.Entry(scrollable_frame, width=60)
            entry.grid(row=row, column=1, pady=4)
            self.entries[key] = entry
            row += 1

        def add_multiselect(label, key, options):
            nonlocal row
            tk.Label(scrollable_frame, text=label, anchor='w').grid(row=row, column=0, sticky='w', pady=4)
            vars_list = []
            for i, option in enumerate(options):
                var = tk.BooleanVar()
                chk = tk.Checkbutton(scrollable_frame, text=option, variable=var)
                chk.grid(row=row, column=1, sticky='w', padx=20)
                row += 1
                vars_list.append((option, var))
            self.entries[key] = vars_list

        # Basic Info
        add_entry("Full Name", "name")
        add_entry("Email (optional)", "email")
        add_entry("Class/Grade", "class")
        add_entry("Institution (optional)", "institution")

        # Subjects
        add_entry("Subjects you're studying (comma separated)", "subjects")
        add_entry("Subjects you find interesting", "interests")
        add_entry("Subjects you need help with", "needs_help_with")
        add_entry("Are there upcoming exams/assignments? Describe:", "exam_preparation", is_multiline=True)

        # Study Habits
        add_multiselect("Study hours per day", "study_hours_per_day", [
            "Less than 1 hour", "1-2 hours", "2-4 hours", "More than 4 hours"
        ])

        add_multiselect("Preferred study time", "study_time_preference", [
            "Morning", "Afternoon", "Evening", "Late night"
        ])

        add_entry("Do you follow a timetable? If yes, describe:", "study_plan")

        add_multiselect("Do you study alone or in groups?", "study_mode", [
            "Alone", "In a group", "Both"
        ])

        add_multiselect("Study resources used:", "study_resources", [
            "Textbooks", "Online courses", "YouTube tutorials", "Coaching/tutors",
            "Study apps", "College/School Notes", "Others"
        ])

        # Learning Preferences
        add_multiselect("Preferred learning style:", "learning_preference", [
            "Step-by-step explanation", "Visual aids", "Practice problems",
            "Real-life examples", "Group discussion"
        ])
        add_entry("Topics you need help with right now", "current_difficult_topics")
        add_multiselect("What do you want help with?", "support_needed", [
            "Understanding concepts", "Solving problems", "Making study plans",
            "Time management", "All of the above"
        ])

        # Goals & Motivation
        add_entry("Short-term academic goals", "short_term_goals")
        add_entry("Long-term goal (if any)", "long_term_goal")
        add_entry("What motivates you to study?", "motivation")

        # Support Preferences
        add_multiselect("How often would you like support?", "help_frequency", [
            "Daily", "Few times a week", "Weekly", "Occasionally"
        ])
        add_multiselect("Interested in:", "interested_in", [
            "Personalized study suggestions", "Reminders and schedules",
            "Practice quizzes", "Peer study groups", "Revision tools", "All of the above"
        ])

        submit_btn = tk.Button(scrollable_frame, text="Submit", command=self.save_data, bg="#4CAF50", fg="white")
        submit_btn.grid(row=row+1, column=0, columnspan=2, pady=20)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def save_data(self):
        data = {}
        for key, widget in self.entries.items():
            if isinstance(widget, list):
                # multiselect checkboxes
                data[key] = [label for label, var in widget if var.get()]
            elif isinstance(widget, tk.Text):
                data[key] = widget.get("1.0", tk.END).strip()
            else:
                data[key] = widget.get().strip()

        try:
            with open("student_data_gui.json", "w") as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Success", "Data saved to student_data_gui.json!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

if __name__ == "__main__":
    app = StudentForm()
    app.mainloop()
