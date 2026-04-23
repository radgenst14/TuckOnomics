from datetime import date
from db import Database
from db import Position

DIVIDER = "─" * 44

class Orchestrator:
    menu = (
        f"\n{DIVIDER}\n"
        "  TuckOnomics Menu\n"
        f"{DIVIDER}\n"
        "  1) Display All Positions\n"
        "  2) Add New Position\n"
        "  3) Remove Position\n"
        "  q) Quit\n"
        f"{DIVIDER}\n"
        "  Selection: "
    )

    valid_menu_inputs = ["1", "2", "3", "q"]

    def __init__(self) -> None:
        pass

    def menu_input(self) -> str:
        while True:
            opt = input(self.menu)
            if opt in self.valid_menu_inputs:
                return opt

    def display_all_positions(self, db: Database):
        positions = db.get_all_positions()

        header = f"  {'TICKER':<8} {'SHARES':>10} {'COST BASIS':>12} {'DATE':>12}"
        print(f"\n{DIVIDER}")
        print("  Portfolio Positions")
        print(DIVIDER)
        if not positions:
            print("  No positions found.")
        else:
            print(header)
            print(f"  {'─'*8} {'─'*10} {'─'*12} {'─'*12}")
            for p in positions:
                print(f"  {p.tckr:<8} {p.shares:>10.4f} {p.cost_basis:>12.2f} {str(p.purchase_date):>12}")
        print(DIVIDER)

    def add_position(self, db: Database):
        print(f"\n{DIVIDER}")
        print("  Add New Position")
        print(DIVIDER)
        while True:
            tckr        = input("  Ticker:            ").upper()
            shares      = float(input("  Shares:            "))
            cost_basis  = float(input("  Avg Cost Basis:    "))
            purchase_date = date.fromisoformat(input("  Date (YYYY-MM-DD): "))

            print(f"\n{DIVIDER}")
            print(f"  {'Ticker:':<18} {tckr}")
            print(f"  {'Shares:':<18} {shares:.4f}")
            print(f"  {'Avg Cost Basis:':<18} {cost_basis:.2f}")
            print(f"  {'Purchase Date:':<18} {purchase_date}")
            print(DIVIDER)

            confirm = input("  Confirm? [y / Enter to retry / q to cancel]: ").strip().lower()
            if confirm == "y":
                return db.add_position(tckr, shares, cost_basis, purchase_date)
            elif confirm == "q":
                print("  Cancelled.")
                return

    def remove_position(self, db: Database):
        print(f"\n{DIVIDER}")
        print("  Remove Position")
        print(DIVIDER)
        tckr = input("  Ticker:            ").upper()
        purchase_date = date.fromisoformat(input("  Date (YYYY-MM-DD): "))
        db.remove_position(tckr, purchase_date)
        print(f"  Removed {tckr} ({purchase_date}).")
        print(DIVIDER)

    def run(self):
        print(f"\n{'═' * 44}")
        print("  Welcome to TuckOnomics")
        print(f"{'═' * 44}")
        db_name = input("  Database name: ").strip()
        db = Database(db_name)

        opt = input("  Enter 'd' to delete this database, or press Enter to continue: ").strip().lower()

        if opt == "d":
            db.remove_db()
            print("  Database deleted. Goodbye.")
            return

        while True:
            opt = self.menu_input()

            if opt == "1":
                self.display_all_positions(db)

            elif opt == "2":
                self.add_position(db)

            elif opt == "3":
                self.remove_position(db)

            elif opt == "q":
                print(f"\n  Goodbye.\n{'═' * 44}\n")
                break
