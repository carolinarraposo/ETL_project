--Semana 3--
--Carolina Raposo, 51601 e Patrícia Marcos, 51858

CREATE DATABASE Spotify_ETL;
GO

USE Spotify_ETL;
GO

--criação de tabela provisória para inserir todos os dados
CREATE TABLE merged_left_raw (
    pos INT,
    artist_name NVARCHAR(255),
    track_uri NVARCHAR(200),
    artist_uri NVARCHAR(200),
    track_name_x NVARCHAR(255),
    album_uri NVARCHAR(200),
    duration_ms INT,
    album_name NVARCHAR(255),
    playlist_id INT,
    track_id NVARCHAR(100),
    popularity_norm FLOAT
);

--inserção dos dados na tabela provisória
INSERT INTO merged_left_raw (pos, artist_name,track_uri, artist_uri,track_name_x, album_uri, duration_ms, album_name,playlist_id, track_id,popularity_norm)
SELECT DISTINCT pos, artist_name,track_uri, artist_uri,track_name_x, album_uri, duration_ms, album_name,playlist_id, track_id,popularity_norm
FROM merged_left

--validação--
SELECT TOP 10 * FROM merged_left_raw;

--criação das tabelas definitivas
CREATE TABLE artists (
    artist_uri NVARCHAR(200) PRIMARY KEY,
    artist_name NVARCHAR(255) NOT NULL
);

CREATE TABLE albums (
    album_uri NVARCHAR(200) PRIMARY KEY,
    album_name NVARCHAR(255) NOT NULL
);


CREATE TABLE playlists (
    playlist_id INT PRIMARY KEY
);


CREATE TABLE tracks (
    track_id NVARCHAR(100) PRIMARY KEY,
    track_name NVARCHAR(255) NOT NULL,
    track_uri NVARCHAR(200) UNIQUE NOT NULL,
    album_uri NVARCHAR(200),
    artist_uri NVARCHAR(200),
    duration_ms INT,
    popularity_norm FLOAT,
    FOREIGN KEY (album_uri) REFERENCES albums(album_uri),
    FOREIGN KEY (artist_uri) REFERENCES artists(artist_uri)
);


CREATE TABLE playlist_tracks (
    playlist_id INT,
    track_id NVARCHAR(100),
    pos INT,
    PRIMARY KEY (playlist_id, track_id, pos),
    FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id),
    FOREIGN KEY (track_id) REFERENCES tracks(track_id)
);

--inserções--
INSERT INTO artists (artist_uri, artist_name)
SELECT DISTINCT artist_uri, artist_name
FROM merged_left_raw;

INSERT INTO albums (album_uri, album_name)
SELECT DISTINCT album_uri, album_name
FROM merged_left_raw;

INSERT INTO playlists (playlist_id)
SELECT DISTINCT playlist_id
FROM merged_left_raw;

INSERT INTO tracks (
    track_id, track_name, track_uri,
    album_uri, artist_uri, duration_ms, popularity_norm
)
SELECT DISTINCT
    track_id, track_name_x, track_uri,
    album_uri, artist_uri, duration_ms, popularity_norm
FROM merged_left_raw;

INSERT INTO playlist_tracks (playlist_id, track_id, pos)
SELECT DISTINCT playlist_id, track_id, pos
FROM merged_left_raw;

--validação--
SELECT COUNT(*) FROM artists;
SELECT COUNT(*) FROM albums;
SELECT COUNT(*) FROM tracks;
SELECT COUNT(*) FROM playlists;
SELECT COUNT(*) FROM playlist_tracks;


--eliminação da tabela provisória
DROP TABLE merged_left_raw;