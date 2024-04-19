import os
import pathlib

import zstandard

COURSE_DIR = 'DATSTPRO/'
LOGS_ARCHIES_DIR = "log_archives/"
LOGS_FILES_DIR = "log_decompressed/"


def decompress_zstandard_to_folder(input_file, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    input_file = pathlib.Path(input_file)
    with open(input_file, 'rb') as compressed:
        decompressor = zstandard.ZstdDecompressor()
        with open(pathlib.Path(output_path) / input_file.stem, 'wb') as destination:
            decompressor.copy_stream(compressed, destination)


def decompress_log_archives(course_dir=COURSE_DIR):
    files = os.listdir(f"{LOGS_ARCHIES_DIR}{course_dir}")
    files = list(filter(lambda x: x.endswith('.zst'), files))
    for file in files:
        decompress_zstandard_to_folder(f"{LOGS_ARCHIES_DIR}{course_dir}{file}", f"{LOGS_FILES_DIR}{course_dir}")


if __name__ == '__main__':
    decompress_log_archives()
