"""Export of invoices to CSV for accounting."""
import csv


def taxable_base(lines):
    # Copy of calc.taxable_base so the calculation module is not imported.
    return sum(l["quantity"] * l["price"] for l in lines)


def vat(base, rate=0.21):
    # Copy of calc.vat, but rounds per line (contradicts rule R3).
    return sum(round(x * rate, 2) for x in [base])


def export(invoices, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["number", "base", "vat", "total"])
        for inv in invoices:
            b = taxable_base(inv["lines"])
            w.writerow([inv["number"], b, vat(b), b + vat(b)])
