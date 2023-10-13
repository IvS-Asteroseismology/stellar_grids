from glob import glob
import multiprocessing, tarfile
import os.path
from sys import argv
from pathlib import Path

def make_tarfile(source_dir):
    _, output_filename = source_dir.split(TOP_DIR)
    with tarfile.open(f'{TOP_DIR}_tar{output_filename}.tar.gz', "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

# Tar the preMS folder as a directory, but compress each other file individually
path = argv[1]
directories = glob(f'{path}/Zini*')
for directory in directories:
    Path(f'{directory}_tar/gyre').mkdir(parents=True, exist_ok=True)
    Path(f'{directory}_tar/profiles').mkdir(parents=True, exist_ok=True)
    Path(f'{directory}_tar/history').mkdir(parents=True, exist_ok=True)
    TOP_DIR = f'{directory}'
    files= glob(f'{directory}/gyre/*')
    with multiprocessing.Pool() as p:
        p.map(make_tarfile, files)

    files= glob(f'{directory}/profiles/*')
    with multiprocessing.Pool() as p:
        p.map(make_tarfile, files)

    files= glob(f'{directory}/preMS')
    with multiprocessing.Pool() as p:
        p.map(make_tarfile, files)

    files= glob(f'{directory}/history/*')
    with multiprocessing.Pool() as p:
        p.map(make_tarfile, files)
