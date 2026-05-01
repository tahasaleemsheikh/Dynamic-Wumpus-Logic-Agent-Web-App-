from flask import Flask, render_template, request, jsonify
import random
from itertools import product

app = Flask(__name__)

# -------- GLOBAL STATE --------
ROWS, COLS = 4, 4
grid = []
agent = [0, 0]
visited = set()
safe = set()
danger = set()
KB = []          # list[set[str]]  (CNF clauses)
steps = 0

# -------- UTIL --------
def cell(r, c): return f"{r}_{c}"

def neighbors(r, c):
    dirs = [(0,1),(1,0),(-1,0),(0,-1)]
    res = []
    for dr, dc in dirs:
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            res.append((nr, nc))
    return res

# -------- ENV --------
def init_world(r, c):
    global ROWS, COLS, grid, agent, visited, safe, danger, KB, steps
    ROWS, COLS = r, c
    grid = [["" for _ in range(COLS)] for _ in range(ROWS)]
    agent = [0, 0]
    visited.clear(); safe.clear(); danger.clear(); KB.clear()
    steps = 0

    # place one Wumpus (not at start)
    while True:
        wr, wc = random.randrange(ROWS), random.randrange(COLS)
        if (wr, wc) != (0, 0):
            grid[wr][wc] = "W"; break

    # place pits (~20% cells, avoid start & Wumpus)
    pits = max(1, (ROWS * COLS)//5)
    placed = 0
    while placed < pits:
        pr, pc = random.randrange(ROWS), random.randrange(COLS)
        if (pr, pc) != (0, 0) and grid[pr][pc] == "":
            grid[pr][pc] = "P"
            placed += 1

def percept(r, c):
    b = s = False
    for nr, nc in neighbors(r, c):
        if grid[nr][nc] == "P": b = True
        if grid[nr][nc] == "W": s = True
    return {"breeze": b, "stench": s}

# -------- CNF + RESOLUTION --------
def neg(lit): return lit[1:] if lit.startswith("~") else "~" + lit

def resolve(ci, cj):
    out = []
    for di in ci:
        for dj in cj:
            if di == neg(dj):
                newc = set(ci) | set(cj)
                newc.discard(di); newc.discard(dj)
                out.append(newc)
    return out

def ask(query):
    """Resolution refutation: KB ⊨ query ?"""
    global steps
    clauses = [set(c) for c in KB]
    clauses.append({neg(query)})
    new = set()

    while True:
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                steps += 1
                for r in resolve(clauses[i], clauses[j]):
                    if not r:
                        return True
                    new.add(frozenset(r))
        if new.issubset(set(map(frozenset, clauses))):
            return False
        for c in new:
            sc = set(c)
            if sc not in clauses:
                clauses.append(sc)

# -------- KB (TELL rules) --------
def tell_percept(r, c):
    """Add CNF rules based on percept at (r,c)."""
    p = percept(r, c)
    visited.add((r, c))
    safe.add((r, c))

    nbrs = neighbors(r, c)

    # Breeze rules
    if not p["breeze"]:
        # ~P for all neighbors
        for nr, nc in nbrs:
            KB.append({f"~P_{cell(nr,nc)}"})
    else:
        # at least one neighbor has pit: (P_n1 ∨ P_n2 ∨ ...)
        KB.append({f"P_{cell(nr,nc)}" for nr, nc in nbrs})

    # Stench rules
    if not p["stench"]:
        for nr, nc in nbrs:
            KB.append({f"~W_{cell(nr,nc)}"})
    else:
        KB.append({f"W_{cell(nr,nc)}" for nr, nc in nbrs})

    return p

def is_safe(r, c):
    name = cell(r, c)
    # if KB proves hazard → mark danger
    if ask(f"P_{name}") or ask(f"W_{name}"):
        danger.add((r, c))
        return False
    # if KB proves no hazard → safe
    if ask(f"~P_{name}") and ask(f"~W_{name}"):
        return True
    return False

# -------- AGENT (frontier search) --------
def frontier():
    fr = set()
    for (r, c) in visited:
        for nr, nc in neighbors(r, c):
            if (nr, nc) not in visited:
                fr.add((nr, nc))
    return list(fr)

def next_move():
    r, c = agent
    p = tell_percept(r, c)

    # choose among frontier cells proven safe
    for nr, nc in frontier():
        if is_safe(nr, nc):
            agent[0], agent[1] = nr, nc
            return p, "moved"

    # if none proven safe, stay (conservative)
    return p, "no-safe-move"

# -------- ROUTES --------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/init", methods=["POST"])
def init():
    data = request.get_json()
    r = int(data.get("rows", 4))
    c = int(data.get("cols", 4))
    r = max(2, min(10, r))
    c = max(2, min(10, c))
    init_world(r, c)
    return jsonify({"ok": True, "rows": ROWS, "cols": COLS})

@app.route("/step")
def step():
    p, status = next_move()
    return jsonify({
        "rows": ROWS,
        "cols": COLS,
        "pos": agent,
        "visited": list(visited),
        "safe": list(safe),
        "danger": list(danger),
        "percept": p,
        "steps": steps,
        "status": status
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)