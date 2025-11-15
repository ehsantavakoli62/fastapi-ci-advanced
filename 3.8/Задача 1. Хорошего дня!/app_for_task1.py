import datetime
from flask import Flask
from typing import Tuple

# Create an instance of the Flask application
app = Flask(__name__)

# Optimal storage for weekdays in Russian
# 0: Monday, 1: Tuesday, ..., 6: Sunday
WEEKDAYS_RU: Tuple[str, ...] = (
    "понедельника", # Monday
    "вторника",    # Tuesday
    "среды",       # Wednesday
    "четверга",    # Thursday
    "пятницы",     # Friday
    "субботы",     # Saturday
    "воскресенья"  # Sunday
)

@app.route('/hello-world/<string:name>')
def hello_world_name(name: str) -> str:
    """
    Returns a greeting message including the provided name and a good wish
    for the current day of the week in Russian.
    """
    current_weekday_index = datetime.datetime.today().weekday()
    weekday_name_ru = WEEKDAYS_RU[current_weekday_index]
    return f"Привет, {name}. Хорошей {weekday_name_ru}!"

if __name__ == '__main__':
    # This block allows running the app directly for testing purposes.
    # In a production environment, a WSGI server would be used.
    app.run(debug=True)
