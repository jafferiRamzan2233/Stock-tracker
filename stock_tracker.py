"""
Stock Portfolio Tracker
-----------------------
Calculates total investment value from manually defined stock prices.
Concepts: dictionary, input/output, basic arithmetic, file handling.
"""

import csv
from datetime import datetime

# Hardcoded stock prices (price per share)
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOG": 140,
    "MSFT": 330,
}


def get_stock_name():
    """Ask for a stock name until it is valid. Returns None if user types 'done'."""
    while True:
        name = input("Enter stock name (or 'done' to finish): ").strip().upper()
        if name == "DONE":
            return None
        if name in STOCK_PRICES:
            return name
        print(f"  Error: '{name}' is not available. "
              f"Choose from: {', '.join(STOCK_PRICES)}")


def get_quantity(name):
    """Ask for a quantity until it is a valid positive integer."""
    while True:
        raw = input(f"Enter quantity of {name}: ").strip()
        try:
            qty = int(raw)
            if qty > 0:
                return qty
            print("  Error: quantity must be greater than 0.")
        except ValueError:
            print("  Error: please enter a valid whole number (e.g. 5).")


def collect_portfolio():
    """Repeatedly collect stocks and quantities. Returns a list of rows."""
    portfolio = []  # each item: (stock, quantity, price, value)
    print("Available stocks:")
    for stock, price in STOCK_PRICES.items():
        print(f"  {stock:<6} ${price}")
    print()

    while True:
        name = get_stock_name()
        if name is None:
            break
        qty = get_quantity(name)
        price = STOCK_PRICES[name]
        portfolio.append((name, qty, price, price * qty))
        print(f"  Added {qty} x {name} = ${price * qty:,}\n")
    return portfolio


def build_report(portfolio):
    """Return the formatted report as a string."""
    line = "-" * 46
    lines = [
        line,
        f"{'Stock':<8}{'Qty':>6}{'Price':>12}{'Value':>16}",
        line,
    ]
    total = 0
    for name, qty, price, value in portfolio:
        lines.append(f"{name:<8}{qty:>6}{'$' + format(price, ','):>12}"
                     f"{'$' + format(value, ','):>16}")
        total += value
    lines.append(line)
    lines.append(f"{'TOTAL INVESTMENT':<26}{'$' + format(total, ','):>20}")
    lines.append(line)
    return "\n".join(lines), total


def save_txt(report, filename="portfolio.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Stock Portfolio Report\n")
        f.write(f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")
        f.write(report + "\n")
    print(f"Saved to {filename}")


def save_csv(portfolio, total, filename="portfolio.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Stock", "Quantity", "Price", "Value"])
        writer.writerows(portfolio)
        writer.writerow(["TOTAL", "", "", total])
    print(f"Saved to {filename}")


def main():
    print("=== Stock Portfolio Tracker ===\n")
    portfolio = collect_portfolio()

    if not portfolio:
        print("No stocks entered. Goodbye!")
        return

    report, total = build_report(portfolio)
    print("\n" + report + "\n")

    choice = input("Save result? (txt / csv / both / no): ").strip().lower()
    if choice in ("txt", "both"):
        save_txt(report)
    if choice in ("csv", "both"):
        save_csv(portfolio, total)
    if choice not in ("txt", "csv", "both"):
        print("Result not saved.")


if __name__ == "__main__":
    main()
