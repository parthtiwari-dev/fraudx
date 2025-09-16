# scripts/run_detection.py
import os
import csv
import logging
from collections import Counter, defaultdict

from fraud_engine.pipeline import pipeline
from fraud_engine.detector import FraudDetector
from fraud_engine.rules.rapid_transaction_rule import RapidTransactionsRule
from fraud_engine.rules.other_rules import LargeTransactionRule

# --- logging setup ---
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "fraud_engine.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("fraudx.run_detection")


def main():
    # Pipeline source (relative to repo root)
    source = "data/sample_transaction.csv"  # keep matching your CSV name

    # Initialize rules + detector (stream-safe)
    rules = [
        RapidTransactionsRule(max_txns=3, window_minutes=1),
        LargeTransactionRule(threshold=10000.0),
    ]
    detector = FraudDetector(rules)

    # Stats
    total = 0
    fraud_count = 0
    rule_counter = Counter()
    user_counter = Counter()
    flagged_rows = []

    # Stream transactions from pipeline (pipeline() should yield validated Transaction objects)
    for txn in pipeline(source, source_type="csv"):
        total += 1
        result = detector.evaluate(txn)
        if result["is_fraud"]:
            fraud_count += 1
            for r in result["flags"]:
                rule_counter[r] += 1
            user_counter[result["user_id"]] += 1

            # store a small record for CSV output
            flagged_rows.append({
                "transaction_id": result["transaction_id"],
                "user_id": result["user_id"],
                "flags": ";".join(result["flags"]),
            })
            logger.warning(f"ALERT: txn={result['transaction_id']} user={result['user_id']} flags={result['flags']}")

    # Write flagged transactions to disk
    out_csv = os.path.join(LOG_DIR, "fraud_alerts.csv")
    if flagged_rows:
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["transaction_id", "user_id", "flags"])
            writer.writeheader()
            writer.writerows(flagged_rows)
        logger.info(f"Wrote {len(flagged_rows)} flagged transactions to: {out_csv}")
    else:
        logger.info("No flagged transactions to write.")

    # Summary
    logger.info("=== Detection Summary ===")
    logger.info(f"Total transactions processed: {total}")
    logger.info(f"Total flagged (fraud): {fraud_count}")
    logger.info("Top rules fired:")
    for rule, cnt in rule_counter.most_common():
        logger.info(f"  {rule}: {cnt}")
    logger.info("Top flagged users:")
    for user, cnt in user_counter.most_common(10):
        logger.info(f"  {user}: {cnt}")


if __name__ == "__main__":
    main()
