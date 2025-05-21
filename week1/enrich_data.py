from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

def enrich_static_tracks_with_popularity(input_csv, output_csv):
    sp = Spotify(auth_manager=SpotifyClientCredentials(
        client_id="6f2b607c7c0b412d882cbbbfe2f5f3fe",
        client_secret="dc97bf38c3674c4497a33291ca31cd0f"
    ))

    df_tracks = pd.read_csv(input_csv)
    track_ids = df_tracks['track_uri'].str.replace('spotify:track:', '', regex=False).dropna().unique().tolist()

    track_infos = []

    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50]
        try:
            response = sp.tracks(batch)
            track_infos.extend(response.get('tracks', []))
        except Exception as e:
            print(f"Erro na batch {i}-{i+50}: {e}")
            time.sleep(2)

    valid_tracks = [t for t in track_infos if t and 'id' in t and 'popularity' in t]
    if not valid_tracks:
        print("Nenhuma faixa válida encontrada.")
        return

    df_infos = pd.DataFrame(valid_tracks)[['id', 'popularity']].rename(columns={'id': 'track_id'})

    df_tracks['track_id'] = df_tracks['track_uri'].str.replace('spotify:track:', '', regex=False)
    df_final = df_tracks.merge(df_infos, on='track_id', how='left')

    df_final.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"Dados enriquecidos salvos: {output_csv}")