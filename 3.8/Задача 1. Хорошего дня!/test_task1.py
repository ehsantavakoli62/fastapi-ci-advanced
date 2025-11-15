import unittest
import datetime
from freezegun import freeze_time
import sys
import os

# To import the Flask app from 'app_for_task1.py', ensure it's in the same directory.
# If your Flask app is in a different structure, you might need to adjust this import.
try:
    from app_for_task1 import app, WEEKDAYS_RU
except ImportError:
    # Fallback: if the above import fails, assume the app code is directly here for local testing.
    # In a real scenario, you would ensure the import path is correct.
    print("Warning: Could not import Flask app from app_for_task1.py. Ensure the file exists and is accessible.")
    sys.exit(1) # Exit if the app cannot be imported for testing.


class TestHelloWorldEndpoint(unittest.TestCase):
    """
    Unit tests for the /hello-world/<name> Flask endpoint.
    Ensures correct weekday generation and handling of various names.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the Flask test client once for all tests in this class.
        """
        cls.app = app.test_client()
        cls.app.testing = True

    def test_can_get_correct_username_with_weekdate(self) -> None:
        """
        Tests if the endpoint correctly returns the greeting with the provided
        username and the dynamically calculated (and frozen) correct weekday.
        Covers all 7 days of the week.
        """
        # Define test dates and their corresponding Russian weekday names.
        # Weekday index: 0=Monday, 6=Sunday.
        test_cases = [
            ("2023-01-02", "понедельника"), # Monday
            ("2023-01-03", "вторника"),     # Tuesday
            ("2023-01-04", "среды"),        # Wednesday
            ("2023-01-05", "четверга"),     # Thursday
            ("2023-01-06", "пятницы"),      # Friday
            ("2023-01-07", "субботы"),      # Saturday
            ("2023-01-08", "воскресенья")  # Sunday
        ]

        for date_str, expected_weekday_ru in test_cases:
            with self.subTest(f"Testing date: {date_str}"):
                with freeze_time(date_str):
                    test_name = "Tester"
                    expected_response_text = f"Привет, {test_name}. Хорошей {expected_weekday_ru}!"
                    
                    response = self.app.get(f'/hello-world/{test_name}')
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.data.decode('utf-8'), expected_response_text)

    def test_username_as_wish_for_weekday(self) -> None:
        """
        Tests scenarios where the username itself contains a weekday wish.
        The endpoint should always return the *actual* current weekday, not the one in the username.
        """
        # Simulate a specific date, e.g., a Friday.
        fixed_date = "2023-11-17" # This is a Friday
        with freeze_time(fixed_date):
            username_with_wish = "Good_Wednesday" # The username suggests Wednesday
            actual_weekday_index = datetime.datetime.strptime(fixed_date, "%Y-%m-%d").weekday()
            actual_weekday_ru = WEEKDAYS_RU[actual_weekday_index] # Should be 'пятницы' (Friday)

            expected_response_text = f"Привет, {username_with_wish}. Хорошей {actual_weekday_ru}!"
            
            response = self.app.get(f'/hello-world/{username_with_wish}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode('utf-8'), expected_response_text)
            self.assertIn(actual_weekday_ru, response.data.decode('utf-8')) # Check actual weekday is present
            self.assertNotIn("среды", response.data.decode('utf-8')) # Ensure "среды" (Wednesday) is NOT used as the actual weekday

    def test_different_valid_names(self) -> None:
        """
        Tests the endpoint with various valid usernames to ensure proper integration.
        """
        # Fix the date to a Thursday for consistent testing.
        with freeze_time("2023-01-05"): # Thursday
            expected_weekday_ru = WEEKDAYS_RU[datetime.datetime(2023, 1, 5).weekday()] # Should be 'четверга'
            
            names_to_test = ["Ivan", "Maria", "Petr", "Alexey"]
            for name in names_to_test:
                with self.subTest(f"Testing name: {name}"):
                    expected_response_text = f"Привет, {name}. Хорошей {expected_weekday_ru}!"
                    response = self.app.get(f'/hello-world/{name}')
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.data.decode('utf-8'), expected_response_text)

if __name__ == '__main__':
    # Ensure 'freezegun' is installed: pip install freezegun
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
