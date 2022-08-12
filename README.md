# Genetic Algorithm For Channel Routing

## Intro
In this project we'll implement the genetic algorithm suggested in the following article - [genetic algorithm](genetic_algorithm_for_vlsi_routing.pdf). <br>
Programming langauge: Python.


## Project Specification

### Input
#### Input Format
- basic - XML file.
- extended - GUI.

#### Input Parameters
- pins locations - 2D array.
- P_c - population size - int.
- max number of descendants - int.
- number of generations - int.
- a - net length factor - float.
- b - number of vias factor - float.
- mut_1 - probability to get mutation of type 1 in a single iteration - float.
- mut_2 - probability to get mutation of type 2 in a single iteration - float.
- mut_3 - probability to get mutation of type 3 in a single iteration - float.
- mut_4 - probability to get mutation of type 4 in a single iteration - float.

#### Extra Goals
- get multiple input problems.
- GUI.

---

### Algorithm Phases
for detailed information please refer the [article](genetic_algorithm_for_vlsi_routing.pdf) 
- create initial population
  - create individual - single solution for our the input problem.
  - implement <b>random routing</b> operation.
- fitness calculation 
  - calculate groups of solutions by number of rows.
  - calculate net length (accurate direction).
  - calculate net length (opposite direction).
  - calculate number of vias.
  - calculate total fitness according to the formula.
- partner selection
  - pick 2 solutions with fitness based probability.
- create descendant (parents cross)
  - random cut point, take each side from a different parent, remove connections that cross the cut and apply random routing if needed.
- reduction
  - calculate fitness for descendants.
  - pick the best P_c (population size) from old + new generations.
- calculate P_best (the best solution) and keep it
- mutation
  - for each solution:
    - sort the mutations randomly.
    - apply/skip with probability from the input file.
    - mutation details in the article.
  - <b>extra</b> - try to add more mutations.
- P_best optimization
  - final phase.
  - apply random mutations on P_best and except only better solutions.

---
### Output

#### Output Format
- basic - XML
- extended - GUI 

#### Output Content
- best solution
- basic - Genotype
  - 3D array
- extended - Phenotype
  - image of the best circuit

#### Benchmarks and Testing
- basic:
  - run the algorithm on several inputs
- extended:
  - run the algorithm on known benchmarks and try to get similar results to the article.
  - tables and graphs.
