from datetime import datetime
import re
from enum import Enum
from typing import List

class AssignmentStatus(Enum):
    PENDING = "Pending"
    SUBMITTED = "Submitted"
    GRADED = "Graded"

class Themes_of_the_works:
    def __init__(self, student_name: str, theme_name: str, issue_date: datetime):
        self._student_name = student_name
        self._theme_name = theme_name
        self._issue_date = issue_date

    @property
    def student_name(self) -> str:
        return self._student_name

    @property
    def theme_name(self) -> str:
        return self._theme_name

    @property
    def issue_date(self) -> datetime:
        return self._issue_date

    def __str__(self) -> str:
        return f"Студент: {self._student_name}, Тема: {self._theme_name}, Дата выдачи: {self._issue_date.strftime('%Y.%m.%d')}"

class Assignment(Themes_of_the_works):
    def __init__(self, student_name: str, theme_name: str, issue_date: datetime, status: AssignmentStatus = AssignmentStatus.PENDING, grade: float = None):
        super().__init__(student_name, theme_name, issue_date)
        self._status = status
        self._grade = grade

    @property
    def status(self) -> AssignmentStatus:
        return self._status

    @property
    def grade(self) -> float:
        return self._grade

    def update_status(self, new_status: AssignmentStatus) -> None:
        self._status = new_status

    def set_grade(self, grade: float) -> None:
        if 0 <= grade <= 100:
            self._grade = grade
            self._status = AssignmentStatus.GRADED
        else:
            raise ValueError("Оценка должна быть от 0 до 100")

    def __str__(self) -> str:
        base_str = super().__str__()
        grade_str = f", Оценка: {self._grade}" if self._grade is not None else ""
        return f"{base_str}, Статус: {self._status.value}{grade_str}"

class Course:
    def __init__(self, course_name: str, instructor: str):
        self._course_name = course_name
        self._instructor = instructor
        self._assignments: List[Assignment] = []

    @property
    def course_name(self) -> str:
        return self._course_name

    @property
    def instructor(self) -> str:
        return self._instructor

    def add_assignment(self, assignment: Assignment) -> None:
        self._assignments.append(assignment)

    def get_assignments(self) -> List[Assignment]:
        return self._assignments

    def __str__(self) -> str:
        return f"Курс: {self._course_name}, Преподаватель: {self._instructor}, Количество заданий: {len(self._assignments)}"

class Distributor:
    @staticmethod
    def parse_value(value: str):
        try:
            if value.startswith('"') and value.endswith('"'):
                return value.strip('"')
            if match('....'): 
                return datetime.strptime(value, '%Y.%m.%d')
            if '.' in value:
                return float(value)
            return int(value)
        except:
            pass

    @staticmethod
    def create_from_string(description: str, course: Course) -> Assignment:
        tokens = re.findall(r'"[^"]*"|\d{4}\.\d{2}\.\d{2}|\S+', description)
        parsed_values = [Distributor.parse_value(token) for token in tokens]
        if len(parsed_values) != 3:
            raise ValueError("Ошибка: ожидалось 3 значения (ФИО, тема, дата выдачи)")
        assignment = Assignment(*parsed_values)
        course.add_assignment(assignment)
        return assignment

    @staticmethod
    def create_from_file(file_path: str, course: Course) -> List[Assignment]:
        assignments = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                if line.strip():
                    try:
                        assignment = Distributor.create_from_string(line.strip(), course)
                        assignments.append(assignment)
                    except ValueError as e:
                        print(f"Пропущена строка {line_number}: {e}")
        return assignments

def add_task():
    while True:
                input_str = input('Введите описание задания (в формате: "ФИО" "Тема" ГГГГ.ММ.ДД) или "назад" для возврата: ')
                if input_str.lower() == 'назад':
                    break
                try:
                    assignment = Distributor.create_from_string(input_str, course)
                    print("Создано задание:")
                    print(assignment)
                except ValueError as e:
                    print(f"Ошибка: {e}. Попробуйте снова.")
def main():
    course = Course("Программирование на Python", "Иванов И.И.")
    
    while True:
        print("\nМеню:")
        print(f"Текущий курс: {course}")
        print("1. Ввести строку и создать задание")
        print("2. Показать все задания курса")
        print("3. Загрузить задания из файла")
        print("4. Изменить статус задания")
        print("5. Поставить оценку за задание")
        print("6. Выход")
        choice = input("Выберите действие (1-6): ")
        if choice == '1':
            

        elif choice == '2':
            print("\nВсе задания курса:")
            assignments = course.get_assignments()
            if not assignments:
                print("Задания отсутствуют.")
            for i, assignment in enumerate(assignments, 1):
                print(f"{i}. {assignment}")

        elif choice == '3':
            file_path = input("Введите путь к файлу: ")
            assignments = Distributor.create_from_file(file_path, course)
            print(f"\nЗагружено {len(assignments)} заданий:")
            for assignment in assignments:
                print(assignment)

        elif choice == '4':
            assignments = course.get_assignments()
            if not assignments:
                print("Задания отсутствуют.")
                continue
            for i, assignment in enumerate(assignments, 1):
                print(f"{i}. {assignment}")
            try:
                index = int(input("Выберите номер задания для изменения статуса: ")) - 1
                if 0 <= index < len(assignments):
                    print("Доступные статусы: 1. Pending, 2. Submitted, 3. Graded")
                    status_choice = input("Выберите новый статус (1-3): ")
                    status_map = {
                        '1': AssignmentStatus.PENDING,
                        '2': AssignmentStatus.SUBMITTED,
                        '3': AssignmentStatus.GRADED
                    }
                    if status_choice in status_map:
                        assignments[index].update_status(status_map[status_choice])
                        print("Статус обновлен:")
                        print(assignments[index])
                    else:
                        print("Некорректный выбор статуса.")
                else:
                    print("Некорректный номер задания.")
            except ValueError:
                print("Ошибка: введите корректный номер.")

        elif choice == '5':
            assignments = course.get_assignments()
            if not assignments:
                print("Задания отсутствуют.")
                continue
            for i, assignment in enumerate(assignments, 1):
                print(f"{i}. {assignment}")
            try:
                index = int(input("Выберите номер задания для выставления оценки: ")) - 1
                if 0 <= index < len(assignments):
                    grade = float(input("Введите оценку (0-100): "))
                    assignments[index].set_grade(grade)
                    print("Оценка выставлена:")
                    print(assignments[index])
                else:
                    print("Некорректный номер задания.")
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == '6':
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()