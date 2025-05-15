import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time

#Configuração da autenticação
client_id = "9dac97c219714e8c8281b17c3c433a42"
client_secret = "772c602a877942d786dc8be02c246153"
redirect_uri = "https://example.com/callback"

# Para leitura pública de faixas, escopo pode ser None
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=None
)

#Etapa de autenticação
auth_url = sp_oauth.get_authorize_url()
print("Vá para este link, faça login e cole aqui a URL de redirecionamento após login:\n", auth_url)
redirect_response = input("Cole aqui a URL de redirecionamento: ")
code = sp_oauth.parse_response_code(redirect_response)

# Obter token de acesso
token_info = sp_oauth.get_access_token(code)
access_token = token_info['access_token']
sp = spotipy.Spotify(auth=access_token)

#Leitura do CSV com faixas
df_tracks = pd.read_csv('static_tracks.csv')
track_ids = df_tracks['track_uri'].str.replace('spotify:track:', '', regex=False).dropna().unique().tolist()

#Buscar popularidade em batches
track_infos = []
for i in range(0, len(track_ids), 50):
    batch = track_ids[i:i+50]
    try:
        response = sp.tracks(batch)
        tracks = response.get('tracks', [])
        print(f"Batch {i}-{i+len(batch)}: {len(tracks)} faixas retornadas")
        track_infos.extend(tracks)
    except Exception as e:
        print(f"Erro na batch {i}-{i+50}: {e}")
        time.sleep(2)

#Filtrar faixas válidas
valid_tracks = [t for t in track_infos if t and 'id' in t and 'popularity' in t]

if valid_tracks:
    # Criar DataFrame com ID e Popularidade
    df_infos = pd.DataFrame(valid_tracks)[['id', 'popularity']].rename(columns={'id': 'track_id'})

    # Adicionar coluna de track_id no DataFrame original
    df_final = df_tracks.copy()
    df_final['track_id'] = df_final['track_uri'].str.replace('spotify:track:', '', regex=False)

    # Mesclar popularidade com dados originais
    df_final = df_final.merge(df_infos, on='track_id', how='left')

    # Salvar CSV final
    df_final.to_csv('enriched_tracks.csv', index=False, encoding='utf-8-sig')
    print("Dados enriquecidos salvos como enriched_tracks.csv")
else:
    print("Nenhuma faixa válida foi retornada pela API.")