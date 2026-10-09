# ПК «Кадровое агентство» (практические работы 1–4)

Учебный проект информационной системы кадрового агентства. Автор: Лаптев В.И., группа 3ИП7-24.

| № | Работа | Документы |
|---|---|---|
| 1 | Анализ предметной области | [docs/01_Domain_Analysis.md](docs/01_Domain_Analysis.md) |
| 2 | Разработка и оформление технического задания | [docs/02_Technical_Specification.md](docs/02_Technical_Specification.md) |
| 3 | Построение архитектуры программного средства | [эскизный проект](docs/03_Sketch_Project.md), [технический проект](docs/03_Technical_Project.md), [диаграммы](docs/diagrams) |

Диаграммы строятся из исходников Graphviz: `cd docs/diagrams && for f in *.dot; do dot -Tpng $f -o ${f%.dot}.png; done`.
