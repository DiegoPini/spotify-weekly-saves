import json
from dotenv import load_dotenv
import os
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_id = os.getenv("USER_ID")
weekly_discover = os.getenv("WEEKLY_DISCOVER")
SCOPE = 'user-library-read playlist-modify-public playlist-modify-private'
URI = os.getenv("URI")

token = SpotifyOAuth(client_id= client_id, client_secret= client_secret, redirect_uri = URI,scope= SCOPE, username= user_id)

spotifyObject = spotipy.Spotify(auth_manager = token) 

def get_tracks_uri(playlist_uri):
    songs_uri = []
    json_result = spotifyObject.playlist(playlist_id='https://open.spotify.com/playlist/' + playlist_uri)
    json_lenght = json_result['tracks']['total']
    for i in range(json_lenght):
        songs_uri.append(json_result['tracks']['items'][i]['track']['uri'])
    return songs_uri

def add_songs():
    user_playlists = []
    json_result = spotifyObject.user_playlists(user= user_id)
    json_lenght = json_result['total']
    for i in range(json_lenght):
       user_playlists.append(json_result['items'][i]['name'])  
    
    if 'Weekly Saves' not in user_playlists:
        spotifyObject.user_playlist_create(user= user_id, name = 'Weekly Saves', public = True, description= 'Weekly Discover Saves' )
    else:
        numPlaylist = user_playlists.index('Weekly Saves')
        playlist_id = json_result['items'][numPlaylist]['id']
       

    tracks_uri = get_tracks_uri(playlist_uri=weekly_discover)
    spotifyObject.user_playlist_add_tracks(user = user_id, playlist_id=playlist_id, tracks= tracks_uri)
    remove_duplicates(playlist_id)

def remove_duplicates(playlist_id):

    tracks_uri = get_tracks_uri(playlist_uri=weekly_discover)
    playlist_tracks = get_tracks_uri(playlist_uri = playlist_id)
    

    remove_songs = []
    for i in range(len(tracks_uri)):
        x = 0
        for c in range(len(playlist_tracks)):
            if(tracks_uri[i] == playlist_tracks[c]):
                x = x +1
                if(x > 1):
                    remove_songs.append({'uri' : tracks_uri[i], 'positions' : [c]})
                    
    spotifyObject.playlist_remove_specific_occurrences_of_items(playlist_id= playlist_id, items= remove_songs)


add_songs()