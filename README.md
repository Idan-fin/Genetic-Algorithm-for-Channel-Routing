# Genetic Algorithm For Channel Routing

## Intro
In this project we'll implement the genetic algorithm suggested in the following article - [genetic algorithm](genetic_algorithm_for_vlsi_routing.pdf). <br>
Programming langauge: Python.


## Requirements & Instructions

#### Requirements
- Python >= 3.8

#### Instructions
- clone this repo
- `cd < your local dir path >`
- `pip install -r requirements.txt`
- prepare JSON input file (you can find examples in genetic_algo dir).
- change the path inside `genetic_algo/main.py` to match your input file.
- `python genetic_algo/main.py`


## Project Specification

### Input
#### Input Format
- JSON file.

#### Input Parameters
- pins_position: List[List[int]]
- population_size: int 
- net_length_factor: float 
- via_numbers_factor: float 
- max_descendants: int 
- max_generations: int 
- mut_1_prob: float 
- mut_2_prob: float 
- mut_3_prob: float 
- mut_4_prob: float 
- expected_final_row_num: int 
- preferred_direction_layer: list[Direction]
- num_of_optimization_rounds: int

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
- JSON file
- informative layers print

#### JSON Output Content
- given input
- best solution - 3D list
