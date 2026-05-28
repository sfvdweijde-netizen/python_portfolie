import tkinter as tk
from tkinter import messagebox, ttk
import os

TODO_FILE = "todo.txt"


def load_tasks() -> list:
    tasks = []
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line and "|" in line:
                    parts = line.split("|", 2)
                    if len(parts) == 3:
                        tasks.append({"status": parts[0], "priority": parts[1], "description": parts[2]})
    return tasks


def save_tasks(tasks: list):
    with open(TODO_FILE, "w") as file:
        for task in tasks:
            file.write(f"{task['status']}|{task['priority']}|{task['description']}\n")


def sort_key(task: dict) -> tuple:
    status_order = 0 if task["status"] == "Todo" else 1
    priority_order = {"High": 0, "Medium": 1, "Low": 2}.get(task["priority"], 3)
    return (status_order, priority_order)


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart To-Do List")
        self.root.geometry("450x500")
        self.root.resizable(False, False)

        self.tasks = load_tasks()
        self.create_widgets()
        self.refresh_list()

    def create_widgets(self):
        # --- Top Section: Input ---
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="Task:").grid(row=0, column=0, sticky=tk.W)
        self.task_entry = tk.Entry(input_frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Priority:").grid(row=1, column=0, sticky=tk.W)
        self.prio_combo = ttk.Combobox(input_frame, values=["High", "Medium", "Low"], width=12, state="readonly")
        self.prio_combo.set("Medium")
        self.prio_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        add_btn = tk.Button(input_frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white", padx=10)
        add_btn.grid(row=0, column=2, rowspan=2, padx=5, sticky=tk.NSEW)

        # --- Middle Section: Task List ---
        list_frame = tk.Frame(self.root, padx=10, pady=5)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(list_frame, font=("Courier", 10), selectmode=tk.SINGLE)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # --- Bottom Section: Action Buttons ---
        btn_frame = tk.Frame(self.root, padx=10, pady=10)
        btn_frame.pack(fill=tk.X)

        toggle_btn = tk.Button(btn_frame, text="Toggle Done/Todo", command=self.toggle_task, width=18)
        toggle_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(btn_frame, text="Delete Task", command=self.delete_task, fg="red", width=12)
        delete_btn.pack(side=tk.RIGHT, padx=5)

    def refresh_list(self):
        self.task_listbox.delete(0, tk.END)
        self.tasks.sort(key=sort_key)
        for task in self.tasks:
            icon = "[X]" if task["status"] == "Done" else "[ ]"
            display_text = f"{icon} ({task['priority']:<6}) {task['description']}"
            self.task_listbox.insert(tk.END, display_text)

    def add_task(self):
        desc = self.task_entry.get().strip()
        prio = self.prio_combo.get()
        if desc:
            self.tasks.append({"status": "Todo", "priority": prio, "description": desc})
            save_tasks(self.tasks)
            self.refresh_list()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task description cannot be empty!")

    def toggle_task(self):
        try:
            selected_idx = self.task_listbox.curselection()[0]
            task = self.tasks[selected_idx]
            task["status"] = "Done" if task["status"] == "Todo" else "Todo"
            save_tasks(self.tasks)
            self.refresh_list()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task first!")

    def delete_task(self):
        try:
            selected_idx = self.task_listbox.curselection()[0]
            self.tasks.pop(selected_idx)
            save_tasks(self.tasks)
            self.refresh_list()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task first!")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
