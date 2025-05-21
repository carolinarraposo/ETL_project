from prefect import flow, task
from extract_static import extract_static_tracks
from extract_api import extract_tracks_from_artists
from enrich_data import enrich_static_tracks_with_popularity
import boto3

@task
def run_extract_static():
    extract_static_tracks(
        json_path="mpd.slice.0-999.json",
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

@task
def upload_to_s3(file_path, bucket_name, s3_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id='AKIA5LNU5WIDALR2RVNV',            # <- substitui
        aws_secret_access_key='...',        # <- substitui
        region_name='eu-north-1'                        # <- ajusta conforme tua região
    )
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"✅ Upload realizado: {file_path} → s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"❌ Falha ao fazer upload: {e}")

@flow
def spotify_etl_flow():
    run_extract_static()
    run_extract_api()
    run_enrich_data()
    upload_to_s3(
        file_path="enriched_tracks.csv",
        bucket_name="etl1",  # <- substitui
        s3_key="dados/enriched_tracks.csv"  # <- caminho dentro do bucket
    )


if __name__ == "__main__":
    spotify_etl_flow()

