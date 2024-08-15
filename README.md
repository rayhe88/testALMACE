# Minimum version to test remote use of the almace wrapper
The file to test the wrapper is `test_OPT.py`. Inside, you will find the definition of an opt function, which receives the file's name in xyz format to be optimized and the address of the working node (host) that will carry out the evaluation.

The first lines generate the names of the trajectory files and the final xyz structure.

This wrapper needs to include information from an electronic structure code (in this case, Quantum Espresso). This information is in the dictionaries pseudo, with details on the pseudopotentials, conf_qe, and the general parameters of quantum espresso, such as the number of k points, cutting energy, functional, etc.
Finally, the kwargs dictionary contains all the information that we pass to the ALMACE wrapper, including specific execution information, such as the DFT software, its parameters, the host, the storage location, etc.
The lines below are just the invocation of an optimization via wrapper's ALMACE.

To run it, use the following instructions:
```bash
python test_OPT.py file.xyz host
```

The following is an output when `debug` takes the value `False`.


```bash
python test_OPT.py CO_Cu36.xyz x3002c0s19b0n0
 Optimization for: CO_Cu36.xyz
      Step     Time          Energy         fmax
BFGS:    0 17:00:39  -241520.546875        0.3928
BFGS:    1 17:00:49  -241520.562500        0.3219
BFGS:    2 17:00:58  -241520.593750        0.2025
BFGS:    3 17:01:07  -241520.593750        0.1582
BFGS:    4 17:01:16  -241520.593750        0.1250
BFGS:    5 17:01:25  -241520.593750        0.1007
BFGS:    6 17:01:34  -241520.593750        0.1493
BFGS:    7 17:01:44  -241520.593750        0.1978
BFGS:    8 17:01:53  -241520.593750        0.1654
BFGS:    9 17:02:02  -241520.609375        0.0758
BFGS:   10 17:02:11  -241520.609375        0.0736
BFGS:   11 17:02:20  -241520.609375        0.1142
BFGS:   12 17:02:29  -241520.609375        0.1358
BFGS:   13 17:02:38  -241520.609375        0.0823
BFGS:   14 17:02:48  -241520.609375        0.0196
```
When debug takes the value True, the following output allows you to find out where it is running.


``` bash
python test_OPT.py CO_Cu36.xyz x3002c0s19b0n0
 Optimization for: CO_Cu36.xyz
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
      Step     Time          Energy         fmax
BFGS:    0 16:56:47  -241520.546875        0.3928
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:    1 16:56:56  -241520.562500        0.3219
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:    2 16:57:05  -241520.593750        0.2025
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:    3 16:57:14  -241520.593750        0.1582
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:    4 16:57:24  -241520.593750        0.1250
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:    5 16:57:33  -241520.593750        0.1007
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:    6 16:57:42  -241520.593750        0.1493
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:    7 16:57:51  -241520.578125        0.1978
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:    8 16:58:01  -241520.609375        0.1654
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:    9 16:58:10  -241520.609375        0.0758
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:   10 16:58:19  -241520.609375        0.0736
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:   11 16:58:28  -241520.609375        0.1142
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:   12 16:58:37  -241520.593750        0.1359
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:   13 16:58:47  -241520.609375        0.0823
 Current directory /lus/eagle/projects/catalysis_aesp/raymundohe/testOpt
 runing in the host :  x3002c0s19b0n0
BFGS:   14 16:58:56  -241520.593750        0.0196
```

Acknowledgements

This research used resources of the Argonne Leadership Computing Facility, which is a DOE Office of Science User Facility supported under Contract DE-AC02-06CH11357. Argonne National Laboratory’s work was supported by the U.S. Department of Energy, Office of Science, under contract DE-AC02-06CH11357.

All rights reserved. Copyright Argonne National Laboratory UChicago LLC. Raymundo Hernandez-Esparza
