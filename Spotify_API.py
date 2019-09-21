import spotipy
import pprint
from spotipy.oauth2 import SpotifyClientCredentials
import os


client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                      client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def search_song(search_info):
    song_info = sp.search(search_info, limit=5, type='track', market='DO')['tracks']
    preview = []
    song_list = []
    for item in song_info['items']:
        song_name = item['name']
        song_url = item['external_urls']['spotify']
        song = {'name': song_name, 'url': song_url}
        artist = list(map(lambda a: {'name': a['name'], 'url' : a['external_urls']['spotify']}, item['artists']))
        song_list.append({'song': song, 'artists': artist, })
        preview.append(item['preview_url'])
    return song_list, preview

#
# songs_found, songs = search_song(input('song name       '))
#
# for item in songs_found:
#     print(item[1] + '\n' + item[0] + '\n' + item[2] + '\n')
