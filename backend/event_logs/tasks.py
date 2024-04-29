import os
import zipfile

import zstandard

from app.celery import app
from courses.models import Course
from event_logs.models import LogsArchive
from event_logs.upload_logs import insert_logs, create_logs_table
from metrics.utils.db_operations import open_db_connection

UNZIP_FOLDER = 'private'


@app.task(name="unzip_logs_archive")
def unzip_logs_archive_task(log_id: int):
    logs_archive = LogsArchive.objects.get(id=log_id)
    with zipfile.ZipFile(logs_archive.archive.path, 'r') as zip_ref:
        zip_ref.extractall(logs_archive.zst_folder_path)

    os.makedirs(logs_archive.logs_folder_path, exist_ok=True)

    files = os.listdir(logs_archive.zst_folder_path)
    for file in files:
        # just to be sure we do not decompress something wrong
        if not file.endswith('.zst'):
            continue
        decompress_zst_task.apply_async(kwargs={'log_id': log_id, 'zst_file_path': os.path.join(logs_archive.zst_folder_path, file)})


@app.task(name="decompress_zst")
def decompress_zst_task(log_id: int, zst_file_path: str):
    logs_archive = LogsArchive.objects.get(id=log_id)

    log_name = os.path.basename(zst_file_path)
    output_path = os.path.join(logs_archive.logs_folder_path, log_name).removesuffix('.zst')

    decompressor = zstandard.ZstdDecompressor()
    with open(zst_file_path, 'rb') as compressed, open(output_path, 'wb') as destination:
        decompressor.copy_stream(compressed, destination)
        upload_logs_task.apply_async(kwargs={'log_id': log_id, 'log_path': destination.name})


@app.task(name="upload_logs")
def upload_logs_task(log_id: int, log_path: str):
    print(f"upload_logs_task for {log_id} with path: {log_path}")
    connection = open_db_connection(database=os.environ.get("LOGS_DB_DATABASE"))
    create_logs_table(connection)
    insert_logs(connection, log_path)
    print(f"insert_logs finished: {log_id}")
    course_id = log_path.removesuffix('.log').split('.')[-2]
    Course.objects.get_or_create(course_id=course_id, name=course_id, short_name=course_id, image_url=f"https://picsum.photos/seed/{course_id.__hash__()}/200/200")
