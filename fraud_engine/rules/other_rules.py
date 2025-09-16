from fraud_engine.rules.base import Rule
from fraud_engine.schema import Transaction


class LargeTransactionRule(Rule):
    """Flags transactions above a certain threshold amount."""

    def __init__(self, threshold: float = 10000.0):
        self.threshold = threshold

    def check(self, transaction: Transaction) -> bool:
        return transaction.amount > self.threshold


