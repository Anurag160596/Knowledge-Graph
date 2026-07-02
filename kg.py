#!/usr/bin/env python3
"""
kg.py — a tiny, dependency-free knowledge-graph query tool.

Demonstrates the core operations any knowledge graph supports, over the
ABL / Kore.ai value model graph in knowledge_graph.json:

    python kg.py stats                 # size + node types
    python kg.py nodes [TYPE]          # list nodes (optionally by type)
    python kg.py show NODE_ID          # a node + all its relationships
    python kg.py search TEXT           # find nodes by label/props
    python kg.py neighbors NODE_ID     # one hop out
    python kg.py path FROM_ID TO_ID    # shortest relationship path

This is a proof-of-concept. Swap the JSON for SQLite/Neo4j and the same
query surface scales to millions of edges.
"""
import json
import os
import sys
from collections import deque, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH_PATH = os.path.join(HERE, "knowledge_graph.json")


def load():
    with open(GRAPH_PATH, encoding="utf-8") as f:
        g = json.load(f)
    g["_by_id"] = {n["id"]: n for n in g["nodes"]}
    out = defaultdict(list)
    inn = defaultdict(list)
    for e in g["edges"]:
        out[e["from"]].append(e)
        inn[e["to"]].append(e)
    g["_out"], g["_in"] = out, inn
    return g


def _label(g, nid):
    n = g["_by_id"].get(nid)
    return f"{n['label']} ({nid})" if n else f"<missing:{nid}>"


def cmd_stats(g, _):
    types = defaultdict(int)
    for n in g["nodes"]:
        types[n["type"]] += 1
    print(f"{g['meta']['name']}")
    print(f"  {len(g['nodes'])} nodes, {len(g['edges'])} edges\n")
    print("  Node types:")
    for t, c in sorted(types.items(), key=lambda x: -x[1]):
        print(f"    {c:>3}  {t}")


def cmd_nodes(g, args):
    want = args[0] if args else None
    for n in g["nodes"]:
        if want and n["type"] != want:
            continue
        print(f"  [{n['type']:<15}] {n['id']:<20} {n['label']}")


def cmd_show(g, args):
    nid = args[0]
    n = g["_by_id"].get(nid)
    if not n:
        print(f"No such node: {nid}")
        return
    print(f"{n['label']}  [{n['type']}]")
    if n.get("props"):
        for k, v in n["props"].items():
            print(f"    {k}: {v}")
    print("\n  Outgoing:")
    for e in g["_out"].get(nid, []):
        print(f"    --{e['rel']}--> {_label(g, e['to'])}")
    print("  Incoming:")
    for e in g["_in"].get(nid, []):
        print(f"    <--{e['rel']}-- {_label(g, e['from'])}")


def cmd_search(g, args):
    q = " ".join(args).lower()
    for n in g["nodes"]:
        hay = (n["id"] + " " + n["label"] + " " + json.dumps(n.get("props", {}))).lower()
        if q in hay:
            print(f"  {n['id']:<20} {n['label']}  [{n['type']}]")


def cmd_neighbors(g, args):
    nid = args[0]
    seen = set()
    for e in g["_out"].get(nid, []):
        print(f"    --{e['rel']}--> {_label(g, e['to'])}")
        seen.add(e["to"])
    for e in g["_in"].get(nid, []):
        print(f"    <--{e['rel']}-- {_label(g, e['from'])}")


def cmd_path(g, args):
    src, dst = args[0], args[1]
    # BFS over undirected view; remember the edge used to reach each node.
    prev = {src: None}
    q = deque([src])
    while q:
        cur = q.popleft()
        if cur == dst:
            break
        for e in g["_out"].get(cur, []):
            if e["to"] not in prev:
                prev[e["to"]] = (cur, e["rel"], "->")
                q.append(e["to"])
        for e in g["_in"].get(cur, []):
            if e["from"] not in prev:
                prev[e["from"]] = (cur, e["rel"], "<-")
                q.append(e["from"])
    if dst not in prev:
        print(f"No path from {src} to {dst}")
        return
    steps = []
    node = dst
    while prev[node] is not None:
        frm, rel, direction = prev[node]
        arrow = f"--{rel}-->" if direction == "->" else f"<--{rel}--"
        steps.append(f"  {_label(g, frm)}  {arrow}  {_label(g, node)}")
        node = frm
    for line in reversed(steps):
        print(line)


COMMANDS = {
    "stats": cmd_stats, "nodes": cmd_nodes, "show": cmd_show,
    "search": cmd_search, "neighbors": cmd_neighbors, "path": cmd_path,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(0 if len(sys.argv) < 2 else 1)
    g = load()
    COMMANDS[sys.argv[1]](g, sys.argv[2:])


if __name__ == "__main__":
    main()
