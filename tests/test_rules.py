# tests/test_rules.py
from fraud_engine.rules.other_rules import LargeTransactionRule
from fraud_engine.schema import Transaction
from datetime import datetime

def test_large_transaction_rule_triggers():
    rule = LargeTransactionRule(threshold=1000)
    txn = Transaction(transaction_id="t1", user_id="u1", amount=2000.0,
                      timestamp=datetime.now(), location="X", payment_method="Y")
    assert rule.check(txn) is True

def test_large_transaction_rule_not_trigger():
    rule = LargeTransactionRule(threshold=5000)
    txn = Transaction(transaction_id="t2", user_id="u2", amount=2000.0,
                      timestamp=datetime.now(), location="X", payment_method="Y")
    assert rule.check(txn) is False
