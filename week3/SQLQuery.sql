--SEMANA 3--
--Carolina Raposo, 51601 e Patrícia Marcos, 51858

CREATE DATABASE Spotify_ETL;
GO

USE Spotify_ETL;
GO

--Criação de tabela provisória para inserir todos os dados
CREATE TABLE merged_left_raw (
    track_id NVARCHAR(100),
    artists NVARCHAR(255),
    album_name NVARCHAR(255),
    track_name NVARCHAR(255),
    popularity FLOAT,
    duration_ms INT,
    explicit_track NVARCHAR(10),
    danceability FLOAT,
    energy FLOAT,
    key_track INT,
    loudness FLOAT,
    mode INT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    time_signature INT,
    track_genre NVARCHAR(100)
);

--Inserção dos dados na tabela provisória
INSERT INTO merged_left_raw (
    pos, artist_name, track_uri, artist_uri, track_name_x,
    album_uri, duration_ms, album_name, playlist_id,
    track_id, popularity_norm
)
SELECT DISTINCT
    pos, artist_name, track_uri, artist_uri, track_name_x,
    album_uri, duration_ms, album_name, playlist_id,
    track_id, popularity_norm
FROM merged_left;


--Validação--
SELECT TOP 10 * FROM merged_left_raw;

--Criação das tabelas definitivas
-- Tabela de artistas
CREATE TABLE artists (
    artist_name NVARCHAR(255) PRIMARY KEY
);

CREATE TABLE albums (
    album_name NVARCHAR(255) PRIMARY KEY
);

CREATE TABLE tracks (
    track_id NVARCHAR(100) PRIMARY KEY,
    track_name NVARCHAR(255) NOT NULL,
    artist_name NVARCHAR(255),
    album_name NVARCHAR(255),
    popularity FLOAT,
    duration_ms INT,
    explicit_track BIT,
    danceability FLOAT,
    energy FLOAT,
    key_track INT,
    loudness FLOAT,
    mode INT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    time_signature INT,
    track_genre NVARCHAR(100),
    FOREIGN KEY (artist_name) REFERENCES artists(artist_name),
    FOREIGN KEY (album_name) REFERENCES albums(album_name)
);

--Inserções--
INSERT INTO artists (artist_name)
SELECT DISTINCT artists FROM merged_left_raw;

INSERT INTO albums (album_name)
SELECT DISTINCT album_name FROM merged_left_raw;

INSERT INTO tracks (
    track_id, track_name, artist_name, album_name,
    popularity, duration_ms, explicit,
    danceability, energy, key, loudness, mode,
    speechiness, acousticness, instrumentalness,
    liveness, valence, tempo, time_signature, track_genre
)
SELECT DISTINCT
    track_id, track_name_x, artists, album_name,
    popularity, duration_ms, explicit,
    danceability, energy, key, loudness, mode,
    speechiness, acousticness, instrumentalness,
    liveness, valence, tempo, time_signature, track_genre
FROM merged_left_raw;

--Validação--
SELECT COUNT(*) FROM artists;
SELECT COUNT(*) FROM albums;
SELECT COUNT(*) FROM tracks;

-- Verificação de chaves estrangeiras inválidas
SELECT * FROM tracks
WHERE artist_name NOT IN (SELECT artist_name FROM artists);

SELECT * FROM tracks
WHERE album_name NOT IN (SELECT album_name FROM albums);

-- Verificação de nulos
SELECT * FROM tracks WHERE track_name IS NULL;
SELECT * FROM tracks WHERE popularity IS NULL;

-- (Opcional) Eliminar a tabela temporária
DROP TABLE merged_left_raw;