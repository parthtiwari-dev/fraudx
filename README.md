# FraudX - Rule-Based Fraud Detection Engine

## Overview

FraudX is a Python-based fraud detection engine that processes transaction data through configurable rule sets to identify potentially fraudulent activities. The system is built around a modular architecture with pluggable rules, schema validation, and comprehensive logging.

## Project Structure

```
fraudx/
├── fraud_engine/           # Core detection engine
│   ├── rules/              # Rule implementations
│   │   ├── base.py         # Abstract rule interface
│   │   ├── rapid_transaction_rule.py  # Detects rapid transactions
│   │   └── other_rules.py  # Large transaction rules
│   ├── detector.py         # Main fraud detector orchestrator
│   ├── pipeline.py         # Data ingestion pipeline (CSV/JSON/API)
│   ├── schema.py           # Transaction data validation
│   ├── exceptions.py       # Custom exception classes
│   ├── profiler.py         # User behavior profiling
│   ├── decorators.py       # Performance and logging decorators
│   └── utils.py            # Utility functions
├── config/                 # Configuration files
│   ├── logging.yaml        # Logging configuration
│   └── rules.config.yaml   # Rule configuration (max_txns, thresholds)
├── data/                   # Sample data
│   └── sample_transaction.csv  # 201 sample transactions for testing
├── scripts/                # Executable scripts
│   ├── run_detection.py    # Main script to run fraud detection
│   └── profile_engine.py   # User profiling script
├── tests/                  # Test suite
│   ├── test_detector.py    # Tests for fraud detector
│   ├── test_pipeline.py    # Tests for data pipeline
│   ├── test_rules.py       # Tests for fraud rules
│   └── other_test.py       # Additional tests
├── notebooks/              # Analysis notebooks
│   └── fraud_analysis.ipynb  # Jupyter notebook for analysis
├── logs/                   # Generated log files
└── docs/                   # Documentation (placeholder)
```

## Core Components

### 1. Fraud Detection Engine
- **detector.py**: Central orchestrator that applies rules to transactions
- **schema.py**: Pydantic-based validation for transaction data structure
- **pipeline.py**: Streaming data ingestion from CSV, JSON, or API sources

### 2. Rule System
- **base.py**: Abstract Rule class that all fraud rules must implement
- **rapid_transaction_rule.py**: Flags users making >N transactions in M minutes
- **other_rules.py**: Simple threshold-based rules (large amount detection)

### 3. Configuration
- **rules.config.yaml**: Rule parameters (max_txns: 3, window_minutes: 1, threshold: 10000)
- **logging.yaml**: Structured logging to console and files

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Quick Start
```bash
# Clone the repository
git clone https://github.com/parthtiwari-dev/fraudx.git
cd fraudx

# Install dependencies
pip install -r requirements.txt

# Run fraud detection on sample data
python scripts/run_detection.py
```

### Dependencies
- **pydantic==2.11.0**: Data validation and schema definition
- **python-dateutil>=2.9.0**: Date/time parsing utilities
- **pytz>=2024.1**: Timezone handling
- **pytest>=8.0.0**: Testing framework
- **requests**: API data ingestion (used in pipeline.py)
- **pyyaml**: Configuration file parsing

## Usage

### Running Detection
The main script processes the sample transaction data through all configured rules:

```bash
python scripts/run_detection.py
```

This will:
1. Load transaction data from `data/sample_transaction.csv`
2. Apply rules from `config/rules.config.yaml`
3. Generate fraud alerts in `logs/fraud_alerts.csv`
4. Output summary statistics and user profiles
5. Log all activities to `logs/fraud_engine.log`

### Sample Transaction Format
```csv
transaction_id,user_id,amount,timestamp,location,payment_method
1,U117,4126.39,2025-09-01 08:20:06,Hyderabad,NetBanking
2,U108,2946.32,2025-09-01 10:05:40,Indore,CreditCard
```

### Rule Configuration
Edit `config/rules.config.yaml` to adjust detection parameters:
```yaml
rules:
  - type: "RapidTransactionsRule"
    max_txns: 3
    window_minutes: 1
  - type: "LargeTransactionRule"
    threshold: 10000.0
```

### Programmatic Usage
```python
from fraud_engine.detector import FraudDetector
from fraud_engine.rules.rapid_transaction_rule import RapidTransactionsRule
from fraud_engine.rules.other_rules import LargeTransactionRule
from fraud_engine.pipeline import pipeline

# Setup rules
rules = [
    RapidTransactionsRule(max_txns=3, window_minutes=1),
    LargeTransactionRule(threshold=5000.0)
]
detector = FraudDetector(rules)

# Process transactions
for txn in pipeline("data/sample_transaction.csv", source_type="csv"):
    result = detector.evaluate(txn)
    if result["is_fraud"]:
        print(f"FRAUD DETECTED: {txn.transaction_id} - {result['flags']}")
```

## Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_detector.py

# Run with coverage
pytest --cov=fraud_engine
```

## Extending the System

### Creating New Rules
1. Create a new rule class inheriting from `Rule`:
```python
from fraud_engine.rules.base import Rule
from fraud_engine.schema import Transaction

class MyCustomRule(Rule):
    def __init__(self, threshold=1000):
        self.threshold = threshold
    
    def check(self, transaction: Transaction) -> bool:
        # Your fraud detection logic here
        return transaction.amount > self.threshold
```

2. Add it to the rule registry in `scripts/run_detection.py`
3. Configure it in `config/rules.config.yaml`

### Adding New Data Sources
Extend `pipeline.py` to support new data formats or sources.

## Architecture

The system follows a clean, modular architecture:

1. **Data Ingestion**: `pipeline.py` streams validated transactions
2. **Rule Engine**: `detector.py` applies all configured rules
3. **Validation**: `schema.py` ensures data integrity using Pydantic
4. **Profiling**: `profiler.py` tracks user behavior patterns
5. **Logging**: Comprehensive logging for monitoring and debugging

## Output

### Console Output
- Real-time fraud alerts
- Processing statistics
- Top triggered rules
- User behavior profiles

### Generated Files
- `logs/fraud_alerts.csv`: All flagged transactions with reasons
- `logs/fraud_engine.log`: Detailed processing logs

## Current Limitations

- Rules are stateful but not persisted between runs
- No database integration (file-based processing)
- Limited to two basic rule types
- No web interface or API endpoints
- No machine learning components (pure rule-based)

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Add tests for new functionality
4. Run tests: `pytest`
5. Commit changes: `git commit -m 'Add your feature'`
6. Push to branch: `git push origin feature/your-feature`
7. Submit a Pull Request

## License

This project is licensed under the MIT License.

## Author

Parth Tiwari

---

**Note**: This is a rule-based fraud detection engine focused on transaction analysis. It processes data in batch mode and is designed for integration into larger fraud prevention systems.
