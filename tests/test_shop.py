import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shop import PRODUCTS, get_low_stock

def test_get_low_stock():
    low = get_low_stock(PRODUCTS, 3)
    assert all(p["qty"] <= 3 for p in low)
    assert low == sorted(low, key=lambda p: p["qty"])

from shop import search_advanced

def test_search_advanced():
    r = search_advanced(PRODUCTS, "nike", category="Обувь")
    assert len(r) == 1 and r[0]["name"] == "Кроссовки RunFast"

from shop import count_by_category

def test_count_by_category():
    c = count_by_category(PRODUCTS)
    assert "Обувь" in c and c["Обувь"] >= 1

from shop import save_orders

def test_save_orders(tmp_path):
    f = tmp_path / "o.json"
    save_orders([{"a": 1}], str(f))
    assert f.exists()
