import csv
import sys

from invoicer.calc import total


def main(path):
    with open(path) as f:
        lines = [{"quantity": float(r["quantity"]), "price": float(r["price"])} for r in csv.DictReader(f)]
    print(f"Total: {total(lines):.2f}")


if __name__ == "__main__":
    main(sys.argv[1])
