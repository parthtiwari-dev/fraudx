from fraud_engine.pipeline import pipeline
from fraud_engine.detector import FraudDetector
from fraud_engine.rules.rapid_transaction_rule import RapidTransactionsRule
from fraud_engine.rules.other_rules import LargeTransactionRule

def main():
    # 1. Stream validated transactions directly from pipeline
    txns = pipeline("data/sample_transaction.csv", source_type="csv")

    # 2. Initialize rules and detector
    rules = [
        RapidTransactionsRule(max_txns=4, window_minutes=1),
        LargeTransactionRule(threshold=4000)
    ]
    detector = FraudDetector(rules)

    # 3. Evaluate each transaction for fraud
    for txn in txns:
        result = detector.evaluate(txn)
        if result["is_fraud"]:
            print(f"⚠️ Fraud detected for transaction {result['transaction_id']}: {result['flags']}")

if __name__ == "__main__":
    main()
