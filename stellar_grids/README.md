## contents

1. `templates`: A number of template files; GYRE inlists, bash scripts, VSC submit files.
2. `functions_for_mesa.py`: Helpful functions to process MESA output.
3. `grid_building_pleiades.py`: Functions for building MESA and GYRE grids on the pleiades SLURM framework (the local IvS cluster).
4. `grid_building_vsc.py`: Functions for building MESA and GYRE grids on the VSC framework.
5. `lambda.csv`: List with lambda (eigenvalue of laplace tidal equations) and nu (spin parameter) for modes up to degree 3. (TAR approximation)
6. `support_functions.py` : Support functions used by the other modules in the package.
7. `rerun_failed_GYRE`: Scripts to identify and re-run GYRE models that failed to run on the VSC. (E.g. due to "file not found" errors from HDF5 library because of high I/O on the VSC system.)

