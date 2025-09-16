
"""
    Fraud detection rule to flag rapid-fire transactions by a single user.

    Flags a transaction as suspicious if the same user executes more than
    `max_txns` transactions within a rolling window of `window_minutes` minutes.

    Attributes:
        max_txns (int): Maximum allowed transactions in the window before flagging as fraud.
        window (timedelta): Duration of the rolling time window to consider.
        _user_txn_times (defaultdict): Tracks recent transaction timestamps for each user.

    Example:
        Flags if a user makes >3 transactions in any 1-minute window.

    Usage:
        rule = RapidTransactionsRule(max_txns=3, window_minutes=1)
        rule.check(transaction)  # Returns True if transaction is part of a suspicious burst
"""



from fraud_engine.rules.base import Rule
from fraud_engine.schema import Transaction
from collections import defaultdict, deque
from datetime import timedelta

class RapidTransactionsRule(Rule):
    """
    Flags users who make more than `max_txns` within `window_minutes`.
    """

    def __init__(self, max_txns=3, window_minutes=1):
        self.max_txns = max_txns
        self.window = timedelta(minutes=window_minutes)
        # Store recent transaction times per user
        self._user_txn_times = defaultdict(deque)

    def check(self, transaction: Transaction) -> bool:
        now = transaction.timestamp
        user = transaction.user_id
        txns = self._user_txn_times[user]

        # Add new timestamp, drop old ones outside the window
        txns.append(now)
        while txns and (now - txns[0] > self.window):
            txns.popleft()

        # Flag if count exceeds allowed
        return len(txns) > self.max_txns
