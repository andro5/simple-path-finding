import sys
import heapq
from collections import deque

# ucitavanja ss (prostor stanja)
def load_state_space(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if not line.startswith("#")]

    start_state = lines[0]
    goal_states = set(lines[1].split())
    transitions = {}

    for line in lines[2:]:
        parts = line.split(":")
        state = parts[0].strip()
        neighbors = [n.split(",") for n in parts[1].split()]
        transitions[state] = {n[0]: float(n[1]) for n in neighbors}

    return start_state, goal_states, transitions

# ucitavanje heuristic fajla
def load_heuristics(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if not line.startswith("#")]

    return {line.split(":")[0].strip(): float(line.split(":")[1].strip()) for line in lines}

# razlika izmedju bfs (breadth first search) i ucs (uniform cost search)
# bfs ne koristi troskove nego trazi rjesenje s najmanjim brojem koraka
# bfs koristi red (deque), ucs koristi heap (heapq)
def bfs(start, goals, transitions):
    queue = deque([(start, [])])
    visited = set()
    states_visited = 0
    while queue:
        state, path = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        states_visited += 1
        path.append(state)
        if state in goals:
            return path, states_visited
        for neighbor in sorted(transitions.get(state, {})):
            queue.append((neighbor, path[:]))
    return None, states_visited

def ucs(start, goals, transitions):
    pq = [(0, start, [])]
    visited = {}
    states_visited = 0
    while pq:
        cost, state, path = heapq.heappop(pq)
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost
        states_visited += 1
        path.append(state)
        if state in goals:
            return path, cost, states_visited
        for neighbor, edge_cost in sorted(transitions.get(state, {}).items()):
            heapq.heappush(pq, (cost + edge_cost, neighbor, path[:]))
    return None, float("inf"), states_visited

# a* radi kao ucs ali dodaje heuristicne vrijednosti
# red sortira po f = g + h ; g-stvarni trosak, h-procjenjena udaljenosti od cilja
def a_star(start, goals, transitions, heuristics):
    pq = [(heuristics[start], 0, start, [])]
    visited = {}
    states_visited = 0
    while pq:
        _, cost, state, path = heapq.heappop(pq)
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost
        states_visited += 1
        path.append(state)
        if state in goals:
            return path, cost, states_visited
        for neighbor, edge_cost in sorted(transitions.get(state, {}).items()):
            heapq.heappush(pq, (cost + edge_cost + heuristics.get(neighbor, 0), cost + edge_cost, neighbor, path[:]))
    return None, float("inf"), states_visited

# check

# optimistic znaci da ne precjenjuje stvarni trosak do cilja

# consistent znaci da heuristika mora biti logicna i ne odskakati puno
# procjena udaljenosti iz stanja S ne smije skočiti previsoko u odnosu na procjenu iz susjednog stanja T,
# kad uračunaš cijenu koraka između njih
def check_optimistic(heuristics, start, goals, transitions):
    print("# HEURISTIC-OPTIMISTIC")
    optimistic = True
    for state, h_value in heuristics.items():
        _, true_cost, _ = ucs(state, goals, transitions)
        if h_value > true_cost:
            print(f"[CONDITION]: [ERR] h({state}) <= h*: {h_value:.1f} <= {true_cost:.1f}")
            optimistic = False
        else:
            print(f"[CONDITION]: [OK] h({state}) <= h*: {h_value:.1f} <= {true_cost:.1f}")
    print(f"[CONCLUSION]: Heuristic is {'optimistic' if optimistic else 'not optimistic'}.")

def check_consistent(heuristics, transitions):
    print("# HEURISTIC-CONSISTENT")
    consistent = True
    for state in transitions:
        for neighbor, cost in transitions[state].items():
            if heuristics[state] > heuristics[neighbor] + cost:
                print(
                    f"[CONDITION]: [ERR] h({state}) <= h({neighbor}) + c: {heuristics[state]:.1f} <= {heuristics[neighbor]:.1f} + {cost:.1f}")
                consistent = False
            else:
                print(
                    f"[CONDITION]: [OK] h({state}) <= h({neighbor}) + c: {heuristics[state]:.1f} <= {heuristics[neighbor]:.1f} + {cost:.1f}")
    print(f"[CONCLUSION]: Heuristic is {'consistent' if consistent else 'not consistent'}.")

def main():
    args = sys.argv[1:]
    alg, ss_file, h_file, check_opt, check_cons = None, None, None, False, False

    i = 0
    while i < len(args): # rucno parsiranje argumenata
        if args[i] == "--alg":
            alg = args[i + 1]
            i += 1
        elif args[i] == "--ss":
            ss_file = args[i + 1]
            i += 1
        elif args[i] == "--h":
            h_file = args[i + 1]
            i += 1
        elif args[i] == "--check-optimistic":
            check_opt = True
        elif args[i] == "--check-consistent":
            check_cons = True
        i += 1

    start, goals, transitions = load_state_space(ss_file)
    heuristics = load_heuristics(h_file) if h_file else {}

    path, cost, states_visited = None, None, None

    if check_opt:
        check_optimistic(heuristics, start, goals, transitions)
        return
    elif check_cons:
        check_consistent(heuristics, transitions)
        return

    if alg == "bfs":
        path, states_visited = bfs(start, goals, transitions)
        print("# BFS")
    elif alg == "ucs":
        path, cost, states_visited = ucs(start, goals, transitions)
        print("# UCS")
        print(f"[TOTAL_COST]: {round(cost, 1)}")
    elif alg == "astar":
        path, cost, states_visited = a_star(start, goals, transitions, heuristics)
        print("# A-STAR")
        print(f"[TOTAL_COST]: {round(cost, 1)}")

    if path:
        print("[FOUND_SOLUTION]: yes")
        print(f"[STATES_VISITED]: {states_visited}")
        print(f"[PATH_LENGTH]: {len(path)}")
        print("[PATH]:", " => ".join(path))
    else:
        print("[FOUND_SOLUTION]: no")

if __name__ == "__main__":
    main()