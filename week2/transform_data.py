import pandas as pd

# Carregar os dados
df = pd.read_csv("enriched_tracks.csv")
df2 = pd.read_csv("artists_tracks.csv")

# Mostrar forma e colunas iniciais
print("Shape original do enriched tracks:", df.shape)
print("Colunas:", df.columns)

missing_values = df.isnull().sum()
print("Valores ausentes por coluna no enrich tracks:")
print(missing_values)

print("Shape original do artist tracks:", df2.shape)
print("Colunas do artist tracks:", df2.columns)

missing_values = df2.isnull().sum()
print("Valores ausentes por coluna do artist tracks:")
print(missing_values)

df = df.dropna()

# Verificar novamente valores ausentes depois de remover
missing_after_drop = df.isnull().sum()
print("Valores ausentes após drop no enriched tracks:")
print(missing_after_drop)

duplicate_rows = df.duplicated().sum()
print("\nLinhas duplicadas de enriched traks:", duplicate_rows)

duplicate_rows = df2.duplicated().sum()
print("\nLinhas duplicadas artists tracks:", duplicate_rows)

# Normalizar a coluna 'popularity' para o intervalo [0, 1]
df["popularity"] = df["popularity"] / 100
print("\nColuna popularity normalizada:")
print(df["popularity"].head())

df.to_csv("enriched_tracks_cleaned.csv", index=False)
df2.to_csv("artists_tracks_cleaned.csv", index=False)

# Carregar os ficheiros CSV
enriched_df = pd.read_csv("enriched_tracks_cleaned.csv")
artists_df = pd.read_csv("artists_tracks_cleaned.csv")

# LEFT JOIN
merged_left = pd.merge(enriched_df, artists_df, on="track_id", how="left")
print("LEFT JOIN - shape:", merged_left.shape)

missing_values = merged_left.isnull().sum()
print("Valores ausentes por coluna final:")
print(missing_values)

print("Shape csv final:", merged_left.shape)
print("Colunas:", merged_left.columns)

merged_left = merged_left.drop(['artist', 'album', 'track_name_y', 'all_artists'], axis=1)

missing_values = merged_left.isnull().sum()
print(missing_values)

print("Shape csv final (com colunas eliminadas):", merged_left.shape)
print("Colunas:", merged_left.columns)
merged_left.to_csv("merged_left.csv", index=False)
