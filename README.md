# To-Do List Application (CLI and GUI)

This repository contains a To-Do List application implemented in Python, offering both a command-line interface (CLI) and a graphical user interface (GUI).

## Features

* **CLI Version:**
    * Add, view, mark as completed, and remove tasks.
    * Save and load tasks from a `tasks.json` file.
* **GUI Version:**
    * All CLI features, plus:
    * Due date functionality.
    * Task editing.
    * Clear completed tasks.
    * Keyboard shortcuts (Ctrl+Enter to add, Delete to remove).
    * Tooltips for buttons.
    * Status bar.
    * Confirmation dialogs for task removal.
    * Drag-and-drop task reordering.
    * Save and load tasks from a `tasksGUI.json` file.

## Files

* `todolist.py`: The command-line version of the application.
* `todolistGUI.py`: The graphical user interface version of the application.
* `tasks.json`: Data file for the CLI version.
* `tasksGUI.json`: Data file for the GUI version.
* `README.md`: This file.
* `.gitignore`: Specifies files Git should ignore.

## How to Run

### CLI Version

1.  Ensure you have Python installed.
2.  Navigate to the directory containing `todolist.py` in your terminal.
3.  Run `python todolist.py`.

### GUI Version

1.  Ensure you have Python and Tkinter installed (Tkinter is usually included with Python).
2.  Navigate to the directory containing `todolistGUI.py` in your terminal.
3.  Run `python todolistGUI.py`.

## Dependencies

* Python 3.x
* Tkinter (for the GUI version)

## Usage

### CLI

* Follow the prompts in the terminal to interact with the application.

### GUI

* Use the buttons and input fields in the graphical window to manage your tasks.
* Use Ctrl+Enter to add a new task.
* Use the Delete key to remove the selected task.
* Drag and drop tasks in the list to reorder them.

## Contributing

Feel free to contribute to this project by submitting pull requests or opening issues.