import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shop import PRODUCTS, get_low_stock, search_advanced, count_by_category, save_orders, create_order


def test_get_low_stock():
    low = get_low_stock(PRODUCTS, 3)
    assert all(p["qty"] <= 3 for p in low)
    assert low == sorted(low, key=lambda p: p["qty"])


def test_search_advanced():
    r = search_advanced(PRODUCTS, "nike", category="Обувь")
    assert len(r) == 1 and r[0]["name"] == "Кроссовки RunFast"


def test_count_by_category():
    c = count_by_category(PRODUCTS)
    assert "Обувь" in c and c["Обувь"] >= 1


def test_save_orders(tmp_path):
    f = tmp_path / "o.json"
    save_orders([{"a": 1}], str(f))
    assert f.exists()
