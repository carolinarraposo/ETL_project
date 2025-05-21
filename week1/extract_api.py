import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def extract_tracks_from_artists(output_csv):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="d78fbc07ff5140418beed2ece6e796b6",
        client_secret="359f983ca0f6470c9f63e8477df82101",
        redirect_uri="https://example.com/callback",
        scope="user-library-read user-top-read",
        cache_path=".spotify_cache"
    ))

    artist_names = ["One Direction", "Taylor Swift", "Billie Eilish", "Ariana Grande", "Sabrina Carpenter", "Tate Mcrae"]
    all_tracks = []

    for input_artist_name in artist_names:
        result = sp.search(q=f"artist:{input_artist_name}", type='artist', limit=1)
        if not result['artists']['items']:
            print(f"Artista '{input_artist_name}' não encontrado.")
            continue

        artist = result['artists']['items'][0]
        artist_id = artist['id']
        artist_name = artist['name']

        if input_artist_name.lower() not in artist_name.lower():
            print(f"Atenção: encontrado '{artist_name}' para busca '{input_artist_name}' — ignorando.")
            continue

        albums = sp.artist_albums(artist_id, album_type='album', limit=50)['items']
        for album in albums:
            tracks = sp.album_tracks(album['id'])['items']
            for track in tracks:
                if not track or not track['id']:
                    continue

                track_artists = [a['name'] for a in track['artists']]
                main_artist = track_artists[0] if track_artists else artist_name

                all_tracks.append({
                    'artist': artist_name,
                    'track_main_artist': main_artist,
                    'album': album['name'],
                    'track_id': track['id'],
                    'track_name': track['name'],
                    'all_artists': ', '.join(track_artists)
                })

    df = pd.DataFrame(all_tracks).drop(columns=['track_main_artist'])
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"Extração de artistas concluída: {output_csv}")
