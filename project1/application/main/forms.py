from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    query = StringField(label="Query", validators=[
        DataRequired(message=("Query required"))])
    category = SelectField(label="Type of query",
                           validators=[DataRequired(
                               message=("Choice required"))],
                           choices=[
                               ("isbn", "ISBN Number"),
                               ("title", "Title"),
                               ("author", "Author")])


class ReviewForm(FlaskForm):
    isbn = HiddenField()
    username = HiddenField()
    rating = RadioField(label="Rating", validators=[DataRequired(
        message=("Rating required"))], choices=[("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)])
    review = TextAreaField(label="Review", validators=[
        DataRequired(message=("Review required")),
        Length(max=1200, message=("Max 1200 chars"))])
