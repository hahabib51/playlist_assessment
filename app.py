from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

from os import environ

app  = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI', postgresql:///playlist_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "MyPassWordsASecret"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def root():
    """HOMEPAGE: redirect to /playlists."""

    return redirect("/playlist")

  ############################################################################################################################
  #PLAYLIST routes

@app.route("/playlists")
def show_all_playlists():
    #"""Return a list of playlists."""

    playlist = Playlist.query.all()
    return render_template("playlist.html", playlists=playlists)

  
@app.route("/playlist/<int:playlist_id>")
def show_playlist(playlist_id):
      #"""GET specific playlist details"""

      playlist = Playlist.query.get_or_404(playlist_id)
      songs = Songs.query.filter(Song.playlists.any(id=playlist_id)).all()

      return render_template('playlist.html', playlist=playlist, songs=songs)

  
@app.route("/playlists/add", methods["GET", "POST"])
def add_playlist():
    #"""HANDLE add-playlist form"""

    form = PlaylistForm()

    if form.validate_on_submit():
      name = form.name.data
      description = form.description.data
      playlist = Playlist(name=name, description=description)
      db.session.add(playlist)
      db.session.commit()
      return redirect("/playlists")

    else:
        return render_template("new_playlist.html", form=form

  ############################################################################################################################
  #Song routes

@app.route("/songs")
def show_all_songs():
    #"""Show list of songs"""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)

@app.route("/songs/<int:song_id>")
def show_song(song_id):
    #"""RETURN a specific song"""

    song = Song.query.get_or_404(song_id)
    playlists = Playlist.query.filter(Playlist.song.any(id=song_id)).all()

    return render_template("songs.html", playlists=playlists)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    #"""HANDLE add-song form"""

    form = SongForm()

    if form.validate_on_submit():
      title = form.title.data
      aritst = form.artist.data 
      song = Song(tite=title, artist=artist)
      db.session.add(song)
      db.session.commit()
      return redirect("/playlist")

    else: 
      return render_template("new_playlist.html", form=form)

##################################################################################
#SONG routes

@app.route("/songs")
def show_all_songs():
    #"""Show list of songs"""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)

@app.route("/songs/<int:song_id>")
def show_song(song_id):
    #"""return specific song"""

    song = Song.query.get_or_404(song_id)
    playlists = Playlists.query.filter(Playlist.song.any(id=song_id)).all()

    return render_template('song.html', song=song, playlists=playlists)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    #"""HANDLE add-song form"""

    form = SongForm()

    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data
        song = Song(title=title, artist=artist, artist)
        db.session.add(song)
        db.session.commit()
        return redirect("/songs")
      
    else: 
        return render_template("new_song.html", form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    #"""Add a playlist and redirect to list"""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    curr_on_playlist = [s.id for s in playlist.songs]
    form.song.choices = (db.session.query(Song.id, Song.title).filter(Song.id.notin_(curr_on_playlist)).all())

    if form.validate_on_submit():

        playlist_song = PlaylistSong(song_id=form.song.data, playlist_id=playlist_id)
        db.session.add(playlist_song)
        db.session.commit()

        return redirect(f"/playlists{playlist_id}")

    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)

if __name__ == "__main__":
    app.run()