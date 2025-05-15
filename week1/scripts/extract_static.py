#o de cima pelo pycharm
import json
import pandas as pd

# Carregar o JSON único
with open('C:\Lic.IACD\Python\ETD\projeto\spotify_million_playlist_dataset\data\mpd.slice.0-999.json', 'r') as f:
    data = json.load(f)

# Extrair todas as faixas das playlists
all_tracks = []
for playlist in data['playlists']:
    for track in playlist['tracks']:
        track['playlist_id'] = playlist['pid']  # Adiciona ID da playlist
        all_tracks.append(track)

# Criar DataFrame e remover duplicatas
df_tracks = pd.DataFrame(all_tracks)
df_tracks = df_tracks.drop_duplicates(subset=['track_uri'])
df_tracks.to_csv('static_tracks.csv', index=False)
print(df_tracks.head())