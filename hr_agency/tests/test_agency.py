"""Тесты объектной модели ПК «Кадровое агентство» (работа № 4)."""
import unittest
from datetime import date

from hr_agency.agency import (Agency, Applicant, Employer, Role, Selection, User, Vacancy,
                              VacancyStatus)


def make():
    ag = Agency("Тест")
    emp = ag.add_employer(Employer(1, "ООО «ТехСофт»", "7701234567", "Москва", "Смирнова Е.В."))
    vac = ag.add_vacancy(Vacancy(1, emp, "Python-разработчик", "Москва", ["Python", "SQL", "Git"], 2, 120000))
    a1 = ag.add_applicant(Applicant(1, "Иванов Иван Иванович", "89161112233", "Москва", "высшее", 3,
                                    ["python", "git", "docker"], 110000))
    a2 = ag.add_applicant(Applicant(2, "Кузнецов Пётр", "89031112233", "Тула", "СПО", 5, ["excel"], 60000))
    rec = ag.add_user(User(2, "petrova", "rec2026!", Role.RECRUITER, "Петрова А.С."))
    return ag, vac, a1, a2, rec


class TestPerson(unittest.TestCase):
    def test_phone_normalized(self):
        a = Applicant(1, "Иванов Иван", "8 (916) 111-22-33", "Москва", "высшее", 1, [], 1000)
        self.assertEqual(a.phone, "+79161112233")

    def test_bad_phone(self):
        with self.assertRaises(ValueError):
            Applicant(1, "Иванов Иван", "123", "Москва", "высшее", 1, [], 1000)

    def test_full_name_required(self):
        with self.assertRaises(ValueError):
            Applicant(1, "Иванов", "89161112233", "Москва", "высшее", 1, [], 1000)

    def test_short_name(self):
        a = Applicant(1, "Иванов Иван Иванович", "89161112233", "Москва", "в", 1, [], 1000)
        self.assertEqual(a.short_name, "Иванов И.И.")

    def test_negative_experience(self):
        with self.assertRaises(ValueError):
            Applicant(1, "Иванов Иван", "89161112233", "Москва", "в", -1, [], 1000)


class TestEmployerVacancy(unittest.TestCase):
    def test_inn_checked(self):
        with self.assertRaises(ValueError):
            Employer(1, "ООО", "12345", "Москва", "Иванов")

    def test_duplicate_inn(self):
        ag, *_ = make()
        with self.assertRaises(ValueError):
            ag.add_employer(Employer(5, "Другая", "7701234567", "Москва", "Петров"))

    def test_close_sets_date_and_cannot_reopen(self):
        _, vac, *_ = make()
        vac.status = VacancyStatus.CLOSED
        self.assertEqual(vac.closed, date.today())
        with self.assertRaises(ValueError):
            vac.status = VacancyStatus.OPEN


class TestUser(unittest.TestCase):
    def test_password_hashed(self):
        u = User(1, "admin", "secret1", Role.ADMIN, "А")
        self.assertNotIn("secret1", vars(u).values())
        self.assertTrue(u.check_password("secret1"))
        self.assertFalse(u.check_password("wrong12"))

    def test_login_fails(self):
        ag, *_ = make()
        with self.assertRaises(PermissionError):
            ag.login("petrova", "bad-password")

    def test_roles(self):
        self.assertFalse(User(1, "boss", "boss123", Role.HEAD, "Б").can("match"))
        self.assertTrue(User(1, "rec", "rec123", Role.RECRUITER, "Р").can("match"))


class TestMatching(unittest.TestCase):
    def test_score_example_from_tech_project(self):
        _, vac, a1, *_ = make()
        self.assertEqual(Agency.score(vac, a1), 80)   # 40 + 20 + 15 + 5

    def test_match_filters_and_sorts(self):
        ag, vac, a1, a2, _ = make()
        result = ag.match_candidates(vac)
        self.assertEqual([a for a, _ in result], [a1])

    def test_closed_vacancy_cannot_be_matched(self):
        ag, vac, *_ = make()
        vac.status = VacancyStatus.PAUSED
        with self.assertRaises(ValueError):
            ag.match_candidates(vac)

    def test_head_cannot_create_selection(self):
        ag, vac, *_ = make()
        head = User(9, "boss", "boss123", Role.HEAD, "Б")
        with self.assertRaises(PermissionError):
            ag.create_selection(head, vac)


class TestStages(unittest.TestCase):
    def test_stages_in_order_and_hire_closes_vacancy(self):
        ag, vac, a1, _, rec = make()
        sel = ag.create_selection(rec, vac)[0]
        with self.assertRaises(ValueError):
            sel.add_stage("интервью")
        for st in ["первичный контакт", "интервью", "тестирование", "направление к работодателю",
                   "обратная связь", "приём на работу"]:
            sel.add_stage(st)
        self.assertEqual(vac.status, VacancyStatus.CLOSED)
        self.assertEqual(ag.report_recruiters(), [("Петрова А.С.", 1, 1, 100.0)])


if __name__ == "__main__":
    unittest.main()
