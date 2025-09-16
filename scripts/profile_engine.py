from collections import defaultdict
from fraud_engine.schema import Transaction

class ProfileEngine:
    """
    Maintains user profiles:
    - total transactions
    - total amount
    - average amount
    """

    def __init__(self):
        self.user_profiles = defaultdict(lambda: {
            "total_txn": 0,
            "total_amount": 0.0,
            "avg_amount": 0.0
        })

    def update_profile(self, txn: Transaction):
        profile = self.user_profiles[txn.user_id]
        profile["total_txn"] += 1
        profile["total_amount"] += txn.amount
        profile["avg_amount"] = profile["total_amount"] / profile["total_txn"]

    def get_profile(self, user_id):
        return self.user_profiles.get(user_id, {
            "total_txn": 0,
            "total_amount": 0.0,
            "avg_amount": 0.0
        })

    def summary(self):
        return dict(self.user_profiles)
