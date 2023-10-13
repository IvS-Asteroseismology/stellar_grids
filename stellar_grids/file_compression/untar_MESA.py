from glob import glob
from pathlib import Path
import multiprocessing, tarfile, os


def untar_dir(directory):
    # Create a tarfile Object
    with tarfile.open(directory, 'r') as zipObj:
       # Extract all the contents of tar file in current directory
       zipObj.extractall(f'{Path(directory).parent}')

def untar_file(file):
    # Create a tarfile Object
    with tarfile.open(file, 'r:gz') as zipObj:
       # Extract all the contents of tar file in current directory and remove the tar
       zipObj.extractall(f'{Path(file).parent}')
       os.remove(file)

directories = glob(f'Zini*/*.tar')
with multiprocessing.Pool() as p:
    p.map(untar_dir, directories)

files = glob(f'Zini*/*/*.tar.gz')
with multiprocessing.Pool() as p:
    p.map(untar_file, files)
