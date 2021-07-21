from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# CREATING A LIST OF MUSIC OF THIS TIME
time = input("What year you would like to travel to in YYY-MM-DD format? ")
URL = f"https://www.billboard.com/charts/hot-100/{time}"

response = requests.get(URL)
contents = response.text
soup = BeautifulSoup(contents, 'html.parser')

songs = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")
song_list = [song.getText() for song in songs]

# START SPOTIFY AUTHENTICATION
SPOTIPY_CLIENT_ID = "Your ID"
SPOTIPY_CLIENT_SECRET = "Your client secret"
REDIRECT_CITE = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_CITE,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

# SEARCH FOR A MUSIC

song_uris = []
year = time.split("-")[0]
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#CREATING A PLAYLIST

playlist = sp.user_playlist_create(user=user_id, name=f"{time} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

# NOW CHECK OUT YOUR PROFILE ^_^