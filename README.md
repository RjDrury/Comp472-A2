# Comp472-A2

Solves a 2x4 puzzle by putting 7 randomly generated numbers into order using moves up, down, right, left and diagonal 
wrapping moves.  

The puzzle solution is generated using one of 3 search algorithms
* Uniform cost
* Greedy best first 
* A*

GBFS and A* use one of two heuristics to find their solutions 
* hamming distance
* modified manhattan distance that takes into account the effect of diagonal moves and always returns a value 
h() <= h*(n) so that it is admissible
