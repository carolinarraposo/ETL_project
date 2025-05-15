import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Autenticação com a API do Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="9dac97c219714e8c8281b17c3c433a42",
    client_secret="772c602a877942d786dc8be02c246153",
    redirect_uri="https://example.com/callback",
    scope="user-library-read user-top-read",
    cache_path=".spotify_cache"
))

# Lista de nomes dos artistas
artist_names = ["One Direction", "Taylor Swift", "Billie Eilish", "Ariana Grande","Sabrina Carpenter","Tate Mcrae"]

all_tracks = []

for input_artist_name in artist_names:
    # encontrar o artista por nome
    result = sp.search(q=f"artist:{input_artist_name}", type='artist', limit=1)

    if not result['artists']['items']:
        print(f"Artista '{input_artist_name}' não encontrado.")
        continue

    artist = result['artists']['items'][0]
    artist_id = artist['id']
    artist_name = artist['name']

    # verificação: o nome encontrado é semelhante ao buscado?
    if input_artist_name.lower() not in artist_name.lower():
        print(f"Atenção: encontrado '{artist_name}' para busca '{input_artist_name}' — ignorando para evitar erro.")
        continue

    print(f"Artista confirmado: {artist_name} (ID: {artist_id})")

    # obter álbuns
    albums = sp.artist_albums(artist_id, album_type='album', limit=50)
    album_items = albums['items']

    for album in album_items:
        album_name = album['name']
        album_id = album['id']
        print(f"Processando álbum: {album_name}")

        tracks = sp.album_tracks(album_id)['items']
        for track in tracks:
            if not track or not track['id']:
                continue

            track_artists = [a['name'] for a in track['artists']]
            main_artist = track_artists[0] if track_artists else artist_name

            all_tracks.append({
                'artist': artist_name,
                'track_main_artist': main_artist,
                'album': album_name,
                'track_id': track['id'],
                'track_name': track['name'],
                'all_artists': ', '.join(track_artists)
            })

# guardar em CSV
df = pd.DataFrame(all_tracks)

# (opcional) se quiser apenas 1 coluna de artista final:
df = df.drop(columns=['track_main_artist'])

df.to_csv("artists_tracks.csv", index=False, encoding='utf-8-sig')
print("\nFicheiro 'artists_tracks.csv' guardado com sucesso!")