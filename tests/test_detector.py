from fraud_engine.detector import FraudDetector
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
        payment_method=payment_method,
    )


def test_detector_combined():
    rules = [
        RapidTransactionsRule(max_txns=1, window_minutes=1),
        LargeTransactionRule(threshold=100),
    ]
    detector = FraudDetector(rules)

    t1 = make_txn("1", "u1", 50, datetime.now())
    t2 = make_txn("2", "u1", 200, datetime.now() + timedelta(seconds=10))

    result1 = detector.evaluate(t1)
    result2 = detector.evaluate(t2)

    assert not result1["is_fraud"]
    assert result2["is_fraud"]
    assert "LargeTransactionRule" in result2["flags"]
