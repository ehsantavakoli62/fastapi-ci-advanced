import unittest
import sys
import os

# To import the Flask app and financial_storage from 'finance_app.py',
# ensure it's in the same directory.
try:
    from finance_app import app, financial_storage
except ImportError:
    print("Error: Could not import 'app' and 'financial_storage' from finance_app.py. Ensure the file exists and is accessible.")
    sys.exit(1) # Exit if the app cannot be imported for testing.


class TestFinanceApp(unittest.TestCase):
    """
    Unit tests for the Financial Accounting Flask application.
    Covers adding expenses, calculating monthly/yearly totals,
    and handling invalid inputs and empty storage scenarios.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the Flask test client once for all tests in this class.
        """
        cls.app = app.test_client()
        cls.app.testing = True

    def setUp(self) -> None:
        """
        Reset financial_storage before each test to ensure test isolation.
        Populate with consistent initial data for testing.
        """
        financial_storage.clear() # Clear storage to start fresh for each test

        # Populate with initial data for consistent test scenarios
        financial_storage.update({
            2023: {
                1: 100,  # January 2023 total
                2: 150,  # February 2023 total
                3: 50    # March 2023 total
            },
            2024: {
                1: 200,  # January 2024 total
                2: 250   # February 2024 total
            }
        })

    def test_add_expense_valid_date(self) -> None:
        """
        Tests the /add/ endpoint with various valid dates and amounts.
        Verifies that expenses are correctly added and aggregated in storage.
        """
        # Add to an existing month
        response1 = self.app.get('/add/20230115/75')
        self.assertEqual(response1.status_code, 200)
        self.assertIn("Расход 75 руб. добавлен за 20230115.", response1.data.decode('utf-8'))
        self.assertEqual(financial_storage[2023][1], 100 + 75) # Verify aggregation

        # Add to a new month in an existing year
        response2 = self.app.get('/add/20230401/120')
        self.assertEqual(response2.status_code, 200)
        self.assertIn("Расход 120 руб. добавлен за 20230401.", response2.data.decode('utf-8'))
        self.assertEqual(financial_storage[2023][4], 120)

        # Add to a completely new year and month
        response3 = self.app.get('/add/20250701/500')
        self.assertEqual(response3.status_code, 200)
        self.assertIn("Расход 500 руб. добавлен за 20250701.", response3.data.decode('utf-8'))
        self.assertEqual(financial_storage[2025][7], 500)

    def test_add_expense_invalid_date_format(self) -> None:
        """
        Tests the /add/ endpoint with invalid date formats.
        Verifies that an error message is returned and storage remains unchanged.
        """
        initial_storage_copy = {y: {m: a for m, a in months.items()} for y, months in financial_storage.items()}
        
        # Test cases for invalid date formats
        invalid_dates = [
            '2023-01-25',   # Incorrect separator
            '202301',       # Too short
            '202301010',    # Too long
            'invalid_date', # Non-numeric
            '20231301',     # Invalid month (13)
            '20230001'      # Invalid month (00)
        ]

        for date_str in invalid_dates:
            with self.subTest(f"Invalid date format: {date_str}"):
                response = self.app.get(f'/add/{date_str}/75')
                self.assertEqual(response.status_code, 200)
                # Check for the error message that the app provides
                self.assertIn(f"Ошибка: Неправильный формат даты или значение {date_str}.", response.data.decode('utf-8'))
                # Ensure the storage has not changed
                self.assertEqual(financial_storage, initial_storage_copy)

    def test_calculate_year_expenses(self) -> None:
        """
        Tests the /calculate/<year> endpoint for correct yearly totals.
        """
        # Test for year 2023: 100 (Jan) + 150 (Feb) + 50 (Mar) = 300
        response_2023 = self.app.get('/calculate/2023')
        self.assertEqual(response_2023.status_code, 200)
        self.assertIn("Суммарные траты за 2023 год: 300 руб.", response_2023.data.decode('utf-8'))

        # Test for year 2024: 200 (Jan) + 250 (Feb) = 450
        response_2024 = self.app.get('/calculate/2024')
        self.assertEqual(response_2024.status_code, 200)
        self.assertIn("Суммарные траты за 2024 год: 450 руб.", response_2024.data.decode('utf-8'))

    def test_calculate_year_expenses_empty_storage(self) -> None:
        """
        Tests /calculate/<year> when financial_storage is completely empty.
        Should return 0 for any year.
        """
        financial_storage.clear() # Empty the storage
        response1 = self.app.get('/calculate/2023')
        self.assertEqual(response1.status_code, 200)
        self.assertIn("Суммарные траты за 2023 год: 0 руб.", response1.data.decode('utf-8'))

        response2 = self.app.get('/calculate/2025') # Non-existent year
        self.assertEqual(response2.status_code, 200)
        self.assertIn("Суммарные траты за 2025 год: 0 руб.", response2.data.decode('utf-8'))

    def test_calculate_month_expenses(self) -> None:
        """
        Tests the /calculate/<year>/<month> endpoint for correct monthly totals.
        """
        # Test for January 2023 (expected: 100)
        response_2023_1 = self.app.get('/calculate/2023/1')
        self.assertEqual(response_2023_1.status_code, 200)
        self.assertIn("Суммарные траты за 01.2023 год: 100 руб.", response_2023_1.data.decode('utf-8'))

        # Test for February 2024 (expected: 250)
        response_2024_2 = self.app.get('/calculate/2024/2')
        self.assertEqual(response_2024_2.status_code, 200)
        self.assertIn("Суммарные траты за 02.2024 год: 250 руб.", response_2024_2.data.decode('utf-8'))
    
    def test_calculate_month_expenses_non_existent(self) -> None:
        """
        Tests /calculate/<year>/<month> for months or years that do not exist in storage.
        Should return 0.
        """
        # Month 4 does not exist for 2023 in our initial data
        response1 = self.app.get('/calculate/2023/4')
        self.assertEqual(response1.status_code, 200)
        self.assertIn("Суммарные траты за 04.2023 год: 0 руб.", response1.data.decode('utf-8'))

        # Year 2025 does not exist in our initial data
        response2 = self.app.get('/calculate/2025/1')
        self.assertEqual(response2.status_code, 200)
        self.assertIn("Суммарные траты за 01.2025 год: 0 руб.", response2.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
