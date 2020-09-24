from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL
from models import Movies, Actors


class MoviesForm(FlaskForm):
    title = StringField(
        'title', validators=[DataRequired()]
    )
    releaseDate = DateTimeField(
        'releaseDate', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )

    # choices=[
    #     ('AL', 'AL'),
    #     ('AK', 'AK'),
    #     ('AZ', 'AZ'),
    #     ('AR', 'AR')
    # ]


# def get_movies_list():
#     movies_list = []
#     movies = Movies.query.all()
#     for movie in movies:
#         movies_list.append((movie.id, movie.id))
#     return movies_list

def choice_query():
    return Movies.query


class ActorsForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    Age = IntegerField(
        'Age', validators=[DataRequired()]
    )
    gender = SelectField(
        'gender', validators=[DataRequired()],
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
        ]
    )
    image_link = StringField(
        'image_link'
    )
    movie_id = SelectMultipleField(
        'movie_id',
        query_factory=choice_query,
        allow_blank=True,
        get_Label='name'
    )
