import unittest
from datetime import datetime
from models import Assignment, AssignmentBase, AssignmentStatus, Course


class TestAssignmentBase(unittest.TestCase):
    def setUp(self):
        self.base = AssignmentBase("Иванов Иван", "Введение в Python", datetime(2025, 1, 15))

    def test_init(self):
        self.assertEqual(self.base.student_name, "Иванов Иван")
        self.assertEqual(self.base.theme_name, "Введение в Python")
        self.assertEqual(self.base.issue_date, datetime(2025, 1, 15))

    def test_str(self):
        expected = "Студент: Иванов Иван, Тема: Введение в Python, Дата выдачи: 2025.01.15"
        self.assertEqual(str(self.base), expected)


class TestAssignment(unittest.TestCase):
    def setUp(self):
        self.assignment = Assignment("Иванов Иван", "Введение в Python", datetime(2025, 1, 15))

    def test_init_default(self):
        self.assertEqual(self.assignment.student_name, "Иванов Иван")
        self.assertEqual(self.assignment.theme_name, "Введение в Python")
        self.assertEqual(self.assignment.issue_date, datetime(2025, 1, 15))
        self.assertEqual(self.assignment.status, AssignmentStatus.PENDING)
        self.assertIsNone(self.assignment.grade)

    def test_init_with_status_and_grade(self):
        assignment = Assignment("Петров Петр", "ООП", datetime(2025, 2, 20), AssignmentStatus.GRADED, 85.0)
        self.assertEqual(assignment.status, AssignmentStatus.GRADED)
        self.assertEqual(assignment.grade, 85.0)

    def test_update_status(self):
        self.assignment.update_status(AssignmentStatus.SUBMITTED)
        self.assertEqual(self.assignment.status, AssignmentStatus.SUBMITTED)

    def test_set_grade_valid(self):
        self.assignment.set_grade(90.0)
        self.assertEqual(self.assignment.grade, 90.0)
        self.assertEqual(self.assignment.status, AssignmentStatus.GRADED)

    def test_set_grade_invalid(self):
        with self.assertRaises(ValueError):
            self.assignment.set_grade(-1)
        with self.assertRaises(ValueError):
            self.assignment.set_grade(101)

    def test_str(self):
        expected = "Студент: Иванов Иван, Тема: Введение в Python, Дата выдачи: 2025.01.15, Статус: Pending"
        self.assertEqual(str(self.assignment), expected)
        self.assignment.set_grade(85.0)
        expected = "Студент: Иванов Иван, Тема: Введение в Python, Дата выдачи: 2025.01.15, Статус: Graded, Оценка: 85.0"
        self.assertEqual(str(self.assignment), expected)


class TestCourse(unittest.TestCase):
    def setUp(self):
        self.course = Course("Программирование на Python", "Иванов И.И.")
        self.assignment = Assignment("Иванов Иван", "Введение в Python", datetime(2025, 1, 15))

    def test_init(self):
        self.assertEqual(self.course.course_name, "Программирование на Python")
        self.assertEqual(self.course.instructor, "Иванов И.И.")
        self.assertEqual(self.course.assignments, [])

    def test_add_assignment(self):
        self.course.add_assignment(self.assignment)
        self.assertEqual(len(self.course.assignments), 1)
        self.assertEqual(self.course.assignments[0], self.assignment)

    def test_remove_assignment_valid(self):
        self.course.add_assignment(self.assignment)
        self.course.remove_assignment(0)
        self.assertEqual(len(self.course.assignments), 0)

    def test_remove_assignment_invalid(self):
        with self.assertRaises(IndexError):
            self.course.remove_assignment(0)

    def test_get_assignments(self):
        self.course.add_assignment(self.assignment)
        assignments = self.course.get_assignments()
        self.assertEqual(assignments, [self.assignment])

    def test_str(self):
        expected = "Курс: Программирование на Python, Преподаватель: Иванов И.И., Количество заданий: 0"
        self.assertEqual(str(self.course), expected)
        self.course.add_assignment(self.assignment)
        expected = "Курс: Программирование на Python, Преподаватель: Иванов И.И., Количество заданий: 1"
        self.assertEqual(str(self.course), expected)


if __name__ == '__main__':
    unittest.main()