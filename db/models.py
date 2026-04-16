from datetime import date

class Position:

    def __init__(self, id: int, tckr: str, shares: float, cost_basis: float, purchase_date: date):
        self.id = id
        self.tckr = tckr
        self.shares = shares
        self.cost_basis = cost_basis
        self.purchase_date = purchase_date