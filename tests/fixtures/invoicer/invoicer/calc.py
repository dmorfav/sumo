"""Invoice amount calculation. The business rules are in docs/rules.md."""

VAT_STANDARD = 0.21
VAT_REDUCED = 0.10


def taxable_base(lines):
    return sum(l["quantity"] * l["price"] for l in lines)


def vat(base, rate=VAT_STANDARD):
    # Rule R3: VAT is rounded to 2 decimals per invoice, not per line.
    return round(base * rate, 2)


def total(lines, rate=VAT_STANDARD):
    b = taxable_base(lines)
    return b + vat(b, rate)


def volume_discount(base):
    # Rule R5: 3 % from a taxable base of 1,000 € upwards.
    if base >= 1000:
        return base * 0.03
    return 0
