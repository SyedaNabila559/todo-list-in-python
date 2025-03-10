import click
import json
import os

# Define the file where the tasks will be saved
TASKS_FILE = 'tasks.json'

# Load tasks from the JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

# Save tasks to the JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Add a new task
@click.command()
@click.argument('task')
def add_task(task):
    tasks = load_tasks()
    tasks.append({"task": task, "done": False})
    save_tasks(tasks)
    click.echo(f"✅ Task '{task}' added to your list!")

# List all tasks
@click.command()
def list_tasks():
    tasks = load_tasks()
    if not tasks:
        click.echo("❌ No tasks in the list!")
        return
    for idx, task in enumerate(tasks, 1):
        status = "✅ Done" if task["done"] else "❌ Pending"
        click.echo(f"{idx}. {task['task']} - {status}")

# Mark a task as completed
@click.command()
@click.argument('task_number', type=int)
def mark_done(task_number):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]["done"] = True
        save_tasks(tasks)
        click.echo(f"✅ Task {task_number} marked as completed!")
    else:
        click.echo("❌ Task number is invalid!")

# Update a task
@click.command()
@click.argument('task_number', type=int)
@click.argument('new_task')
def update_task(task_number, new_task):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        old_task = tasks[task_number - 1]["task"]
        tasks[task_number - 1]["task"] = new_task
        save_tasks(tasks)
        click.echo(f"🔄 Task {task_number} updated from '{old_task}' to '{new_task}'")
    else:
        click.echo("❌ Task number is invalid!")

# Delete a task
@click.command()
@click.argument('task_number', type=int)
def delete_task(task_number):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        deleted_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        click.echo(f"🗑️ Task '{deleted_task['task']}' deleted!")
    else:
        click.echo("❌ Task number is invalid!")

# Main entry point
@click.group()
def cli():
    """Simple To-Do List Application"""
    pass

# Add commands to the CLI group
cli.add_command(add_task)
cli.add_command(list_tasks)
cli.add_command(mark_done)
cli.add_command(update_task)
cli.add_command(delete_task)

if __name__ == '__main__':
    cli()
