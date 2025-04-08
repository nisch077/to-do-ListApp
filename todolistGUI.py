import tkinter as tk
from tkinter import ttk, font, messagebox
import json
import os
from datetime import datetime

def load_tasks(filename="tasksGUI.json"):
    """Loads tasks from a JSON file."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks, filename="tasksGUI.json"):
    """Saves tasks to a JSON file."""
    with open(filename, "w") as f:
        json.dump(tasks, f)

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip_window, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.configure(bg="#f0f0f0")  # Light gray background

        self.tasks = load_tasks()

        # Custom Fonts
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.task_font = font.Font(family="Arial", size=12)

        # Title Label
        self.title_label = tk.Label(root, text="My To-Do List", font=self.title_font, bg="#f0f0f0")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Task Entry
        self.task_entry = tk.Entry(root, width=40, font=self.task_font)
        self.task_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        #Date Entry
        self.due_date_entry = tk.Entry(root, width=15, font=self.task_font)
        self.due_date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.due_date_entry.insert(0,"YYYY-MM-DD") #initial text

        # Add Button
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white", font=self.task_font)
        self.add_button.grid(row=1, column=2, padx=10, pady=5) # No sticky here

        # Listbox and Scrollbar
        self.listbox_frame = tk.Frame(root, bg="#f0f0f0")
        self.listbox_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.listbox_scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.listbox_frame, width=50, font=self.task_font, yscrollcommand=self.listbox_scrollbar.set)
        self.listbox_scrollbar.config(command=self.listbox.yview)

        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.listbox_scrollbar.grid(row=0, column=1, sticky="ns")

        self.listbox_frame.grid_rowconfigure(0, weight=1)
        self.listbox_frame.grid_columnconfigure(0, weight=1)

        # Completed Button
        self.completed_button = tk.Button(root, text="Mark Completed", command=self.mark_completed, bg="#2196F3", fg="white", font=self.task_font)
        self.completed_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # Remove Button
        self.remove_button = tk.Button(root, text="Remove Task", command=self.remove_task, bg="#f44336", fg="white", font=self.task_font)
        self.remove_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        #Clear Completed Button
        self.clear_completed_button = tk.Button(root, text="Clear Completed", command=self.clear_completed, bg="#9E9E9E", fg="white", font=self.task_font)
        self.clear_completed_button.grid(row=3, column=2, padx=10, pady=5, sticky="ew")

        # Status Bar
        self.status_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=4, column=0, columnspan=3, sticky="ew")

        # Configure Grid Weights
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        self.listbox.bind("<Double-1>", self.edit_task) # double click edit
        self.listbox.bind("<Button-1>", self.drag_start)
        self.listbox.bind("<B1-Motion>", self.drag_motion)
        self.listbox.bind("<ButtonRelease-1>", self.drag_stop)

        self.dragged_item = None

        # Keyboard Shortcuts
        root.bind("<Control-Return>", lambda event: self.add_task())
        self.listbox.bind("<Delete>", self.remove_task) # bind to listbox

        # Tooltips
        ToolTip(self.add_button, "Add a new task (Ctrl+Enter)")
        ToolTip(self.remove_button, "Remove selected task (Delete)")
        ToolTip(self.completed_button, "Mark selected task as completed")
        ToolTip(self.clear_completed_button, "Remove completed tasks")

        self.update_listbox()

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def drag_start(self, event):
        self.dragged_item = self.listbox.nearest(event.y)

    def drag_motion(self, event):
        if self.dragged_item is None:
            return
        
        y = event.y
        new_index = self.listbox.nearest(y)

        if new_index != self.dragged_item:
            self.tasks.insert(new_index, self.tasks.pop(self.dragged_item))
            self.dragged_item = new_index
            self.update_listbox()
    
    def drag_stop(self, event):
        self.dragged_item = None
    
    def add_task(self):
        task = self.task_entry.get()
        due_date = self.due_date_entry.get()
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            due_date = "N/A"
        if task:
            self.tasks.append({"task": task, "completed": False, "due_date": due_date})
            self.task_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.insert(0,"YYYY-MM-DD")
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for task_data in self.tasks:
            status = "[X]" if task_data["completed"] else "[ ]"
            self.listbox.insert(tk.END, f"{status} {task_data['task']} (Due: {task_data['due_date']})")
    
    def mark_completed(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.tasks[selected_index[0]]["completed"] = True
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task.")
    
    def remove_task(self, event=None): # takes event
        selected_index = self.listbox.curselection()
        if selected_index:
            result = messagebox.askyesno("Confirm", "Are you sure you want to remove this task?")
            if result:
                del self.tasks[selected_index[0]]
                self.update_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task.")

    def edit_task(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            task_data = self.tasks[selected_index[0]]
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Task")

            task_label = tk.Label(edit_window, text="Task:")
            task_label.pack()
            task_entry = tk.Entry(edit_window, width=40)
            task_entry.insert(0, task_data["task"])
            task_entry.pack()

            due_date_label = tk.Label(edit_window, text="Due Date:")
            due_date_label.pack()
            due_date_entry = tk.Entry(edit_window, width=15)
            due_date_entry.insert(0, task_data["due_date"])
            due_date_entry.pack()

            def save_edit():
                task_data["task"] = task_entry.get()
                task_data["due_date"] = due_date_entry.get()
                self.update_listbox()
                edit_window.destroy()

            save_button = tk.Button(edit_window, text="Save", command=save_edit)
            save_button.pack()
    
    def clear_completed(self):
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.update_listbox()

    def on_closing(self):
        save_tasks(self.tasks)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()