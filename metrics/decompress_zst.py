import os
import pathlib

import zstandard

LOGS_DIR = '../log_files/DATANTECH2035/'
LOGS_ARCHIES_DIR = "log_archives/"
LOGS_FILES_DIR = "log_decompressed/"


def decompress_zstandard_to_folder(input_file, output_path):
    input_file = pathlib.Path(input_file)
    with open(input_file, 'rb') as compressed:
        decompressor = zstandard.ZstdDecompressor()
        with open(pathlib.Path(output_path) / input_file.stem, 'wb') as destination:
            decompressor.copy_stream(compressed, destination)


def decompress_log_archives(log_dir=LOGS_DIR):
    files = os.listdir(f"{log_dir}{LOGS_ARCHIES_DIR}")
    files = list(filter(lambda x: x.endswith('.zst'), files))
    for file in files:
        decompress_zstandard_to_folder(f"{log_dir}{LOGS_ARCHIES_DIR}{file}", f"{log_dir}{LOGS_FILES_DIR}")


if __name__ == '__main__':
    decompress_log_archives()
