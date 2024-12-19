import attrs
from enum import Enum, auto
from datetime import datetime


@attrs.define
class Employee:
    name: str
    surname: str


@attrs.define
class Manager(Employee):
    pass


class VacationType(Enum):
    VACATION = "VACATION"  # Vacances
    WORKTIME_REDUCTION = "WORKTIME_REDUCTION"  # RTT
    SICK_LEAVE = "SICK_LEAVE"  # Maladie
    PUBLIC_VACATIONS = "PUBLIC_VACATIONS"  # Jours fériés
    LEGAL_LEAVE = "LEGAL_LEAVE"  # Congés de droit


@attrs.define
class Vacation:
    employee: Employee
    vacation_type: VacationType
    validated: bool = attrs.field(default=False, init=False)
    start: datetime
    end: datetime

    def validate(self):
        self.validated = True


@attrs.define
class Team:
    manager: Manager
    employees: list[Employee] = attrs.field(factory=list)
    vacations: list[Vacation] = attrs.field(factory=list)


@attrs.define
class HR:
    teams: list[Team] = attrs.field(factory=list)

    def get_vacations(self, team: Team):
        return team.vacations
