import pytest
import os
import sys
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta

from time_analyzer import run_and_capture_logs, analyze_measurement_logs, LOG_FILE_FOR_MEASUREMENT, MEASURE_ME_SCRIPT


@pytest.fixture
def create_dummy_measure_me_script(tmp_path):
    """
    Creates a dummy measure_me.py script in a temporary directory
    that logs with millisecond precision to stdout.
    """
    script_path = tmp_path / MEASURE_ME_SCRIPT
    script_content = """
import logging
import time
import random
import sys

# Configure logger to output with millisecond precision to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d - %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)

def measure_me():
    logger.info("Enter measure_me")
    time.sleep(random.uniform(0.001, 0.005)) # Simulate very fast work for tests
    logger.info("Leave measure_me")

if __name__ == '__main__':
    num_runs = 3 # Run a few times for average
    for _ in range(num_runs):
        measure_me()
"""
    script_path.write_text(script_content)
    return script_path

@pytest.fixture
def mock_log_file_path(tmp_path):
    """
    Fixture to provide a temporary log file path and ensure it's clean.
    """
    log_file_path = tmp_path / LOG_FILE_FOR_MEASUREMENT
    if log_file_path.exists():
        log_file_path.unlink()
    return log_file_path

@pytest.fixture(autouse=True)
def chdir_to_tmp_path(tmp_path, monkeypatch):
    """
    Change the current working directory to tmp_path for each test
    to ensure scripts and log files are found correctly.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, 'executable', sys.executable)


def test_run_and_capture_logs_success(create_dummy_measure_me_script, mock_log_file_path):
    """
    Test that run_and_capture_logs executes the script and writes output to the log file.
    """
    assert create_dummy_measure_me_script.exists()
    
    success = run_and_capture_logs()
    assert success is True
    assert mock_log_file_path.exists()
    
    with open(mock_log_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "Enter measure_me" in content
        assert "Leave measure_me" in content
        assert content.count("Enter measure_me") == 3
        assert content.count("Leave measure_me") == 3

def test_run_and_capture_logs_script_not_found(monkeypatch, mock_log_file_path, capsys):
    """
    Test that run_and_capture_logs handles the case where measure_me.py is not found.
    """
    monkeypatch.setattr('time_analyzer.MEASURE_ME_SCRIPT', 'non_existent_script.py')
    
    success = run_and_capture_logs()
    assert success is False
    assert not mock_log_file_path.exists()
    captured = capsys.readouterr()
    assert "Error: Script 'non_existent_script.py' not found" in captured.err

def test_analyze_measurement_logs_correct_average(mock_log_file_path):
    """
    Test that analyze_measurement_logs correctly calculates the average time.
    """
    log_content = """
2023-01-01 10:00:00,100 - Enter measure_me
2023-01-01 10:00:00,200 - Leave measure_me
2023-01-01 10:00:01,500 - Enter measure_me
2023-01-01 10:00:01,750 - Leave measure_me
2023-01-01 10:00:02,000 - Enter measure_me
2023-01-01 10:00:02,500 - Leave measure_me
"""
    mock_log_file_path.write_text(log_content)
    
    expected_average = (0.1 + 0.25 + 0.5) / 3
    
    average_time = analyze_measurement_logs()
    assert average_time == pytest.approx(expected_average)

def test_analyze_measurement_logs_no_entries(mock_log_file_path):
    """
    Test that analyze_measurement_logs handles an empty log file.
    """
    mock_log_file_path.write_text("")
    average_time = analyze_measurement_logs()
    assert average_time == -1.0

def test_analyze_measurement_logs_mismatched_entries(mock_log_file_path, capsys):
    """
    Test that analyze_measurement_logs handles mismatched Enter/Leave entries.
    It should still calculate for valid pairs.
    """
    log_content = """
2023-01-01 10:00:00,100 - Enter measure_me
2023-01-01 10:00:00,200 - Leave measure_me
2023-01-01 10:00:01,500 - Leave measure_me
2023-01-01 10:00:01,750 - Enter measure_me
"""
    mock_log_file_path.write_text(log_content)
    average_time = analyze_measurement_logs()
    assert average_time == pytest.approx(0.1)

def test_analyze_measurement_logs_invalid_format(mock_log_file_path):
    """
    Test that analyze_measurement_logs gracefully handles lines with invalid format.
    """
    log_content = """
2023-01-01 10:00:00,100 - Enter measure_me
INVALID LINE HERE
2023-01-01 10:00:00,200 - Leave measure_me
"""
    mock_log_file_path.write_text(log_content)
    average_time = analyze_measurement_logs()
    assert average_time == pytest.approx(0.1)

def test_analyze_measurement_logs_log_file_not_found(monkeypatch, capsys):
    """
    Test handling when the log file itself is not found for analysis.
    """
    monkeypatch.setattr('time_analyzer.LOG_FILE_FOR_MEASUREMENT', 'non_existent_log.log')
    average_time = analyze_measurement_logs()
    assert average_time == -1.0
    captured = capsys.readouterr()
    assert "Error: Log file 'non_existent_log.log' not found for analysis." in captured.err
