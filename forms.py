"""Forms for playlist app"""

from wtforms import SelectField, StringField, TextAreaField
from flask_wtf import FlaskForm 
form wtforms.validators import InputRequired


class PlaylistForm(FlaskForm):
    """Form for adding playlsit"""

    name = StringField("Name", validators=[InputRequired])
    description = TextAreaField("Description", validators=[InputRequired])


class SongForm(FlaskForm):
    """Form for adding songs"""

    title = StringField("Title", validators=[InputRequired])
    artist = StringField("Artist", validators=[InputRequired])


class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist"""

    song = StringField("Song to Add", coerce=int)