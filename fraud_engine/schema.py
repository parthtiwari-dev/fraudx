"""
schema.py

Provides data schema validation and preprocessing utilities for the Fraud Detection Engine.

This module ensures every incoming transaction record conforms to the expected schema
— all required fields are present and of correct types (e.g., amount as float, timestamp as datetime).
It acts as the single source of truth for input data integrity and enables robust, 
type-safe processing downstream (rule engine, analytics, etc.).

Key Responsibilities:
    - Validate transaction records for missing, unexpected, or malformed fields.
    - Cast and normalize field types (e.g., convert strings to float/datetime).
    - Raise custom exceptions or handle errors for invalid records.
    - Allow easy extension if the schema changes in the future.

Typical usage:
    from fraud_engine.schema import validate_transaction

    cleaned_txn = validate_transaction(raw_txn_dict)
    # Now safe for rule processing
"""
from fraud_engine.exceptions import InvalidTransactionError
from pydantic import BaseModel, Field, ValidationError 
from datetime import datetime


class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    merchant_id: str
    amount: float
    timestamp: datetime
    # Optional extra fields can be added here

def validate_transaction(raw_txn: dict):
    """
    Validate and normalize a single transaction record.
    
    Args:
        raw_txn (dict): Raw transaction data.
    
    Returns:
        Transaction: Validated and type-safe transaction object.
    
    Raises:
        InvalidTransactionError: If validation fails.
    """
    try:
        txn = Transaction(**raw_txn)
        return txn
    except ValidationError as e:
        raise InvalidTransactionError(f"Transaction validation failed: {e}")


