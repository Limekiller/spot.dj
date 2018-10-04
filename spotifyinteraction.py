import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='b84f728dd90c4bb793db397de6b2bd1c', client_secret='0677563337c74f0bbb7794f44b52797b')

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

results = sp.search(q='weezer', limit=20)

for i, t in enumerate(results['tracks']['items']):
    print(' ', i, t['name'])