"""Демонстрация объектной модели ПК «Кадровое агентство»: создание объектов и их использование."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hr_agency.agency import Agency, Applicant, Employer, Role, User, Vacancy  # noqa: E402

agency = Agency("Кадровое агентство «Старт»")
admin = agency.add_user(User(1, "admin", "admin123", Role.ADMIN, "Лаптев Василий Иванович"))
rec = agency.add_user(User(2, "petrova", "rec2026!", Role.RECRUITER, "Петрова Анна Сергеевна"))
head = agency.add_user(User(3, "director", "boss2026", Role.HEAD, "Орлов Игорь Петрович"))

user = agency.login("petrova", "rec2026!")
print(f"Вход выполнен: {user.full_name}, роль — {user.role.value}")

techsoft = agency.add_employer(Employer(1, "ООО «ТехСофт»", "7701234567", "Москва", "Смирнова Е.В."))
logist = agency.add_employer(Employer(2, "АО «ЛогистикПро»", "5009876543", "Химки", "Козлов Д.А."))
py = agency.add_vacancy(Vacancy(1, techsoft, "Python-разработчик", "Москва",
                                ["Python", "SQL", "Git"], 2, 120_000))
op = agency.add_vacancy(Vacancy(2, logist, "Оператор склада", "Химки", ["1С", "Excel"], 0, 55_000))

for a in [
    Applicant(1, "Иванов Иван Иванович", "8 (916) 111-22-33", "Москва", "высшее", 3,
              ["python", "git", "docker"], 110_000, "ivanov@mail.ru"),
    Applicant(2, "Сидорова Мария Олеговна", "+7 925 444 55 66", "Москва", "высшее", 1,
              ["Python", "SQL", "Git"], 90_000),
    Applicant(3, "Кузнецов Пётр Андреевич", "89031112233", "Тула", "среднее проф.", 5,
              ["Excel", "1С"], 60_000),
    Applicant(4, "Фёдоров Олег Игоревич", "8-926-777-88-99", "Москва", "высшее", 4,
              ["java", "sql"], 150_000),
]:
    agency.add_applicant(a)
print(f"В базе: работодателей {len(agency.employers)}, вакансий {len(agency.vacancies)}, "
      f"соискателей {len(agency.applicants)}")

print("\nПоиск вакансий «python»:", [v.title for v in agency.search_vacancies("python")])
print("Соискатели со знанием SQL:", [a.short_name for a in agency.search_applicants(skill="sql")])

print(f"\nАвтоподбор на вакансию «{py.title}» (порог 50):")
for sel in agency.create_selection(user, py):
    print(f"  {sel.applicant.short_name:<14} балл {sel.score}")

best = agency.selections[0]
for stage in ["первичный контакт", "интервью", "тестирование", "направление к работодателю",
              "обратная связь", "приём на работу"]:
    best.add_stage(stage)
print(f"\n{best.applicant.short_name}: этап «{best.current_stage}», вакансия — {py.status.value} "
      f"(закрыта {py.closed:%d.%m.%Y})")

try:
    agency.selections[1].add_stage("интервью")
except ValueError as e:
    print("Ошибка этапа:", e)
try:
    agency.create_selection(head, op)
except PermissionError as e:
    print("Ошибка прав:", e)
try:
    Applicant(9, "Тестов", "123", "Москва", "—", 1, [], 1)
except ValueError as e:
    print("Ошибка ввода:", e)

print("\nОтчёт «Открытые вакансии»:", agency.report_open_vacancies())
print("Отчёт «Эффективность рекрутеров»:", agency.report_recruiters())
path = agency.export_selections_csv(Path(__file__).resolve().parent / "selections.csv")
print(f"Подборки выгружены в {path.name}:")
print(path.read_text(encoding="utf-8").strip())
print("\nЖурнал:", *agency.log, sep="\n  ")
