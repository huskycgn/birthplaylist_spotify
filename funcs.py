import requests
import spotipy

from cred import *

auth_manager = spotipy.SpotifyOAuth(client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET,
                                    redirect_uri=URI,
                                    scope='playlist-modify-private')
sp = spotipy.Spotify(auth_manager=auth_manager)


def getsongid(artist: str, song: str):
    result = sp.search(q=f'track:{song} artist:{artist}', limit=1, type='track', market='DE')
    try:
        spotify_id = result[ 'tracks' ][ 'items' ][ 0 ][ 'id' ]
        rtuple = spotify_id, artist, song
        return rtuple
    except IndexError:
        return 'No result', artist, song


def createplaylist(plname: str) -> str:
    response = sp.user_playlist_create(name=plname, public=False, user=USER_ID)
    return response['id']


def addsong(songl: tuple, playlistid: str) -> None:
    playlist_id = playlistid
    endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

    songs = { 'uris':
                  [ f'spotify:track:{songl[ 0 ]}' ]
              }

    auth = {
        'Authorization': f'Bearer {TOKEN}',
    }

    result = requests.post(url=endpoint, headers=auth, json=songs)
    result.raise_for_status()
    print(f'Added song {songl[ 1 ]} - {songl[ 2 ]}')
