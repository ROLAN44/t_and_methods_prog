import re
from datetime import datetime
from typing import List
from models import Assignment, AssignmentStatus, Course


class Distributor:
    """Handles parsing, file reading, and writing for assignments."""
    @staticmethod
    def parse_value(value: str):
        """Parse a single value from string input."""
        try:
            if value == '""':
                return None
            if value.startswith('"') and value.endswith('"'):
                return value.strip('"')
            if re.match(r'\d{4}\.\d{2}\.\d{2}', value):
                return datetime.strptime(value, '%Y.%m.%d')
            if value in [status.value for status in AssignmentStatus]:
                return value
            if value.replace('.', '').isdigit():
                return float(value)
            raise ValueError(f"Невозможно распознать значение: {value}")
        except ValueError as e:
            raise ValueError(f"Ошибка парсинга значения: {value}") from e

    @staticmethod
    def create_from_string(description: str, course: Course) -> Assignment:
        """Create an assignment from a string description."""
        tokens = re.findall(r'"[^"]*"|\d{4}\.\d{2}\.\d{2}|\S+', description)
        if len(tokens) != 5:
            raise ValueError("Ожидалось 5 значений: ФИО, тема, дата выдачи, статус, оценка")
        parsed_values = [Distributor.parse_value(token) for token in tokens]
        student_name, theme_name, issue_date, status_str, grade = parsed_values

        # Convert status string to AssignmentStatus
        for status in AssignmentStatus:
            if status.value == status_str:
                assignment = Assignment(student_name, theme_name, issue_date, status, grade)
                break
        else:
            raise ValueError(f"Недопустимый статус: {status_str}")

        course.add_assignment(assignment)
        return assignment

    @staticmethod
    def create_from_file(file_path: str, course: Course) -> List[Assignment]:
        """Read assignments from a file."""
        assignments = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        assignment = Distributor.create_from_string(line.strip(), course)
                        assignments.append(assignment)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {file_path} не найден")
        return assignments

    @staticmethod
    def save_to_file(file_path: str, course: Course) -> None:
        """Save all assignments from the course to a file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                for assignment in course.get_assignments():
                    grade_str = f'"{assignment.grade}"' if assignment.grade is not None else '""'
                    line = (f'"{assignment.student_name}" "{assignment.theme_name}" '
                            f'{assignment.issue_date.strftime("%Y.%m.%d")} '
                            f'{assignment.status.value} {grade_str}\n')
                    file.write(line)
        except IOError as e:
            raise IOError(f"Ошибка записи в файл {file_path}: {e}") from e