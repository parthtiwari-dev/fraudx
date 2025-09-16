"""
base.py

Defines the base interface/abstract contract for all fraud detection rules
used within the Fraud Detection Engine.

Every fraud rule should inherit from and implement this interface, which
guarantees a standard method signature for checking whether a transaction
is suspicious according to a specific heuristic or policy.

Key Responsibilities:
    - Serve as the blueprint for all modular fraud rules.
    - Enforce a consistent interface for rule registration, configuration, and application.
    - Enable extensibility (easy to add, remove, or swap rules without changing the engine core).
    - Support both simple (stateless) and complex (stateful/history-aware) rules.

Typical usage:
    class MyRule(FraudRule):
        def check(self, txn: Transaction) -> bool:
            # Logic to evaluate transaction
            ...
"""

# fraud_engine/rules/base.py

from abc import ABC, abstractmethod
from fraud_engine.schema import Transaction


class Rule(ABC):
    """Abstract base class for all fraud detection rules."""

    @abstractmethod
    def check(self, transaction: Transaction) -> bool:
        """
        Check if the transaction is fraudulent.

        Args:
            transaction (Transaction): Validated transaction object.

        Returns:
            bool: True if transaction is suspicious/fraudulent, False otherwise.
        """
        pass
