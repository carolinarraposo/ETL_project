import pandas as pd

def extract_static_tracks(csv_path, output_csv):
    df = pd.read_csv(csv_path)

    # Remover duplicados com base no track_id
    df_unique = df.drop_duplicates(subset=["track_id"])

    df_unique.to_csv(output_csv, index=False)
    print(f"Extração concluída: {output_csv}")