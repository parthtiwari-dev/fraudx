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
import requests # type: ignore
import json

def pipeline(source, source_type='csv'):
    """
    Generic pipeline to read data from CSV, JSON, or API.
    
    Args:
        source (str): Path to file or API endpoint.
        source_type (str): 'csv', 'json', or 'api'
        
    Yields:
        dict: One record at a time
    """
    if source_type == 'csv':
        with open(source, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row

    elif source_type == 'json':
        with open(source, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            for row in data:
                yield row

    elif source_type == 'api':
        response = requests.get(source)
        data = response.json()
        for row in data:
            yield row

    else:
        raise ValueError("Unsupported source_type. Use 'csv', 'json', or 'api'.")
