from flask import Flask
from typing import Dict, Any

# Create an instance of the Flask application
app = Flask(__name__)

# In-memory storage for financial records.
# Structure: {year: {month: total_month_expense}}
# This dictionary will hold the aggregated expenses.
financial_storage: Dict[int, Dict[int, int]] = {}

@app.route('/add/<string:date_str>/<int:number>')
def add_expense(date_str: str, number: int) -> str:
    """
    Adds an expense for a given date.
    The date_str is expected in YYYYMMDD format.
    
    Args:
        date_str (str): The date in YYYYMMDD format.
        number (int): The amount of expense to add.
        
    Returns:
        str: A confirmation message or an error if the date format is invalid.
    """
    try:
        if len(date_str) != 8 or not date_str.isdigit():
            raise ValueError("Date string must be 8 digits long.")

        year = int(date_str[0:4])
        month = int(date_str[4:6])
        # day = int(date_str[6:8]) # Day is not used for aggregation

        if not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12.")
        
        # Ensure the year entry exists in financial_storage
        if year not in financial_storage:
            financial_storage[year] = {}
        
        # Add the expense to the corresponding month
        financial_storage[year][month] = financial_storage[year].get(month, 0) + number
        
        return f"Расход {number} руб. добавлен за {date_str}."

    except (ValueError, IndexError) as e:
        return f"Ошибка: Неправильный формат даты или значение {date_str}. Подробности: {e}"


@app.route('/calculate/<int:year>')
def calculate_year_expenses(year: int) -> str:
    """
    Calculates the total expenses for a specified year.
    
    Args:
        year (int): The year for which to calculate expenses.
        
    Returns:
        str: A message displaying the total expenses for the year.
    """
    total_yearly_expense: int = 0
    if year in financial_storage:
        # Sum all monthly expenses for the given year
        for month_expense in financial_storage[year].values():
            total_yearly_expense += month_expense
    
    return f"Суммарные траты за {year} год: {total_yearly_expense} руб."


@app.route('/calculate/<int:year>/<int:month>')
def calculate_month_expenses(year: int, month: int) -> str:
    """
    Calculates the total expenses for a specified year and month.
    
    Args:
        year (int): The year for which to calculate expenses.
        month (int): The month (1-12) for which to calculate expenses.
        
    Returns:
        str: A message displaying the total expenses for the month.
    """
    total_monthly_expense: int = 0
    # Check if the year and month exist in storage
    if year in financial_storage and month in financial_storage[year]:
        total_monthly_expense = financial_storage[year][month]
    
    # Format month to always have two digits (e.g., 01 for January)
    return f"Суммарные траты за {month:02d}.{year} год: {total_monthly_expense} руб."

if __name__ == '__main__':
    # This block allows running the app directly for testing purposes.
    # In a production environment, a WSGI server would be used.
    app.run(debug=True)
