--SEMANA 3--
--Carolina Raposo, 51601 e Patrícia Marcos, 51858

CREATE DATABASE Spotify_ETL;
GO

USE Spotify_ETL;
GO

--Criação de tabela provisória para inserir todos os dados
CREATE TABLE merged_left_raw (
    track_id NVARCHAR(100),
    artists NVARCHAR(MAX),
    album_name NVARCHAR(MAX),
    track_name NVARCHAR(MAX),
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
    track_genre NVARCHAR(MAX)
);

--Inserção dos dados na tabela provisória
INSERT INTO merged_left_raw (
    track_id, artists, album_name, track_name, popularity, duration_ms, explicit_track, danceability, energy, key_track, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature, track_genre
)
SELECT DISTINCT
    track_id, artists, album_name, track_name_x, popularity, duration_ms, explicit_track, danceability, energy, key_track, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature, track_genre
FROM merged_left2;


--Validação--
SELECT TOP 10 * FROM merged_left_raw;

drop table albums

--Criação das tabelas definitivas

CREATE TABLE tracks (
    track_id NVARCHAR(100) PRIMARY KEY,
    track_name NVARCHAR(MAX) NOT NULL,
    artist_name NVARCHAR(MAX),
    album_name NVARCHAR(MAX),
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
    track_genre NVARCHAR(MAX),
);

--Inserções--
INSERT INTO tracks (
    track_id, track_name, artist_name, album_name,
    popularity, duration_ms, explicit_track,
    danceability, energy, key_track, loudness, mode,
    speechiness, acousticness, instrumentalness,
    liveness, valence, tempo, time_signature, track_genre
)
SELECT DISTINCT
    track_id, track_name, artists, album_name,
    popularity, duration_ms, explicit_track,
    danceability, energy, key_track, loudness, mode,
    speechiness, acousticness, instrumentalness,
    liveness, valence, tempo, time_signature, track_genre
FROM merged_left_raw;

--Validação--
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