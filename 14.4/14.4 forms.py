# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange

# Class for adding a new book (کلاس برای افزودن کتاب جدید)
class BookForm(FlaskForm):
    """
    Form for adding a new book with input validation (Task 2).
    فرم برای افزودن کتاب جدید با اعتبارسنجی ورودی (وظیفه ۲).
    """
    # Validators: InputRequired() ensures the field is not empty (اعتبارسنج: InputRequired() تضمین می‌کند که فیلد خالی نباشد)
    book_name = StringField('Название книги', validators=[InputRequired(message='Требуется название'), Length(max=255)])
    author = StringField('Автор', validators=[InputRequired(message='Требуется автор'), Length(max=255)])
    publish_year = IntegerField('Год публикации', validators=[
        InputRequired(message='Требуется год'), 
        NumberRange(min=1800, max=2100, message='Год должен быть в диапазоне 1800-2100')
    ])
    ISBN = StringField('ISBN', validators=[InputRequired(message='Требуется ISBN'), Length(max=255)])
    
    submit = SubmitField('Добавить книгу')
