import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import time

client_credentials_manager = SpotifyClientCredentials(client_id="20d27f203a1a494ba8bb5877bf26d9ab", client_secret="2f211a9c9ef2495aae69364d7a9113c4")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_uri = "https://open.spotify.com/playlist/2o3CjvCCYUPa1CYUTfKa0f?si=588351e3ff7d4941"

def get_playlist_tracks(playlist_uri):
    results = sp.playlist_tracks(playlist_uri)
    tracks = []

    for item in results['items']:
        track = item['track']
        tracks.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],  
            'artist_id': track['artists'][0]['id'],
            'album': track['album']['name'],
            'track_id': track['id'],
            'duration_ms': track['duration_ms'], 
        })

    return tracks

def get_artist_genre(artist_ids):
    genres = {}
    for artist_id in artist_ids:
        try:
            artist_info = sp.artist(artist_id)
            genres[artist_id] = artist_info.get('genres', [])
        except Exception as e:
            print(f"Error fetching genre for artist {artist_id}: {e}")
            genres[artist_id] = []
    return genres

def get_audio_features(track_ids):
    features = []
    for i in range(0, len(track_ids), 100):
        features += sp.audio_features(track_ids[i:i + 100])
        time.sleep(0.2)  # Add delay to avoid rate-limiting
    return features

tracks = get_playlist_tracks(playlist_uri)

artist_ids = list({track['artist_id'] for track in tracks})

artist_genres = get_artist_genre(artist_ids)

track_ids = [track['track_id'] for track in tracks]
audio_features = get_audio_features(track_ids)

csv_data = []

csv_headers = [
    'Track Name', 'Artist', 'Album', 'Genres', 
    'Duration (seconds)', 'Danceability', 'Energy', 'Tempo'
]

csv_data.append(csv_headers)

for i, track in enumerate(tracks):
    artist_id = track['artist_id']
    genres = artist_genres.get(artist_id, [])
    features = audio_features[i]

    danceability = features.get('danceability', 'N/A')
    energy = features.get('energy', 'N/A')
    tempo = features.get('tempo', 'N/A')

    track_data = [
        track['name'],  # Track Name
        track['artist'],  # Artist
        track['album'],  # Album
        ', '.join(genres),  # Genres
        track['duration_ms'] // 1000,  # Duration in seconds
        danceability,  # Danceability
        energy,  # Energy
        tempo  # Tempo
    ]

    csv_data.append(track_data)

with open('spotify_playlist_data10.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

print("Data has been written to spotify_playlist_data10.csv")

