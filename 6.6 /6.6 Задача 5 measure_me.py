import logging
import time
import random
import sys

# Configure logger to output with millisecond precision
# This specific format is required by the problem's analysis.
logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d - %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)

def measure_me():
    logger.info("Enter measure_me")
    time.sleep(random.uniform(0.01, 0.1)) # Simulate some work
    logger.info("Leave measure_me")

if __name__ == '__main__':
    num_runs = 5
    for _ in range(num_runs):
        measure_me()
