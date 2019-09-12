import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os


client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                      client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def search_song(search_info):
    song_info = sp.search(search_info, limit=7)['tracks']
    song = {}
    song_list = []
    for item in song_info['items']:
        if item['type'] == 'track':
            song.update({item['name']: item['external_urls']['spotify']})
            song_list.append([item['artists'][0]['name'], item['name'], item['external_urls']['spotify']])
    return song_list, song

#
# songs_found, songs = search_song(input('song name       '))
#
# for item in songs_found:
#     print(item[1] + '\n' + item[0] + '\n' + item[2] + '\n')
