from datetime import datetime

# Memento Pattern: TaskM
class TaskM:
    def __init__(self, task):
        self.task = task

# Builder Pattern: TaskB
class TaskB:
    def __init__(self, description):
        self.description = description
        self.due_date = None
        self.tags = []

    def set_due_date(self, due_date):
        self.due_date = due_date
        return self

    def add_tag(self, *tags):
        self.tags.extend(tags)
        return self

    def build(self):
        return Task(self)

# Task class with encapsulated data and methods
class Task:
    def __init__(self, builder):
        self.description = builder.description
        self.due_date = builder.due_date
        self.tags = builder.tags
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        due_date_str = f", Due: {self.due_date}" if self.due_date else ""
        tags_str = f", Tags: {', '.join(self.tags)}" if self.tags else ""
        return f"{self.description} - {status}{due_date_str}{tags_str}"

# To-Do List Manager
class ToDoListM:
    def __init__(self):
        self.tasks = []
        self.undo_stack = []
        self.redo_stack = []

    def add_task(self, task):
        self.tasks.append(task)
        self.undo_stack.append(TaskM(task))
        self.redo_stack.clear()

    def mark_completed(self, description):
        for task in self.tasks:
            if task.description == description:
                task.mark_completed()
                self.undo_stack.append(TaskM(task))
                self.redo_stack.clear()
                return

    def delete_task(self, description):
        task_to_delete = None
        for task in self.tasks:
            if task.description == description:
                task_to_delete = task
                break

        if task_to_delete:
            self.undo_stack.append(TaskM(task_to_delete))  # Capture the task state before deletion
            self.tasks.remove(task_to_delete)
            self.redo_stack.clear()
        else:
            print(f"Task '{description}' not found.")

    def view_tasks(self, filter_type):
        if filter_type == "Show all":
            return self.tasks
        elif filter_type == "Show completed":
            return [task for task in self.tasks if task.completed]
        elif filter_type == "Show pending":
            return [task for task in self.tasks if not task.completed]

    def undo(self):
        if self.undo_stack:
            task_memento = self.undo_stack.pop()
            if task_memento:
                self.redo_stack.append(TaskM(task_memento.task))
                self.tasks.append(task_memento.task)  # Add the task back
            else:
                # Handle undo of deletion (remove the task again)
                task_to_remove = self.redo_stack.pop().task
                self.tasks.remove(task_to_remove)


    def redo(self):
        if self.redo_stack:
            task_memento = self.redo_stack.pop()
            if task_memento:
                self.undo_stack.append(TaskM(task_memento.task))
                self.tasks.remove(task_memento.task)  # Remove the task again
            else:
                # Handle redo of restoration (add the task back)
                task_to_restore = self.undo_stack.pop().task
                self.tasks.append(task_to_restore)



# Example usage
if __name__ == "__main__":
    manager = ToDoListM()

    while True:
        print("\nTo-Do List Manager Menu:")
        print("1. Add Task")
        print("2. Mark Task as Completed")
        print("3. Delete Task")
        print("4. View Tasks")
        print("5. Undo")
        print("6. Redo")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter task description: ")
            due_date_input = input("Enter due date (YYYY-MM-DD), if any (press Enter to skip): ")
            due_date = datetime.strptime(due_date_input, "%Y-%m-%d") if due_date_input else None
            tags = input("Enter tags, separated by commas (press Enter to skip): ").split(",") if due_date_input else []
            
            task = TaskB(description).set_due_date(due_date).add_tag(*tags).build()
            manager.add_task(task)
            print("Task added successfully!")

        elif choice == "2":
            description = input("Enter task description to mark as completed: ")
            manager.mark_completed(description)
            print(f"Task '{description}' marked as completed!")

        elif choice == "3":
            description = input("Enter task description to delete: ")
            manager.delete_task(description)
            print(f"Task '{description}' deleted!")

        elif choice == "4":
            filter_type = input("Enter filter type (Show all/Show completed/Show pending): ")
            tasks = manager.view_tasks(filter_type)
            print(f"\n{filter_type} tasks:")
            for task in tasks:
                print(task)

        elif choice == "5":
            manager.undo()
            print("Undo successful!")

        elif choice == "6":
            manager.redo()
            print("Redo successful!")

        elif choice == "7":
            print("Exiting the To-Do List Manager.")
            break

        else:
            print("Invalid choice. Please select a valid option.")
