def format_flags(flags_list):
    """Convert a list of flags into a semicolon-separated string"""
    return ";".join(flags_list)

def is_large_transaction(txn, threshold=1000):
    """Quickly check if a transaction is large"""
    return txn.amount > threshold

def validate_file_path(path):
    """Check if a file exists"""
    import os
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return path
