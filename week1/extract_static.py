import json
import pandas as pd

def extract_static_tracks(json_path, output_csv):
    with open(json_path, 'r') as f:
        data = json.load(f)

    all_tracks = []
    for playlist in data['playlists']:
        for track in playlist['tracks']:
            track['playlist_id'] = playlist['pid']
            all_tracks.append(track)

    df_tracks = pd.DataFrame(all_tracks).drop_duplicates(subset=['track_uri'])
    df_tracks.to_csv(output_csv, index=False)
    print(f"Extração concluída: {output_csv}")