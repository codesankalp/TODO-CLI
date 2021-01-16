import sys
from datetime import datetime as dt
from os import getcwd, path


class Todo:
    """Class Todo:
    A class for making TODO list.
    Methods :-
    add(task)               # Add a new todo
    ls()                    # Show remaining todos
    delete(task_number)     # Delete a todo
    done(task_number)       # Complete a todo
    help()                  # Show usage
    report()                # Statistics
    """

    def __init__(self):
        """Constructor for making `todo.txt` and `done.txt` in working directory."""
        self.curr_dir = getcwd()
        self.todo_path = path.join(self.curr_dir, "todo.txt")
        self.done_path = path.join(self.curr_dir, "done.txt")
        self.today_date = dt.now().strftime("%Y-%m-%d")
        if not path.exists(self.todo_path):
            handle = open(self.todo_path, "w")
            handle.close()
        if not path.exists(self.done_path):
            handle = open(self.done_path, "w")
            handle.close()

    def help(self):
        """Prints Usage or Help for using todo-list."""
        help_text = [
            "Usage :-",
            '$ ./todo add "todo item"  # Add a new todo',
            "$ ./todo ls               # Show remaining todos",
            "$ ./todo del NUMBER       # Delete a todo",
            "$ ./todo done NUMBER      # Complete a todo",
            "$ ./todo help             # Show usage",
            "$ ./todo report           # Statistics\n",
        ]
        sys.stdout.write("\n".join(help_text))

    def ls(self):
        """List all pendings todos."""
        with open(self.todo_path, "r") as f:
            tasks = f.readlines()
            # if there are no pending tasks.
            if tasks == []:
                sys.stdout.write("There are no pending todos!\n")
            # listing todo from recent one to older one.
            else:
                for task_num in range(len(tasks), 0, -1):
                    sys.stdout.write(
                        "[{}] {}\n".format(task_num, tasks[task_num - 1].strip("\n"))
                    )

    def add(self, task):
        """Add a todo with task as an argument"""
        with open(self.todo_path, "r+") as f:
            tasks = f.readlines()
            # if there are no tasks i.e. todo.txt is empty.
            if tasks == []:
                f.write(task)
            # else adding new line and then adding the task.
            else:
                f.write("\n" + task)
        sys.stdout.write('Added todo: "{}"\n'.format(task))

    def delete(self, task_no):
        """Delete a todo with task number as an argument."""
        # raise error if task_no cannot be type converted into integer.
        try:
            task_no = int(task_no)
        except Exception:
            sys.stderr.write(
                "Please provide task number instead of {}\n".format(task_no)
            )
            sys.exit(1)

        with open(self.todo_path, "r") as f:
            tasks = f.readlines()

        try:
            # if task number is less than 0 then raise error.
            if task_no <= 0:
                raise Exception
            # remove the todo with task number given.
            tasks.remove(tasks[task_no - 1])

            with open(self.todo_path, "w") as f:
                f.write("".join(tasks))

            print("Deleted todo #{}".format(task_no))

        except Exception:
            sys.stdout.write(
                "Error: todo #{} does not exist. Nothing deleted.\n".format(task_no)
            )

    def done(self, task_no):
        """Mark done a todo with task number as an argument."""
        # raise error if task_no cannot be type converted into integer.
        try:
            task_no = int(task_no)
        except Exception:
            sys.stderr.write(
                "Please provide task number instead of {}\n".format(task_no)
            )
            sys.exit(1)

        with open(self.todo_path, "r") as f:
            tasks = f.readlines()

        try:
            if task_no <= 0:
                raise Exception
            done = tasks[task_no - 1].strip("\n")
            with open(self.done_path, "r+") as f:
                tasks_done = f.readlines()
                # if done.txt is empty.
                if tasks_done == []:
                    f.write("x {} {}".format(self.today_date, done))
                # else new line character at the end of line.
                else:
                    f.write("\nx {} {}".format(self.today_date, done))

            # remove the todo with task number given.
            tasks.remove(tasks[task_no - 1])
            with open(self.todo_path, "w") as f:
                f.write("".join(tasks))

            sys.stdout.write("Marked todo #{} as done.\n".format(task_no))

        except Exception:
            sys.stdout.write("Error: todo #{} does not exist.\n".format(task_no))

    def report(self):
        """Statistics of the pending and completed todo."""
        with open(self.done_path, "r") as f:
            task_done = len(f.readlines())
        with open(self.todo_path, "r") as f:
            tasks = len(f.readlines())
        sys.stdout.write(
            "{} Pending : {} Completed : {}\n".format(self.today_date, tasks, task_done)
        )


if __name__ == "__main__":
    arguments = sys.argv
    todo = Todo()
    if len(arguments) == 1 or arguments[1] == "help":
        todo.help()
    elif arguments[1] == "ls":
        todo.ls()
    elif arguments[1] == "add":
        try:
            todo.add(arguments[2])
        except Exception:
            sys.stdout.write("Error: Missing todo string. Nothing added!\n")
    elif arguments[1] == "del":
        try:
            todo.delete(arguments[2])
        except Exception:
            sys.stdout.write("Error: Missing NUMBER for deleting todo.\n")
    elif arguments[1] == "done":
        try:
            todo.done(arguments[2])
        except Exception:
            sys.stdout.write("Error: Missing NUMBER for marking todo as done.\n")
    elif arguments[1] == "report":
        todo.report()
    else:
        sys.stderr.write("{}, command not found.\n".format(arguments[1]))
        sys.exit(1)
