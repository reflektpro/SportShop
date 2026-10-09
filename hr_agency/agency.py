"""ПК «Кадровое агентство» — объектная модель предметной области (практическая работа № 4).

Классы соответствуют сущностям ERD из эскизного проекта (работа № 3):
Employer, Vacancy, Applicant, User, Selection, Stage; класс Agency объединяет их и реализует
функции системы: учёт, поиск, автоподбор кандидатов (алгоритм технического проекта),
этапы работы и отчёты.
"""
from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from pathlib import Path


class VacancyStatus(Enum):
    OPEN = "открыта"
    PAUSED = "приостановлена"
    CLOSED = "закрыта"


class Role(Enum):
    ADMIN = "администратор"
    HEAD = "руководитель"
    RECRUITER = "рекрутер"


# порядок этапов работы с кандидатом (процесс 5 эскизного проекта)
STAGES = ["первичный контакт", "интервью", "тестирование", "направление к работодателю",
          "обратная связь", "приём на работу"]


def _norm_skills(skills) -> set[str]:
    return {s.strip().lower() for s in skills if s and s.strip()}


class Person:
    """Базовый класс для людей в системе: ФИО и контактный телефон с проверкой."""

    def __init__(self, full_name: str, phone: str):
        self.full_name = full_name
        self.phone = phone

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        if not value or len(value.split()) < 2:
            raise ValueError("ФИО должно содержать минимум фамилию и имя")
        self._full_name = " ".join(value.split())

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        digits = re.sub(r"\D", "", value or "")
        if len(digits) != 11:
            raise ValueError(f"Телефон должен содержать 11 цифр: {value!r}")
        self._phone = "+7" + digits[1:]

    @property
    def short_name(self) -> str:
        """«Иванов Иван Иванович» → «Иванов И.И.»."""
        parts = self.full_name.split()
        return parts[0] + " " + "".join(p[0] + "." for p in parts[1:])


class Applicant(Person):
    """Соискатель: резюме и параметры для подбора."""

    def __init__(self, applicant_id: int, full_name: str, phone: str, city: str,
                 education: str, experience: int, skills, desired_salary: int,
                 email: str = "", resume_file: str = ""):
        super().__init__(full_name, phone)
        if experience < 0:
            raise ValueError("Опыт не может быть отрицательным")
        if desired_salary <= 0:
            raise ValueError("Желаемая зарплата должна быть больше нуля")
        if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", email):
            raise ValueError(f"Некорректный email: {email}")
        self.id = applicant_id
        self.city = city
        self.education = education
        self.experience = experience
        self.skills = _norm_skills(skills)
        self.desired_salary = desired_salary
        self.email = email
        self.resume_file = resume_file

    def __repr__(self) -> str:
        return f"Applicant({self.id}, {self.short_name})"


@dataclass
class Employer:
    """Работодатель. ИНН — 10 цифр (организация) или 12 (ИП)."""
    id: int
    name: str
    inn: str
    city: str
    contact_person: str
    phone: str = ""
    email: str = ""

    def __post_init__(self):
        if not re.fullmatch(r"\d{10}|\d{12}", self.inn):
            raise ValueError(f"ИНН должен состоять из 10 или 12 цифр: {self.inn}")


class Vacancy:
    """Вакансия работодателя со статусом и требованиями."""

    def __init__(self, vacancy_id: int, employer: Employer, title: str, city: str,
                 requirements, min_experience: int, salary: int,
                 opened: date | None = None):
        if salary <= 0:
            raise ValueError("Зарплата должна быть больше нуля")
        self.id = vacancy_id
        self.employer = employer
        self.title = title
        self.city = city
        self.requirements = _norm_skills(requirements)
        self.min_experience = min_experience
        self.salary = salary
        self.opened = opened or date.today()
        self.closed: date | None = None
        self._status = VacancyStatus.OPEN

    @property
    def status(self) -> VacancyStatus:
        return self._status

    @status.setter
    def status(self, value: VacancyStatus) -> None:
        """Смена статуса; при закрытии фиксируется дата закрытия."""
        if self._status is VacancyStatus.CLOSED and value is not VacancyStatus.CLOSED:
            raise ValueError("Закрытую вакансию нельзя открыть повторно — создайте новую")
        self._status = value
        if value is VacancyStatus.CLOSED:
            self.closed = date.today()

    @property
    def is_open(self) -> bool:
        return self._status is VacancyStatus.OPEN

    def __repr__(self) -> str:
        return f"Vacancy({self.id}, {self.title!r}, {self.status.value})"


