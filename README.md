# Simple Path Finding — Technical Overview

This project demonstrates three fundamental path-finding algorithms:
**Breadth-First Search (BFS)**, **Uniform-Cost Search (UCS)**, and **A\***.

It’s written in Python with a focus on clarity and algorithm comparison rather than performance.

## Purpose
The goal is to find an optimal path between a start and goal node in a graph, using different search strategies.  
It allows testing of both uninformed (BFS, UCS) and informed (A\*) methods, with optional heuristic inputs.

## Implementation
- **BFS** explores all nodes level by level and guarantees the shortest path only in unweighted graphs.  
- **UCS** extends BFS by prioritizing nodes with the lowest cumulative cost.  
- **A\*** combines UCS with a heuristic function `h(n)` to guide the search more efficiently toward the goal.  

All algorithms share the same graph-parsing and path-reconstruction logic, making their outputs easy to compare.

## Example Workflow
1. Load graph data (e.g., `istra.txt`).
2. Choose algorithm (`BFS`, `UCS`, or `A*`).
3. (Optional) Load a heuristic file for `A*`.
4. Run and compare output path, total cost, and visited nodes.

## Key Takeaways
- Demonstrates algorithmic trade-offs between completeness, optimality, and efficiency.  
- Modular design allows easy addition of new algorithms or heuristics.  
- Ideal for educational or visualization purposes in AI and graph theory contexts.

Repository: [github.com/andro5/simple-path-finding](https://github.com/andro5/simple-path-finding)
