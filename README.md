# oofemTests
A selection of OOFEM test and simulation cases, specifically related to multiscale modelling of reinforced concrete and reinforced concrete structures

All tests can be easily run with CTest. To configure cmake, the path to OOFEM executable must be specified in the OOFEM_PATH variable. In the current directory simply run

`cmake -DOOFEM_PATH=/path/to/oofem .`

The tests can then be run with from the current directory with

`ctest`