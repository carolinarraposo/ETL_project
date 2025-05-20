from prefect import flow, task
from extract_static import extract_static_tracks
from extract_api import extract_tracks_from_artists
from enrich_data import enrich_static_tracks_with_popularity

@task
def run_extract_static():
    extract_static_tracks(
        json_path="C:\\Users\\patri\\Desktop\\ubi\\bsc_iacd\\2024_2025\\2_semestre\\extracao_dados\\projeto\\spotify_million_playlist_dataset\\data\\mpd.slice.0-999.json",
        output_csv="static_tracks.csv"
    )

@task
def run_extract_api():
    extract_tracks_from_artists(
        output_csv="artists_tracks.csv"
    )

@task
def run_enrich_data():
    enrich_static_tracks_with_popularity(
        input_csv="static_tracks.csv",
        output_csv="enriched_tracks.csv"
    )

@flow
def spotify_etl_flow():
    run_extract_static()
    run_extract_api()
    run_enrich_data()

if __name__ == "__main__":
    spotify_etl_flow()
