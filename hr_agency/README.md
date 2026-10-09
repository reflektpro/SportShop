# ПК «Кадровое агентство» (практические работы 1–4)

Учебный проект информационной системы кадрового агентства. Автор: Лаптев В.И., группа 3ИП7-24.

| № | Работа | Документы |
|---|---|---|
| 1 | Анализ предметной области | [docs/01_Domain_Analysis.md](docs/01_Domain_Analysis.md) |
| 2 | Разработка и оформление технического задания | [docs/02_Technical_Specification.md](docs/02_Technical_Specification.md) |
| 3 | Построение архитектуры программного средства | [эскизный проект](docs/03_Sketch_Project.md), [технический проект](docs/03_Technical_Project.md), [диаграммы](docs/diagrams) |
| 4 | Объектно-ориентированное проектирование | [docs/04_OOP_Design.md](docs/04_OOP_Design.md), [agency.py](agency.py), [demo.py](demo.py), [tests](tests) |

Диаграммы строятся из исходников Graphviz: `cd docs/diagrams && for f in *.dot; do dot -Tpng $f -o ${f%.dot}.png; done`.

## Практическая работа № 4 — объектно-ориентированное проектирование

* `docs/04_OOP_Design.md` — анализ, функции, схема документопотока, сущности, диаграмма классов, входные/выходные данные;
* `agency.py` — классы предметной области; `demo.py` — создание объектов и пример использования;
* `tests/test_agency.py` — 16 модульных тестов.

```bash
python hr_agency/demo.py
python -m unittest discover -s hr_agency/tests -t .
```
