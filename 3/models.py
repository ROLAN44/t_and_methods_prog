from datetime import datetime
from enum import Enum
from typing import List


class AssignmentStatus(Enum):
    """Статусы задания."""
    PENDING = "Pending"
    SUBMITTED = "Submitted"
    GRADED = "Graded"


class AssignmentBase:
    """Базовый класс для хранения информации о задании."""
    
    def __init__(self, student_name: str, theme_name: str, issue_date: datetime):
        """Инициализация базового задания.

        Args:
            student_name: Имя студента.
            theme_name: Название темы задания.
            issue_date: Дата выдачи задания.
        """
        self.student_name = student_name
        self.theme_name = theme_name
        self.issue_date = issue_date

    def __str__(self) -> str:
        """Строковое представление задания."""
        return (f"Студент: {self.student_name}, Тема: {self.theme_name}, "
                f"Дата выдачи: {self.issue_date.strftime('%Y.%m.%d')}")


class Assignment(AssignmentBase):
    """Класс задания с дополнительными атрибутами статуса и оценки."""
    
    def __init__(self, student_name: str, theme_name: str, issue_date: datetime,
                 status: AssignmentStatus = AssignmentStatus.PENDING,
                 grade: float | None = None):
        """Инициализация задания.

        Args:
            student_name: Имя студента.
            theme_name: Название темы задания.
            issue_date: Дата выдачи задания.
            status: Статус задания (по умолчанию PENDING).
            grade: Оценка за задание (по умолчанию None).
        """
        super().__init__(student_name, theme_name, issue_date)
        self.status = status
        self.grade = grade

    def update_status(self, new_status: AssignmentStatus) -> None:
        """Обновление статуса задания.

        Args:
            new_status: Новый статус задания.
        """
        self.status = new_status

    def set_grade(self, grade: float) -> None:
        """Установка оценки для задания.

        Args:
            grade: Оценка (от 0 до 100).

        Raises:
            ValueError: Если оценка вне диапазона [0, 100].
        """
        if not 0 <= grade <= 100:
            raise ValueError("Оценка должна быть от 0 до 100")
        self.grade = grade
        self.status = AssignmentStatus.GRADED

    def __str__(self) -> str:
        """Строковое представление задания с учетом статуса и оценки."""
        base_str = super().__str__()
        grade_str = f", Оценка: {self.grade}" if self.grade is not None else ""
        return f"{base_str}, Статус: {self.status.value}{grade_str}"


class Course:
    """Класс для управления курсом и связанными заданиями."""
    
    def __init__(self, course_name: str, instructor: str):
        """Инициализация курса.

        Args:
            course_name: Название курса.
            instructor: Имя преподавателя.
        """
        self.course_name = course_name
        self.instructor = instructor
        self.assignments: List[Assignment] = []

    def add_assignment(self, assignment: Assignment) -> None:
        """Добавление задания в курс.

        Args:
            assignment: Объект задания.
        """
        self.assignments.append(assignment)

    def remove_assignment(self, index: int) -> None:
        """Удаление задания по индексу.

        Args:
            index: Индекс задания в списке.

        Raises:
            IndexError: Если индекс вне диапазона.
        """
        if 0 <= index < len(self.assignments):
            self.assignments.pop(index)
        else:
            raise IndexError("Недопустимый индекс задания")

    def get_assignments(self) -> List[Assignment]:
        """Получение списка всех заданий.

        Returns:
            Список заданий курса.
        """
        return self.assignments

    def __str__(self) -> str:
        """Строковое представление курса."""
        return (f"Курс: {self.course_name}, Преподаватель: {self.instructor}, "
                f"Количество заданий: {len(self.assignments)}")