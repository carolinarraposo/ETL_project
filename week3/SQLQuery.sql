--Semana 3--
--Carolina Raposo, 51601 e Patrícia Marcos, 51858

CREATE DATABASE Spotify_ETL;
GO

USE Spotify_ETL;
GO

CREATE TABLE artists (
    artist_uri VARCHAR(100) PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL
);

CREATE TABLE albums (
    album_uri VARCHAR(100) PRIMARY KEY,
    album_name VARCHAR(255) NOT NULL
);

CREATE TABLE playlists (
    playlist_id INT PRIMARY KEY
    -- Podes adicionar nome da playlist no futuro, se necessário
);

CREATE TABLE tracks (
    track_id VARCHAR(100) PRIMARY KEY,
    track_name VARCHAR(255) NOT NULL,         -- de track_name_x
    track_uri VARCHAR(100) UNIQUE NOT NULL,
    album_uri VARCHAR(100),
    artist_uri VARCHAR(100),
    duration_ms INT,
    popularity_norm FLOAT,
    FOREIGN KEY (album_uri) REFERENCES albums(album_uri),
    FOREIGN KEY (artist_uri) REFERENCES artists(artist_uri)
);


CREATE TABLE playlist_tracks (
    playlist_id INT,
    track_id VARCHAR(100),
    pos INT,
    PRIMARY KEY (playlist_id, track_id, pos),
    FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id),
    FOREIGN KEY (track_id) REFERENCES tracks(track_id)
);

--inserções--
INSERT INTO artists (artist_uri, artist_name)
SELECT DISTINCT artist_uri, artist_name
FROM merged_staging;

INSERT INTO albums (album_uri, album_name)
SELECT DISTINCT album_uri, album_name
FROM merged_staging;

INSERT INTO playlists (playlist_id)
SELECT DISTINCT playlist_id
FROM merged_staging;

INSERT INTO tracks (
    track_id, track_name, track_uri,
    album_uri, artist_uri, duration_ms,
    popularity_norm
)
SELECT DISTINCT
    track_id, track_name_x, track_uri,
    album_uri, artist_uri, duration_ms,
    popularity_norm
FROM merged_staging;

INSERT INTO playlist_tracks (playlist_id, track_id, pos)
SELECT DISTINCT playlist_id, track_id, pos
FROM merged_staging;

--validação--
SELECT COUNT(*) FROM artists;
SELECT COUNT(*) FROM tracks;
SELECT * FROM tracks WHERE popularity_norm IS NULL;
