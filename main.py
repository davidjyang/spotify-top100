from bs4 import BeautifulSoup 
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which day do you want to travel to? Please enter the date in the format YYYY-MM-DD: ")
year = date.split("-")[0]

response = requests.get("http://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select(selector="li h3", class_="c-title")
song_names = [song.getText().strip() for song in song_names_spans[:100]]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8000",
        client_id="a4713afc21d14d848c03254e8cf8ae26", 
        client_secret="945e78a2afad4727848992daa8d5a27e",
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

song_uris = []

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)