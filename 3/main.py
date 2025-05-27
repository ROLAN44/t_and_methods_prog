import tkinter as tk
from models import Course
from gui import AssignmentApp


def main():
    """Main function to start the application."""
    course = Course("Программирование на Python", "Иванов И.И.")
    root = tk.Tk()
    app = AssignmentApp(root, course, default_file="assignments.txt")
    app.run()


if __name__ == "__main__":
    main()