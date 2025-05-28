import pandas as pd

# Carregar os dados
df = pd.read_csv("enriched_tracks.csv")
df2 = pd.read_csv("artists_tracks.csv")

# Mostrar forma e colunas iniciais
print("Shape original:", df.shape)
print("Colunas:", df.columns)

missing_values = df.isnull().sum()
print("Valores ausentes por coluna:")
print(missing_values)


print("Shape original:", df2.shape)
print("Colunas:", df2.columns)

missing_values = df2.isnull().sum()
print("Valores ausentes por coluna:")
print(missing_values)


print(df[df["popularity"].isnull()])
print(df[df.isnull().any(axis=1)].index.tolist())
df = df.dropna()

# Verificar novamente valores ausentes depois de remover
missing_after_drop = df.isnull().sum()
print("Valores ausentes após drop:")
print(missing_after_drop)

duplicate_rows = df.duplicated(subset=["track_id", "playlist_id"]).sum()
print("\nLinhas duplicadas:", duplicate_rows)

duplicate_rows = df2.duplicated().sum()
print("\nLinhas duplicadas:", duplicate_rows)

# Normalizar a coluna 'popularity' para o intervalo [0, 1]
df["popularity_norm"] = df["popularity"] / 100
print(df[["popularity", "popularity_norm"]].head())

df.to_csv("enriched_tracks_cleaned.csv", index=False)

# Carregar os ficheiros CSV
enriched_df = pd.read_csv("enriched_tracks_cleaned.csv")
artists_df = pd.read_csv("artists_tracks.csv")

# LEFT JOIN
merged_left = pd.merge(enriched_df, artists_df, on="track_id", how="left")
print("LEFT JOIN - shape:", merged_left.shape)

# salvar os resultados em CSVs para inspecionar depois
merged_left.to_csv("merged_left.csv", index=False)

missing_values = merged_left.isnull().sum()
print("Valores ausentes por coluna final:")
print(missing_values)

print("Shape csv final:", merged_left.shape)
print("Colunas:", merged_left.columns)

merged_left = merged_left.drop(['popularity', 'artist', 'album', 'track_name_y', 'all_artists'], axis=1)
print("Shape csv final:", merged_left.shape)
print("Colunas:", merged_left.columns)