class User:
    """Пользователь системы. Пароль хранится только в виде хэша SHA-256 с солью."""

    def __init__(self, user_id: int, login: str, password: str, role: Role, full_name: str):
        self.id = user_id
        self.login = login
        self.role = role
        self.full_name = full_name
        self._salt = hashlib.sha256(login.encode()).hexdigest()[:16]
        self._hash = self._make_hash(password)

    def _make_hash(self, password: str) -> str:
        if len(password) < 6:
            raise ValueError("Пароль должен быть не короче 6 символов")
        return hashlib.sha256((self._salt + password).encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        try:
            return self._make_hash(password) == self._hash
        except ValueError:
            return False

    def can(self, action: str) -> bool:
        """Права ролей: администратор — всё; руководитель — отчёты; рекрутер — работа с кандидатами."""
        rights = {Role.ADMIN: {"edit", "match", "stage", "report", "users"},
                  Role.HEAD: {"report"},
                  Role.RECRUITER: {"edit", "match", "stage"}}
        return action in rights[self.role]


@dataclass
class Stage:
    name: str
    day: date
    comment: str = ""


@dataclass
class Selection:
    """Подборка: соискатель на вакансию, которого ведёт рекрутер; хранит историю этапов."""
    id: int
    vacancy: Vacancy
    applicant: Applicant
    recruiter: User
    score: int
    created: date = field(default_factory=date.today)
    stages: list[Stage] = field(default_factory=list)

    @property
    def current_stage(self) -> str | None:
        return self.stages[-1].name if self.stages else None

    def add_stage(self, name: str, comment: str = "", day: date | None = None) -> Stage:
        """Добавляет следующий этап. Перескакивать этапы нельзя (процесс 5)."""
        if name not in STAGES:
            raise ValueError(f"Неизвестный этап: {name}")
        expected = STAGES[len(self.stages)] if len(self.stages) < len(STAGES) else None
        if name != expected:
            raise ValueError(f"Следующий этап — «{expected}», а не «{name}»")
        stage = Stage(name, day or date.today(), comment)
        self.stages.append(stage)
        if name == "приём на работу":
            self.vacancy.status = VacancyStatus.CLOSED
        return stage


class Agency:
    """Кадровое агентство: реестр всех объектов и функции системы."""

    def __init__(self, name: str):
        self.name = name
        self.employers: dict[int, Employer] = {}
        self.vacancies: dict[int, Vacancy] = {}
        self.applicants: dict[int, Applicant] = {}
        self.users: dict[str, User] = {}
        self.selections: list[Selection] = []
        self.log: list[str] = []

    # --- учёт (справочники) ---
    def add_employer(self, employer: Employer) -> Employer:
        if any(e.inn == employer.inn for e in self.employers.values()):
            raise ValueError(f"Работодатель с ИНН {employer.inn} уже есть")
        self.employers[employer.id] = employer
        return employer

    def add_vacancy(self, vacancy: Vacancy) -> Vacancy:
        if vacancy.employer.id not in self.employers:
            raise ValueError("Сначала добавьте работодателя")
        self.vacancies[vacancy.id] = vacancy
        return vacancy

    def add_applicant(self, applicant: Applicant) -> Applicant:
        if any(a.phone == applicant.phone for a in self.applicants.values()):
            raise ValueError(f"Соискатель с телефоном {applicant.phone} уже есть")
        self.applicants[applicant.id] = applicant
        return applicant

    def add_user(self, user: User) -> User:
        self.users[user.login] = user
        return user

    # --- авторизация ---
    def login(self, login: str, password: str) -> User:
        user = self.users.get(login)
        if user is None or not user.check_password(password):
            self.log.append(f"неудачный вход: {login}")
            raise PermissionError("Неверный логин или пароль")
        self.log.append(f"вход: {login} ({user.role.value})")
        return user

    # --- поиск ---
    def search_vacancies(self, text: str = "", city: str | None = None,
                         min_salary: int | None = None, only_open: bool = True) -> list[Vacancy]:
        t = text.lower()
        return [v for v in self.vacancies.values()
                if (not only_open or v.is_open)
                and (t in v.title.lower() or t in v.employer.name.lower() or t in v.requirements)
                and (city is None or v.city.lower() == city.lower())
                and (min_salary is None or v.salary >= min_salary)]

    def search_applicants(self, skill: str | None = None, min_experience: int = 0,
                          city: str | None = None, max_salary: int | None = None) -> list[Applicant]:
        return [a for a in self.applicants.values()
                if (skill is None or skill.lower() in a.skills)
                and a.experience >= min_experience
                and (city is None or a.city.lower() == city.lower())
                and (max_salary is None or a.desired_salary <= max_salary)]

    # --- подбор (алгоритм из технического проекта, работа № 3) ---
    @staticmethod
    def score(vacancy: Vacancy, applicant: Applicant) -> int:
        """Балл соответствия 0–100: навыки 60, опыт 20, зарплата 15, город 5."""
        skills = (len(vacancy.requirements & applicant.skills) / len(vacancy.requirements)
                  if vacancy.requirements else 1)
        total = 60 * skills
        total += 20 if applicant.experience >= vacancy.min_experience else 0
        total += 15 if applicant.desired_salary <= vacancy.salary else 0
        total += 5 if applicant.city.lower() == vacancy.city.lower() else 0
        return round(total)

    def match_candidates(self, vacancy: Vacancy, threshold: int = 50) -> list[tuple[Applicant, int]]:
        if not vacancy.is_open:
            raise ValueError(f"Вакансия «{vacancy.title}» не открыта")
        if not 0 <= threshold <= 100:
            raise ValueError("Порог должен быть от 0 до 100")
        result = [(a, self.score(vacancy, a)) for a in self.applicants.values()]
        result = [r for r in result if r[1] >= threshold]
        return sorted(result, key=lambda r: (-r[1], r[0].full_name))

    def create_selection(self, user: User, vacancy: Vacancy, threshold: int = 50) -> list[Selection]:
        if not user.can("match"):
            raise PermissionError(f"Роль «{user.role.value}» не может формировать подборки")
        created = []
        for applicant, sc in self.match_candidates(vacancy, threshold):
            sel = Selection(len(self.selections) + 1, vacancy, applicant, user, sc)
            self.selections.append(sel)
            created.append(sel)
        self.log.append(f"подборка: {vacancy.title} — {len(created)} канд. ({user.login})")
        return created

    # --- отчёты ---
    def report_open_vacancies(self) -> list[tuple[str, str, int]]:
        return sorted((v.employer.name, v.title, v.salary) for v in self.vacancies.values() if v.is_open)

    def report_recruiters(self) -> list[tuple[str, int, int, float]]:
        """(рекрутер, подборок, приёмов, конверсия %)."""
        rows = []
        for u in self.users.values():
            if u.role is not Role.RECRUITER:
                continue
            mine = [s for s in self.selections if s.recruiter is u]
            hired = sum(1 for s in mine if s.current_stage == "приём на работу")
            rows.append((u.full_name, len(mine), hired, round(100 * hired / len(mine), 1) if mine else 0.0))
        return rows

    def export_selections_csv(self, path: str | Path) -> Path:
        path = Path(path)
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["id", "вакансия", "соискатель", "балл", "этап", "рекрутер"])
            for s in self.selections:
                w.writerow([s.id, s.vacancy.title, s.applicant.full_name, s.score,
                            s.current_stage or "—", s.recruiter.login])
        return path
