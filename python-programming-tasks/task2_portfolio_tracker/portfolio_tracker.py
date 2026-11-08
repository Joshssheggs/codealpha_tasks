"""Task 2: Stock Portfolio Tracker.

The user enters stock symbols and quantities. Prices come from a hardcoded
dictionary. The program shows each holding and the total investment value,
and can optionally save the report to a .txt or .csv file.

Run:  python task2_portfolio_tracker/portfolio_tracker.py
"""

import csv
import os

STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 140.00,
    "MSFT": 330.00,
    "AMZN": 125.00,
}


def parse_quantity(raw):
    """Convert text to a positive whole number. Raises ValueError if invalid."""
    value = int(raw.strip())  # raises ValueError for non-integers
    if value <= 0:
        raise ValueError("Quantity must be greater than zero.")
    return value


def add_holding(holdings, symbol, quantity):
    """Add shares to the holdings dict (quantities accumulate per symbol)."""
    symbol = symbol.strip().upper()
    holdings[symbol] = holdings.get(symbol, 0) + quantity
    return holdings


def calculate_portfolio(holdings, prices=STOCK_PRICES):
    """Return (rows, total). Each row is (symbol, quantity, price, value)."""
    rows = []
    total = 0.0
    for symbol, quantity in holdings.items():
        price = prices[symbol]
        value = price * quantity
        rows.append((symbol, quantity, price, value))
        total += value
    return rows, total


def format_report(rows, total):
    """Build a human-readable report string."""
    lines = [
        "STOCK PORTFOLIO REPORT",
        "=" * 52,
        f"{'Symbol':<10}{'Quantity':>10}{'Price':>14}{'Value':>16}",
        "-" * 52,
    ]
    for symbol, quantity, price, value in rows:
        lines.append(f"{symbol:<10}{quantity:>10}{price:>14,.2f}{value:>16,.2f}")
    lines += ["-" * 52, f"{'TOTAL INVESTMENT':<34}{total:>18,.2f}"]
    return "\n".join(lines)


def save_report(path, rows, total):
    """Save the report as .txt or .csv depending on the file extension."""
    extension = os.path.splitext(path)[1].lower()
    if extension == ".csv":
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Quantity", "Price", "Value"])
            for symbol, quantity, price, value in rows:
                writer.writerow([symbol, quantity, f"{price:.2f}", f"{value:.2f}"])
            writer.writerow(["TOTAL", "", "", f"{total:.2f}"])
    elif extension == ".txt":
        with open(path, "w", encoding="utf-8") as f:
            f.write(format_report(rows, total) + "\n")
    else:
        raise ValueError("Unsupported file type. Use a .txt or .csv file name.")


def collect_holdings(input_fn=input, output_fn=print):
    """Interactively collect holdings from the user."""
    holdings = {}
    output_fn("Available stocks: " + ", ".join(
        f"{s} (${p:,.2f})" for s, p in STOCK_PRICES.items()))
    output_fn("Enter a stock symbol and quantity. Type 'done' when finished.\n")

    while True:
        symbol = input_fn("Stock symbol: ").strip().upper()
        if symbol in ("DONE", "Q", "QUIT"):
            break
        if not symbol:
            output_fn("Please enter a symbol.")
            continue
        if symbol not in STOCK_PRICES:
            output_fn(f"'{symbol}' is not available. Choose from: "
                      + ", ".join(STOCK_PRICES))
            continue
        try:
            quantity = parse_quantity(input_fn(f"Quantity of {symbol}: "))
        except ValueError:
            output_fn("Invalid quantity. Enter a whole number greater than 0.")
            continue
        add_holding(holdings, symbol, quantity)
        output_fn(f"Added {quantity} x {symbol}.")
    return holdings


def main():
    try:
        holdings = collect_holdings()
        if not holdings:
            print("No stocks entered. Nothing to calculate.")
            return

        rows, total = calculate_portfolio(holdings)
        print("\n" + format_report(rows, total))

        answer = input("\nSave this report to a file? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            path = input("File name (e.g. portfolio.txt or portfolio.csv): ").strip()
            if not path:
                print("No file name given. Report not saved.")
                return
            if "." not in os.path.basename(path):
                path += ".txt"
            try:
                save_report(path, rows, total)
                print(f"Report saved to {os.path.abspath(path)}")
            except (ValueError, OSError) as error:
                print(f"Could not save the report: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")


if __name__ == "__main__":
    main()
