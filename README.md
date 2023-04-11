# oofemTests
A selection of OOFEM test and simulation cases, specifically related to multiscale modelling of reinforced concrete and reinforced concrete structures.

All tests can be easily run with CTest. To configure cmake, the path to OOFEM executable must be specified in the OOFEM_PATH variable. In the current directory simply run

`cmake -DOOFEM_PATH=/path/to/oofem .`

The tests can then be run from the current directory with

`ctest`

To pass all tests, OOFEM needs to be compiled with PETSc and Python support (compiler flags USE_PETSC and USE_PYTHON_EXTENSION should be set to on).

# Documentation

The sources for the cocumentation material giving a detailed overview on multiscale modelling of reinforced concrete and reinforced concrete structures in OOFEM can be found in the `doc` directory. The built pdf is available [here](https://github.com/adsci/oofemTests/blob/main/doc/multiscaleRC_OOFEM.pdf).