from invoicer.calc import taxable_base, vat, total, volume_discount


def test_taxable_base():
    assert taxable_base([{"quantity": 2, "price": 10.0}]) == 20.0


def test_volume_discount():
    assert volume_discount(1000) == 30.0


def test_vat_rounding():
    # Rule R3: 3 lines of 0.35 € → base 1.05 → VAT 0.22 → total 1.27
    lines = [{"quantity": 1, "price": 0.35}] * 3
    assert total(lines) == 1.27
