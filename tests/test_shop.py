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
