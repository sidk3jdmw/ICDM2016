ICDM2016
===============

Requirements
--------

- PyPy 4.0.1 (for python 2)
- DEAP (Python Package)

Data
--------

### Hospitals Data


### Patients Data


Algorithm
--------

- Gene Method - gene.py
- Greedy Method - greedy.py
- Density Based Method - density.py


How to use
--------

1. Install PyPy 4.0.1 for Python 2 (Cannot use CPython due to the different behavior of multiprocessing)
2. Install Deap package for PyPy
3. Choose a algorithm and set arguments in the corresponding file.
4. run "pypy greedy.py" (or other algorithm files)

Arguments
----------

### General Arguments
| Argument       | Meaning                                      |
|:-------------- |:-------------------------------------------- |
| alpha          | Attractiveness parameter of huff mobility    |
| beta           | distance decay parameter of huff mobility    |
| reachable_dist | The distance patients can abort (degree)     |
| total_capacity | Total resources                              |
| window_size    |            |
| tmp_num        | Number of temporary medical stations         |
| tmp_max_list   | List of maximum capacity of medical stations |

### Greedy Arguments
| Argument       | Meaning                                                                |
|:-------------- |:---------------------------------------------------------------------- |
| density        | A selectable position should have at least **density** patients around |
| dist           | define the max distance that represent "around" (degree)               |
| step           | The distance between two selectable neighbor position (degree)         |

### Gene Arguments
| Argument       | Meaning                                |
|:-------------- |:-------------------------------------- |
| CXPB           | Crossover probability                  |
| MUTPB          | Mutation probability                   |
| NGEN           | Number of generation                   |
| NPOP           | Number of chromosomes at the beginning |

### Density Arguments
| Argument       | Meaning                                                        |
|:-------------- |:-------------------------------------------------------------- |
| step           | The distance between two selectable neighbor position (degree) |

> For the region in dataset, one degree is about 100 km

