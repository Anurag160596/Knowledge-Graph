# Knowledge-Graph

A knowledge graph built **from scratch with Claude Code** — no framework, no database
server, no external dependencies. It's a working proof-of-concept that answers the
question: *"Can I create knowledge from scratch using Claude Code?"* Yes.

The demo domain is the **ABL / Kore.ai contact-center value model** (from the
companion `Value-Creation-Dshboard` repo): its concepts, benchmark sources, cost
assumptions, and the causal links between them — turned into queryable nodes and edges.

## What's here

| File | What it is |
|---|---|
| `knowledge_graph.json` | The knowledge itself: **24 nodes, 30 edges**. Entities (products, tiers, assumptions, metrics, sources) and typed relationships (`DRIVES`, `SOURCED_FROM`, `DISCOUNTED_BY`, …). |
| `kg.py` | A tiny, dependency-free CLI to query the graph (stats, search, show, neighbors, shortest path). |
| `graph.html` | A self-contained interactive visualizer — force-directed layout, tap a node to inspect it. No CDN; the data is inlined. Open it directly in a browser. |

## Try it

```bash
python3 kg.py stats                     # size + node types
python3 kg.py show effective_deflection # a node and all its relationships
python3 kg.py search token              # find nodes by text
python3 kg.py neighbors abl             # one hop out from ABL
python3 kg.py path tier_low npv         # how a low-tier deflection reaches NPV
```

Then open `graph.html` in any browser to see it visually.

## The data model

A node is `{ id, type, label, props }`. An edge is `{ from, rel, to }`. That's the whole
schema — deliberately minimal so it's easy to read and extend. Add a node to the `nodes`
array, wire it up in `edges`, and both `kg.py` and `graph.html` pick it up (re-inline the
JSON into the HTML if you change it — see below).

## Where this can go next

This POC covers the *shape* of a knowledge system. Natural next steps, depending on what you want:

- **Bigger graph** — extend the schema and add more entities/relationships, or write an
  ingestion script that extracts a graph from source documents.
- **Real graph store** — swap the JSON for SQLite or Neo4j; the query surface in `kg.py`
  maps directly onto Cypher.
- **Knowledge base / RAG** — add embeddings + semantic search over documents and answer
  questions with citations (Claude API).
- **Auto-extraction** — point Claude at your docs and have it propose new nodes/edges.

Tell me which direction and I'll build it out.

### Rebuilding graph.html after editing the data

`graph.html` inlines the JSON so it works offline with no fetch. If you edit
`knowledge_graph.json`, re-inline it:

```bash
python3 - <<'PY'
import json
data = open('knowledge_graph.json').read()
html = open('graph.html').read()
import re
html = re.sub(r'const G = \{.*?\n\};', 'const G = ' + data.rstrip() + ';', html, count=1, flags=re.S)
open('graph.html','w').write(html)
print("re-inlined")
PY
```
