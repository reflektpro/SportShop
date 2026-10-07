# 10. Pull Request

## PR: feature/search-advanced → develop

**Что сделано:**
- Доработана функция `search_advanced(products, query, category=None, min_price=None, max_price=None)`.
- Текстовый запрос теперь ищет по названию, бренду **и категории** (например, `"обувь"`).
- Добавлена проверка диапазона: если `min_price > max_price`, выбрасывается `ValueError`.
- Фильтры можно комбинировать; `None` и пустая строка означают «без ограничения».
- Добавлена документация функции (docstring).

**Как проверить:**
```
python3 -c "from shop import *; print([p['name'] for p in search_advanced(PRODUCTS, 'обувь', max_price=10000)])"
# ожидается: ['Кроссовки RunFast']
python3 -c "from shop import *; print([p['name'] for p in search_advanced(PRODUCTS, '', category='Одежда', min_price=2500)])"
# ожидается: ['Футболка DryFit']
python3 -c "from shop import *; search_advanced(PRODUCTS, min_price=5000, max_price=1000)"
# ожидается: ValueError
```

**Связанные задачи:** US-2

**Ревьюер:** Войнов Д. (одногруппник)

**Чек-лист ревью:**
- [x] Код соответствует PEP 8
- [x] Старые вызовы `search_advanced(PRODUCTS, "nike")` работают как раньше
- [x] Нет конфликтов с `develop`

**Решение ревьюера:** Approved ✅ — слито в `develop` через `git merge --no-ff`.
