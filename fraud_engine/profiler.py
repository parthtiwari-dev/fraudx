from scripts.profile_engine import ProfileEngine
from fraud_engine.utils import is_large_transaction

class Profiler:
    """
    Evaluates transactions against dynamic user profiles.
    Returns flags based on deviations from user's historical behavior.
    """

    def __init__(self):
        self.profile_engine = ProfileEngine()

    def evaluate(self, txn):
        """
        Returns list of dynamic flags for the transaction.
        Updates user profile after evaluation.
        """
        flags = []

        # Fetch user's profile
        profile = self.profile_engine.get_profile(txn.user_id)
        avg_amount = profile["avg_amount"]

        # Dynamic large transaction: amount >= 3x user's average
        if avg_amount > 0 and txn.amount >= 3 * avg_amount:
            flags.append("DynamicLargeTransactionRule")

        # Absolute threshold rule
        if is_large_transaction(txn):
            flags.append("LargeTransactionRule")

        # Update user profile after evaluation
        self.profile_engine.update_profile(txn)

        return flags
