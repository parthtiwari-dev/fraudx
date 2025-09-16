# scripts/run_detection.py
import os
import csv
import logging
import logging.config
import yaml
from collections import Counter

from fraud_engine.pipeline import pipeline
from fraud_engine.detector import FraudDetector
from fraud_engine.schema import validate_transaction
from fraud_engine.utils import format_flags, validate_file_path
from scripts.profile_engine import ProfileEngine

from fraud_engine.rules.rapid_transaction_rule import RapidTransactionsRule
from fraud_engine.rules.other_rules import LargeTransactionRule

# --- Setup logs ---
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING_CONFIG = os.path.join(os.path.dirname(__file__), "../config/logging.yaml")
validate_file_path(LOGGING_CONFIG)
with open(LOGGING_CONFIG, "r") as f:
    config = yaml.safe_load(f)

# Update file paths in YAML
for h in config.get("handlers", {}).values():
    if "filename" in h:
        h["filename"] = os.path.join(LOG_DIR, os.path.basename(h["filename"]))

logging.config.dictConfig(config)
logger = logging.getLogger("fraud_engine")

# --- Load rules config ---
RULES_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "../config/rules.config.yaml")
validate_file_path(RULES_CONFIG_FILE)
with open(RULES_CONFIG_FILE, "r") as f:
    rules_config = yaml.safe_load(f)

RULE_CLASSES = {
    "RapidTransactionsRule": RapidTransactionsRule,
    "LargeTransactionRule": LargeTransactionRule,
}

def build_rules(config_list):
    rules = []
    for r_conf in config_list:
        cls_name = r_conf.pop("type", None)
        cls = RULE_CLASSES.get(cls_name)
        if cls is None:
            logger.warning(f"Unknown rule type: {cls_name}, skipping...")
            continue
        rules.append(cls(**r_conf))
    return rules

def main():
    try:
        source = os.path.join(os.path.dirname(__file__), "../data/sample_transaction.csv")
        validate_file_path(source)
        logger.info(f"Starting Fraud Detection on: {source}")

        rules = build_rules(rules_config.get("rules", []))
        detector = FraudDetector(rules)
        profiler = ProfileEngine()

        total, fraud_count = 0, 0
        rule_counter, user_counter = Counter(), Counter()
        flagged_rows = []

        for txn in pipeline(source, source_type="csv"):
            total += 1
            profiler.update_profile(txn)

            try:
                result = detector.evaluate(txn)
            except Exception as e:
                logger.warning(f"Error evaluating txn {txn.transaction_id}: {e}")
                continue

            if result.get("is_fraud"):
                fraud_count += 1
                for r in result.get("flags", []):
                    rule_counter[r] += 1
                user_counter[txn.user_id] += 1
                flagged_rows.append({
                    "transaction_id": txn.transaction_id,
                    "user_id": txn.user_id,
                    "flags": format_flags(result.get("flags", []))
                })
                logger.warning(f"ALERT: txn={txn.transaction_id} user={txn.user_id} flags={result.get('flags', [])}")

        # Write flagged transactions
        out_csv = os.path.join(LOG_DIR, "fraud_alerts.csv")
        if flagged_rows:
            with open(out_csv, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["transaction_id", "user_id", "flags"])
                writer.writeheader()
                writer.writerows(flagged_rows)
            logger.info(f"Wrote {len(flagged_rows)} flagged transactions to: {out_csv}")
        else:
            logger.info("No flagged transactions to write.")

        # --- Summary ---
        logger.info("=== Detection Summary ===")
        logger.info(f"Total transactions processed: {total}")
        logger.info(f"Total flagged (fraud): {fraud_count}")
        logger.info("Top rules fired:")
        for rule, cnt in rule_counter.most_common():
            logger.info(f"  {rule}: {cnt}")
        logger.info("Top flagged users:")
        for user, cnt in user_counter.most_common(10):
            logger.info(f"  {user}: {cnt}")

        # --- Profile summary ---
        logger.info("=== User Profile Summary ===")
        for user, stats in profiler.summary().items():
            logger.info(f"User {user}: {stats}")

    except Exception as e:
        logger.exception(f"Fatal error in fraud detection: {e}")

if __name__ == "__main__":
    main()
