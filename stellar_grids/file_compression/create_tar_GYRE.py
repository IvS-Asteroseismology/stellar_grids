from glob import glob
import multiprocessing, tarfile
import os.path
from sys import argv
from pathlib import Path

def make_tarfile(source_dir):
    _, output_filename = source_dir.split(TOP_DIR)
    with tarfile.open(f'{TOP_DIR}_tar{output_filename}.tar.gz', "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

# compress each file individually
path = argv[1]
directories = glob(f'{path}/Zini*')
for directory in directories:
    Path(f'{directory}_tar/').mkdir(parents=True, exist_ok=True)
    TOP_DIR = f'{directory}'

    files= glob(f'{directory}/*')
    with multiprocessing.Pool() as p:
        p.map(make_tarfile, files)
