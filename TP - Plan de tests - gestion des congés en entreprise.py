from TP1 import *
import unittest
from datetime import timedelta
from unittest.mock import patch
from datetime import datetime, timedelta


class HRTest(unittest.TestCase):
    def setUp(self):
        self.john_doe = Employee("John", "Doe")
        self.jane_smith = Employee("Jane", "Smith")
        self.manager = Manager("Mary", "Jones")
        self.team = Team(self.manager, [self.john_doe, self.jane_smith])
        self.vacation_start = datetime.today()
        self.vacation_end = self.vacation_start + timedelta(days=5)

    def test_employee_creation(self):
        self.assertEqual(self.john_doe.name, "John")
        self.assertEqual(self.john_doe.surname, "Doe")

    def test_manager_creation(self):
        # Assert Manager inherits from Employee
        self.assertIsInstance(self.manager, Manager)
        self.assertIsInstance(self.manager, Employee)

    def test_vacation_type_creation(self):
        self.assertEqual(VacationType.VACATION.name, "VACATION")
        self.assertEqual(VacationType.SICK_LEAVE.name, "SICK_LEAVE")

    def test_vacation_creation(self):
        vacation = Vacation(
            self.john_doe, VacationType.VACATION, self.vacation_start, self.vacation_end
        )
        self.assertFalse(vacation.validated)
        self.assertEqual(vacation.employee, self.john_doe)
        self.assertEqual(vacation.vacation_type, VacationType.VACATION)

    @patch("datetime.datetime")
    def test_vacation_validate(self, mock_datetime):
        mock_datetime.now.return_value = self.vacation_start
        vacation = Vacation(
            self.john_doe, VacationType.VACATION, self.vacation_start, self.vacation_end
        )
        vacation.validate()
        self.assertTrue(vacation.validated)

    def test_team_creation(self):
        self.assertEqual(self.team.manager, self.manager)
        self.assertEqual(self.team.employees, [self.john_doe, self.jane_smith])

    def test_hr_creation(self):
        hr = HR([self.team])
        self.assertEqual(hr.teams, [self.team])

    def test_get_vacations(self):
        hr = HR([self.team])
        vacation = Vacation(
            self.john_doe, VacationType.VACATION, self.vacation_start, self.vacation_end
        )
        self.team.vacations.append(vacation)
        self.assertEqual(hr.getVacations(self.team), [vacation])


if __name__ == "__main__":
    unittest.main()
