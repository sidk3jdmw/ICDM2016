# ICDM DM1047
This code is used in the simulation of the paper entitled "Relief of Spatiotemporal Accessibility Overloading with Optimal Resource Placement", ICDM 2016

## Algorithms
- Greedy
- Gene
- Density

## Requirements

### Language and Interpreter
- PyPy 4.0.1 for Python 2

### PyPy Packages
- DEAP
- Numpy

## Execution

### Greedy
```
pypy greedy.py patient.tsv hospital.tsv
```

### Gene
```
pypy gene.py patient.tsv hospital.tsv
```

### Density
```
pypy density.py patient.tsv hospital.tsv
```

## File Format
### Hospital
File type is \*.tsv. The first line is considered as labels and will be ignored.

|   | Hospital Name | Longitude | Latitude | Capacity |
|---|:----------:|:-------------:|:-----:| :-----:|
|Type|String|Float|Float|Integer|

ex:
```
Name       \t Longitude \t Latitude \t Capacity
Hospital_1 \t 120.21898 \t 23.00218 \t 500
Hospital_2 \t 120.18384 \t 23.18191 \t 500
```
### Patients
File type is \*.tsv. The first line is considered as labels and will be ignored.

|   | Longitude | Latitude | Date |
|---|:----------:|:-------------:|:-----:|
|Type|Float|Float|String (yyyy/mm/dd)|

ex:
```
Longitude \t Latitude \t Date
120.21898 \t 23.00218 \t 2015/5/5
120.18384 \t 23.18191 \t 2015/12/3
```
## Some variables mean

### General Variables
| Variables       | Meaning                     |
|:-------------- |:-------------------------------------------- |
|process         | Num of Processes |
| alpha          | Attractiveness parameter of huff mobility    |
| beta           | Distance decay parameter of huff mobility    |
| reachable_dist | Max distance patients are willing to move to medical station.  (\*1)     |
| total_capacity | Total resources                              |
| window_size    | number of days that patients will stay in hospital         |
| tmp_num        | Number of temporary medical stations         |
| tmp_max_list   | List of capacity limit of medical stations |
| method         | Method to solve resource allocation problem (Greedy or DP)|

### Greedy Variables
| Variables       | Meaning                     |
|:-------------- |:---------------------------------------------------------------------- |
| density        | A selectable position should have at least **density** patients around |
| dist           | define the max distance that represent "around" (\*1)                   |
| step           | The distance between two selectable neighbor position (\*1)             |

### Gene Variables
| Variables       | Meaning                 |
|:-------------- |:-------------------------------------- |
| CXPB           | Crossover probability                  |
| MUTPB          | Mutation probability                   |
| NGEN           | Number of generation                   |
| NPOP           | Number of chromosomes at the beginning |

### Density Variables
| Variables       | Meaning                          |
|:-------------- |:-------------------------------------------------------------- |
| step           | The distance between two selectable neighbor position (\*1)     |

\*1 We use degree to calculate distance because 0.01 degree is about 1km in the region of dataset.
