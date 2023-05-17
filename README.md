# stellar_grids

Package to aid in constructing MESA/GYRE grids of stellar models. <br>
This repository is an open-source package, GNU-licensed, and any improvements provided by the users are well accepted. See GNU License in LICENSE.

<details>
<summary> <b>Installation</b> (click to expand) </summary> <br>

Git clone this repository, and install using poetry (https://python-poetry.org/docs/) with command `poetry install` in the folder with the `pyproject.toml` file. This will install the package with all its dependencies, using the dependency versions as specified in the `poetry.lock` file. (The package will be installed in editable mode, so it will link the package to the original location, meaning any changes to the original package will be reflected directly in your environment.)

If you do not wish to use poetry, you could install by running `pip install .`. Note that this will install it as a package in your python environment, but in non-editable mode.
</details>

<details>
<summary> <b>Usage</b> (click to expand) </summary> <br>
In a python script, run the following line to make a grid with 2 different initial masses (M_ini,numbers are in solar mass), and 3 different metallicities (Z_ini, numbers are mass fraction).
<pre>
from stellar grids import grid_building_vsc as gbv

gbv.make_mesa_setup(M_ini_list=[1,2], Z_ini_list=[0.010, 0.014, 0.018])
</pre>

To make a MESA grid, check the docstring of the `make_mesa_setup` function in file `grid_building_vsc` for all the available and required parameters. The current setup is tuned to have 6 varied parameters `'Zini', 'Mini', 'logD', 'aov', 'fov'` that are put in a csv file (together with the MESA work directory and the output folder). These are read by the job scheduler and passed to the MESA run_star_extras. The run_star_extras should then read these in as command line arguments, and set the appropriate variables in the run_star_extras instead of the inlist. These scripts can of course be modified to suit your specific needs. <br>
To make a GYRE grid based on the MESA grid computed before, check `make_gyre_setup` in file `grid_building_vsc` for all the available and required parameters.

</details>


## contents

1. `stellar_grids`: Package for the grid construction
2. `LICENSE`: GNU general public license
3. `poetry.lock`: List of dependencies and their exact versions.
4. `pyproject.toml`: Installation configuration file.

### Author
Developed by Mathias Michielsen
```
mathias.michielsen[at]kuleuven.be
Instituut voor Sterrenkunde
KU Leuven, Belgium
```
