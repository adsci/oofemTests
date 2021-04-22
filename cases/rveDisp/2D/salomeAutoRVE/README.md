## Automatic OOFEM input file generation for 2D reinforced concrete Representative Volume Elements 

Scripts in this directory can be used for automatic generation of OOFEM input files of 2D reinforced concrete RVEs, which comprise rectangular plane stress elements for concrete, truss elements for reinforcement and interface elements in between.
Geometry (rve size, number of elements per side and spacing of reinforcement in x and y directions) should be specified first.
Additional data (material parameters, cross section geometry etc.) can be modified either in the scripts or after the input file is generated.
By default Concrete3, MisesMat and bondceb material models are used for the concrete, steel and interface, respectively.

Tested on 22 Apr 2012, SALOME 9.6.0 on Windows 10

1. Enter RVE geometry on lines 7-10 in `salomeRVEmesh.py`
2. Run the script in SALOME. Open SALOME, click File->Load Script and select the script `salomeRVEmesh.py`. SALOME will save a `rvemesh.unv` file in it's default directory (e.g. C:\SALOME-9.6.0). Copy that file to your working directory.
3. Create control file. Enter the RVE geometry (and optionally, material parameters) into `makeCTRLfile.py`. In the working directory, run the script `makeCTRLfile.py`:

    `python3 makeCTRLfile.py`

    This will create a rvedd.ctrl file in the working directory.
4. Use `unv2oofem` tool to convert the UNV and CTRL files into an input file:

    `python unv2oofem.py rvemesh.unv rvedd.ctrl rvedd.in`

    This creates the input file `rvedd.in`, which can be readily solved by OOFEM. The `unv2oofem` tools can be found in OOFEM sources under `tools/unv2oofem`. It's best to copy the whole directory to the working directory.
