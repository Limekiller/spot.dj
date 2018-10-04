import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='', client_secret='')

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

results = sp.search(q='weezer', limit=20)

for i, t in enumerate(results['tracks']['items']):
    print(' ', i, t['name'])