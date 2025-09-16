from fraud_engine.pipeline import pipeline
from fraud_engine.schema import validate_transaction


def test_pipeline_csv(tmp_path):
    # Create a temporary CSV
    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(
        "transaction_id,user_id,amount,timestamp,location,payment_method\n"
        "1,u1,100,2025-09-16 10:00:00,NY,CreditCard"
    )

    records = list(pipeline(str(csv_file), source_type="csv"))
    assert len(records) == 1
    txn = records[0]
    assert txn.transaction_id == "1"
    assert txn.amount == 100

