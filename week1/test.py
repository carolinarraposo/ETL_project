import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time

def enrich_static_tracks_with_audio_features(input_csv, output_csv):
    sp_oauth = SpotifyOAuth(
        client_id="d78fbc07ff5140418beed2ece6e796b6",
        client_secret="359f983ca0f6470c9f63e8477df82101",
        redirect_uri="https://example.com/callback",
        scope="user-library-read user-top-read"
    )

    print("Vá para este link e cole a URL de redirecionamento:\n", sp_oauth.get_authorize_url())
    redirect_response = input("Cole aqui a URL de redirecionamento: ")
    code = sp_oauth.parse_response_code(redirect_response)
    token_info = sp_oauth.get_access_token(code)
    sp = spotipy.Spotify(auth=token_info['access_token'])

    df_tracks = pd.read_csv(input_csv)
    track_ids = df_tracks['track_uri'].str.replace('spotify:track:', '', regex=False).dropna().unique().tolist()

    metadata_infos = []
    audio_infos = []

    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50]
        try:
            meta_response = sp.tracks(batch)
            audio_response = sp.audio_features(batch)

            metadata_infos.extend(meta_response.get('tracks', []))
            audio_infos.extend(audio_response)
        except Exception as e:
            print(f"Erro na batch {i}-{i+50}: {e}")
            time.sleep(2)

    meta_df = pd.DataFrame(metadata_infos)
    audio_df = pd.DataFrame(audio_infos)

    if meta_df.empty or audio_df.empty:
        print("Nenhuma faixa válida encontrada.")
        return

    meta_df = meta_df[['id', 'popularity']].rename(columns={'id': 'track_id'})
    audio_df = audio_df[['id', 'danceability', 'energy', 'valence', 'tempo']].rename(columns={'id': 'track_id'})

    df_tracks['track_id'] = df_tracks['track_uri'].str.replace('spotify:track:', '', regex=False)
    df_final = df_tracks.merge(meta_df, on='track_id', how='left')
    df_final = df_final.merge(audio_df, on='track_id', how='left')

    df_final.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"Dados enriquecidos salvos: {output_csv}")