"""
pipeline.py

Core data streaming and ingestion logic for the Fraud Detection Engine.

This module provides efficient, memory-safe generators to stream transaction records 
(one at a time) from CSV or other data sources for further real-time or batch analysis.

Key Responsibilities:
    - Read large or continuous datasets efficiently using Python generators.
    - Validate and parse transaction input data (schema can be custom/plugged in).
    - Yield each transaction as a Python dict (or validated object).
    - Serve as the foundational data layer for rule-based and ML-based detection.
    - Easily extensible for new sources, formats, or preprocessing steps.

Typical usage:
    from fraud_engine.pipeline import stream_transactions

    for txn in stream_transactions("data/sample_transactions.csv"):
        print(txn)

Author: Parth Tiwari
Created: 2025-09-11
"""
import csv
import requests  # type: ignore
import json
import os
from fraud_engine.schema import validate_transaction
from fraud_engine.exceptions import InvalidTransactionError


def pipeline(source, source_type='csv'):
    """
    Generic pipeline to read data from CSV, JSON, or API
    and validate each record using schema.py.
    
    Args:
        source (str): Path to file or API endpoint.
        source_type (str): 'csv', 'json', or 'api'
        
    Yields:
        Transaction: Validated Pydantic Transaction object
    """
    if source_type == 'csv':
        # Build absolute path relative to project root
        base_dir = os.path.dirname(os.path.dirname(__file__))  # fraudx/
        file_path = os.path.join(base_dir, source)

        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    yield validate_transaction(row)
                except InvalidTransactionError as e:
                    print(f"Skipping invalid transaction: {e}")

    elif source_type == 'json':
        base_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_dir, source)

        with open(file_path, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            for row in data:
                try:
                    yield validate_transaction(row)
                except InvalidTransactionError as e:
                    print(f"Skipping invalid transaction: {e}")

    elif source_type == 'api':
        response = requests.get(source)
        data = response.json()
        for row in data:
            try:
                yield validate_transaction(row)
            except InvalidTransactionError as e:
                print(f"Skipping invalid transaction: {e}")

    else:
        raise ValueError("Unsupported source_type. Use 'csv', 'json', or 'api'.")
