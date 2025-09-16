import time
import logging

logger = logging.getLogger("fraud_engine")

def log_execution(func):
    """Logs start, end, and duration of a function"""
    def wrapper(*args, **kwargs):
        logger.info(f"Running {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"{func.__name__} finished in {end - start:.4f}s")
        return result
    return wrapper

def catch_exceptions(func):
    """Decorator to catch exceptions, log, and prevent crashes"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in {func.__name__}: {e}", exc_info=True)
            return None
    return wrapper
