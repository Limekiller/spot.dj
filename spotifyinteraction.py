import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='PUT_THIS_IN', client_secret='PUT_THIS_IN')

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def find(songtitle, artist = ""):
    if artist == "":
        results = sp.search(q=songtitle, limit=3)
    else:
        query = songtitle + " " + artist
        results = sp.search(q=query, limit=3)

    for i, t, a in enumerate(results['tracks']['items']['items']):
        print(' ', i, t['name'])

    print(results)

find("perfect")

print("artist query\n")
find("perfect", "ed sheeran")