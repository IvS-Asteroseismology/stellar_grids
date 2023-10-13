from glob import glob
import multiprocessing
import tarfile
import os.path

def make_tarfile(source_dir):
    output_filename = f'{source_dir}.tar.gz'
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

# Zip the preMS folder as a directory, but zip each other file individually
directories = glob('Zini*')
for directory in directories:
    files= glob(f'{directory}/gyre/*')
    with multiprocessing.Pool() as p:
        p.map(make_tarfile, files)

    files= glob(f'{directory}/profiles/*')
    with multiprocessing.Pool() as p:
        p.map(make_tarfile, files)

    files= glob(f'{directory}/preMS')
    with multiprocessing.Pool() as p:
        p.map(make_tarfile, files)

    files= glob(f'{directory}/*hist')
    with multiprocessing.Pool() as p:
        p.map(make_tarfile, files)
