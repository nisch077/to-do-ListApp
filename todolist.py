import json
import os

def load_tasks(filename="tasks.json"):
    """Loads tasks from a json file"""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks, filename="tasks.json"):
    """Saves tasks to a json file"""
    with open(filename, "w") as f:
        json.dump(tasks, f)

def add_task(tasks, task):
    """Adds a new task to the list."""
    tasks.append({"task": task, "completed": False})
    print(f'Task "{task}" added.')

def view_tasks(tasks):
    """Displays the current list of tasks."""
    if not tasks:
        print("No tasks found.")
        return
    
    print("Tasks:")
    for i, task_data in enumerate(tasks):
        status = "[X]" if task_data["completed"] else "[ ]"
        print(f"{i + 1}. {status} {task_data['task']}")
    
def mark_completed(tasks, task_number):
    """Marks a task as completed."""
    if 1 <= task_number <= len(tasks):
        tasks[task_number - 1]["completed"] = True
        print(f'Task {task_number} marked as completed.')
    else:
        print("Invalid task number.")

def remove_task(tasks, task_number):
    """Removes a task from the list."""
    if 1 <= task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        print(f'Task "{removed_task["task"]}" removed.')
    else:
        print("Invalid task number.")

def main():
    """Main function to run the To-Do List application."""
    tasks = load_tasks()

    while True:
        print("\nOptions:")
        print("1. Add task")
        print("2. View tasks")
        print("3. Mark task as completed")
        print("4. Remove task")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            task = input("Enter task: ")
            add_task(tasks, task)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            try:
                task_number = int(input("Enter task number to mark as completed: "))
                mark_completed(tasks, task_number)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "4":
            try:
                task_number = int(input("Enter task number to remove: "))
                remove_task(tasks, task_number)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "5":
            save_tasks(tasks)
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
    
if __name__ == "__main__":
    main()