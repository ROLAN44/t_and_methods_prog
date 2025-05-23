import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from models import Course, Assignment, AssignmentStatus
from distributor import Distributor


class AssignmentApp:
    """GUI application for managing assignments."""
    def __init__(self, root: tk.Tk, course: Course, default_file: str = "assignments.txt"):
        self._root = root
        self._course = course
        self._default_file = default_file  # Путь к файлу по умолчанию
        self._root.title(f"Управление заданиями - {course.course_name}")
        self._status_translations = {
            AssignmentStatus.PENDING.value: "Ожидает",
            AssignmentStatus.SUBMITTED.value: "Сдано",
            AssignmentStatus.GRADED.value: "Оценено"
        }
        self._setup_ui()

    def _setup_ui(self):
        """Set up the GUI components."""
        # Table
        self._tree = ttk.Treeview(self._root, columns=("Name", "Theme", "Date", "Status", "Grade"), show="headings")
        self._tree.heading("Name", text="ФИО")
        self._tree.heading("Theme", text="Тема")
        self._tree.heading("Date", text="Дата выдачи")
        self._tree.heading("Status", text="Статус")
        self._tree.heading("Grade", text="Оценка")
        self._tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input frame for adding assignments
        input_frame = ttk.Frame(self._root)
        input_frame.pack(pady=5, fill=tk.X)

        ttk.Label(input_frame, text="ФИО:").grid(row=0, column=0, padx=5)
        self._name_entry = ttk.Entry(input_frame)
        self._name_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Тема:").grid(row=0, column=2, padx=5)
        self._theme_entry = ttk.Entry(input_frame)
        self._theme_entry.grid(row=0, column=3, padx=5)

        ttk.Label(input_frame, text="Дата (ГГГГ.ММ.ДД):").grid(row=0, column=4, padx=5)
        self._date_entry = ttk.Entry(input_frame)
        self._date_entry.grid(row=0, column=5, padx=5)

        ttk.Button(input_frame, text="Добавить", command=self._add_assignment).grid(row=0, column=6, padx=5)

        # Frame for status and grade modification
        modify_frame = ttk.Frame(self._root)
        modify_frame.pack(pady=5, fill=tk.X)

        ttk.Label(modify_frame, text="Статус:").grid(row=0, column=0, padx=5)
        self._status_var = tk.StringVar()
        self._status_combobox = ttk.Combobox(modify_frame, textvariable=self._status_var,
                                             values=list(self._status_translations.values()))
        self._status_combobox.grid(row=0, column=1, padx=5)

        ttk.Label(modify_frame, text="Оценка (0-100):").grid(row=0, column=2, padx=5)
        self._grade_entry = ttk.Entry(modify_frame)
        self._grade_entry.grid(row=0, column=3, padx=5)

        ttk.Button(modify_frame, text="Изменить статус/оценку", command=self._modify_assignment).grid(row=0, column=4, padx=5)

        # Buttons for delete, load, and save
        ttk.Button(self._root, text="Удалить выбранное", command=self._delete_assignment).pack(pady=5)
        ttk.Button(self._root, text="Загрузить из файла", command=self._load_from_file).pack(pady=5)
        ttk.Button(self._root, text="Сохранить в файл", command=self._save_to_file).pack(pady=5)

        self._update_table()

    def _add_assignment(self):
        """Add a new assignment from input fields."""
        try:
            name = self._name_entry.get()
            theme = self._theme_entry.get()
            date_str = self._date_entry.get()
            date = datetime.strptime(date_str, '%Y.%m.%d')
            assignment = Assignment(name, theme, date)
            self._course.add_assignment(assignment)
            self._update_table()
            self._name_entry.delete(0, tk.END)
            self._theme_entry.delete(0, tk.END)
            self._date_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def _delete_assignment(self):
        """Delete the selected assignment."""
        selected = self._tree.selection()
        if selected:
            index = int(self._tree.index(selected[0]))
            self._course.remove_assignment(index)
            self._update_table()
        else:
            messagebox.showwarning("Предупреждение", "Выберите задание для удаления")

    def _modify_assignment(self):
        """Modify the status and/or grade of the selected assignment."""
        selected = self._tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите задание для изменения")
            return

        index = int(self._tree.index(selected[0]))
        assignment = self._course.get_assignments()[index]

        try:
            # Update status if selected
            status_value = self._status_var.get()
            if status_value:
                for eng_status, rus_status in self._status_translations.items():
                    if rus_status == status_value:
                        for status in AssignmentStatus:
                            if status.value == eng_status:
                                assignment.update_status(status)
                                break
                        break

            # Update grade if provided
            grade_str = self._grade_entry.get()
            if grade_str:
                grade = float(grade_str)
                assignment.set_grade(grade)

            self._update_table()
            self._status_var.set("")  # Clear status selection
            self._grade_entry.delete(0, tk.END)  # Clear grade entry
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def _load_from_file(self):
        """Load assignments from a file."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                self._course.get_assignments().clear()  # Очищаем текущие задания
                Distributor.create_from_file(file_path, self._course)
                self._default_file = file_path  # Обновляем путь к файлу
                self._update_table()
            except (FileNotFoundError, ValueError) as e:
                messagebox.showerror("Ошибка", str(e))

    def _save_to_file(self):
        """Save assignments to a file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                Distributor.save_to_file(file_path, self._course)
                self._default_file = file_path
                messagebox.showinfo("Успех", f"Данные сохранены в {file_path}")
            except IOError as e:
                messagebox.showerror("Ошибка", str(e))

    def _update_table(self):
        """Update the table with current assignments."""
        for item in self._tree.get_children():
            self._tree.delete(item)
        for assignment in self._course.get_assignments():
            self._tree.insert("", tk.END, values=(
                assignment.student_name,
                assignment.theme_name,
                assignment.issue_date.strftime('%Y.%m.%d'),
                self._status_translations.get(assignment.status.value, assignment.status.value),
                assignment.grade if assignment.grade is not None else ""
            ))

    def run(self):
        """Run the application."""
        self._root.mainloop()