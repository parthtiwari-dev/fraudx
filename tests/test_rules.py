from fraud_engine.rules.rapid_transaction_rule import RapidTransactionsRule
from fraud_engine.rules.other_rules import LargeTransactionRule
from fraud_engine.schema import Transaction
from datetime import datetime, timedelta

def make_txn(id, user, amount, ts, location="NY", payment_method="CreditCard"):
    return Transaction(
        transaction_id=id,
        user_id=user,
        merchant_id="m1",  # you can give dummy merchant_id
        amount=amount,
        timestamp=ts,
        location=location,
        payment_method=payment_method
    )

def test_rapid_rule():
    rule = RapidTransactionsRule(max_txns=2, window_minutes=1)
    t1 = make_txn("1", "u1", 50, datetime.now())
    t2 = make_txn("2", "u1", 50, datetime.now() + timedelta(seconds=10))
    t3 = make_txn("3", "u1", 50, datetime.now() + timedelta(seconds=20))

    assert not rule.check(t1)
    assert not rule.check(t2)
    assert rule.check(t3)

def test_large_transaction_rule():
    rule = LargeTransactionRule(threshold=100)
    txn_small = make_txn("4", "u2", 50, datetime.now())
    txn_large = make_txn("5", "u2", 150, datetime.now())

    assert not rule.check(txn_small)
    assert rule.check(txn_large)
