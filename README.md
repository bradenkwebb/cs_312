# Algorithm Design and Analysis
This repository contains the code I wrote when I took CS 312 at BYU Winter 2023. Boilerplate GUI code was provided by TAs for testing and debugging the various projects, but all of the implementations are my own.

### Project 1: Probabilistic Primality Testing
This project featured mastery of modular arithmetic and the modular exponentiation algorithm to implement both the Fermat primality test and the Miller-Rabin primality test.

### Project 2: Convex Hull
For this project, I built an efficient divide-and-conquer algorithm for solving the Convex Hull problem.

### Project 3: Network Routing
I implemented a priority queue from scratch, and then used it to implement Dijkstra's algorithm to find the shortest paths between two points in a graph for a network-routing context.'

### Project 4: Gene Sequencing
This problem focused on identifying mutations in DNA sequences through edit distance approaches. I implemented a standard version of the Needleman/Wunsch edit distance algorithm as well as a banded variation which, for some positive integer $d$, only considers alignments of *seq1* and *seq2* for which the $i$th character of *seq1* is within distance $d$ of the $j$th character of *seq2*.

### Project 5: Traveling Salesman Problem (TSP)
Although TSP is NP-hard, many heuristic-based approximation algorithms can be applied to it quite effectively. For this project, I implemented and analyzed a greedy solution, a random-path solution, and a branch-and-bound solution to the asymmetric TSP. 

### Project 6: Ant Colony Optimization for TSP
This was a group project that I led in implementing a version of the stochastic, multi-agent Max-Min Ant Colony Optimization (ACO) algorithm [(Stützle & Hoos, 2000)](https://doi.org/10.1016/S0167-739X(00)00043-1) as an improvement upon the work done in Project 5. We went above and beyond in searching through relevant current literature and trying to understand the various ACO approaches that exist. I would have gladly put more time into this assignment if they had given us more time before finals week began, but I still ended up pretty happy with our final product.

I also spent a lot of time formatting that write-up in LaTeX in my local editor rather than on Overleaf. That was the first time I'd used LaTeX that way, and the `group_tsp_report` directory is still quite messy because of it - including the entire raw README.md from the original PaperShell repository that I cloned at the beginning. Maybe some day I'll get around to cleaning that up.
