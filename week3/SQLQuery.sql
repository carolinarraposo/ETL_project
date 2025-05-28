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
    track_name VARCHAR(255) NOT NULL,     -- de track_name_x
    track_name_y VARCHAR(255),            -- possível variação (API)
    track_uri VARCHAR(100) UNIQUE NOT NULL,
    album_uri VARCHAR(100),
    artist_uri VARCHAR(100),
    duration_ms INT,
    popularity FLOAT,
    popularity_norm FLOAT,
    artist_api VARCHAR(255),              -- de coluna "artist" (API)
    album_api VARCHAR(255),               -- de coluna "album" (API)
    all_artists VARCHAR(MAX),             -- lista de artistas ou JSON
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

