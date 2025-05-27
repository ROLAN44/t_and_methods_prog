import re
from datetime import datetime
from typing import List
from models import Assignment, AssignmentStatus, Course
from file_logger import FileLogger


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
            if value.replace('.', '', 1).isdigit():
                return float(value)
            raise ValueError(f"Невозможно распознать значение: {value}")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Ошибка парсинга значения: {value}") from e

    @staticmethod
    def create_from_string(description: str, course: Course, logger: FileLogger) -> Assignment:
        """Create an assignment from a string description."""
        try:
            tokens = re.findall(r'"[^"]*"|\d{4}\.\d{2}\.\d{2}|\S+', description)
            if len(tokens) != 5:
                raise ValueError(f"Ожидалось 5 значений (ФИО, тема, дата, статус, оценка), получено: {len(tokens)}")
            parsed_values = [Distributor.parse_value(token) for token in tokens]
            student_name, theme_name, issue_date, status_str, grade = parsed_values

            if not isinstance(student_name, str) or not student_name:
                raise ValueError("ФИО должно быть непустой строкой")
            if not isinstance(theme_name, str) or not theme_name:
                raise ValueError("Тема должна быть непустой строкой")
            if not isinstance(issue_date, datetime):
                raise ValueError("Дата должна быть в формате ГГГГ.ММ.ДД")
            if grade is not None and not isinstance(grade, float):
                raise ValueError("Оценка должна быть числом или пустой")

            # Convert status string to AssignmentStatus
            for status in AssignmentStatus:
                if status.value == status_str:
                    assignment = Assignment(student_name, theme_name, issue_date, status, grade)
                    break
            else:
                raise ValueError(f"Недопустимый статус: {status_str}")

            course.add_assignment(assignment)
            return assignment
        except ValueError as e:
            logger.log_error(f"Ошибка обработки строки: '{description}'. Причина: {str(e)}")
            raise

    @staticmethod
    def create_from_file(file_path: str, course: Course) -> List[Assignment]:
        """Read assignments from a file, skipping invalid lines."""
        assignments = []
        logger = FileLogger("error.log")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, 1):
                    if line.strip():
                        try:
                            assignment = Distributor.create_from_string(line.strip(), course, logger)
                            assignments.append(assignment)
                        except ValueError as e:
                            logger.log_error(f"Пропущена строка {line_number}: {str(e)}")
                            continue
        except FileNotFoundError:
            logger.log_error(f"Файл не найден: {file_path}")
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