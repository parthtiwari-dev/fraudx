"""
detector.py

Core detection engine for orchestrating rule-based fraud detection. 
Accepts a stream of validated transactions and a set of fraud rules,
and emits any transactions flagged as suspicious (along with which rules flagged them).

Typical usage:
    detector = Detector([RapidTransactionsRule(), LargeAmountRule()])
    for flagged_txn, triggered_rules in detector.detect(stream):
        print(flagged_txn, triggered_rules)
"""
# fraud_engine/detector.py
from typing import List, Dict
from fraud_engine.schema import Transaction
from fraud_engine.rules.base import Rule


class FraudDetector:
    """
    Central fraud detection engine.
    Loads and executes rules against incoming transactions.
    """

    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def evaluate(self, transaction: Transaction) -> Dict:
        """
        Run all rules on a transaction.

        Returns:
            dict: {
                "transaction_id": str,
                "flags": [rule_names_that_triggered],
                "is_fraud": bool
            }
        """
        flags = []

        for rule in self.rules:
            try:
                if rule.check(transaction):
                    flags.append(rule.__class__.__name__)
            except Exception as e:
                # optional: log instead of breaking
                print(f"[ERROR] Rule {rule.__class__.__name__} failed: {e}")

        return {
            "transaction_id": transaction.transaction_id,
            "flags": flags,
            "is_fraud": len(flags) > 0
        }
