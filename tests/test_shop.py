import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shop import PRODUCTS, get_low_stock

def test_get_low_stock():
    low = get_low_stock(PRODUCTS, 3)
    assert all(p["qty"] <= 3 for p in low)
    assert low == sorted(low, key=lambda p: p["qty"])
