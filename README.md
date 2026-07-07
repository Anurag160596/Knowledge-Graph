# Knowledge Graph Agent

A self-contained **knowledge graph agent**. Ask a question in plain language; the agent decides
where the facts come from — the internal knowledge base or a live web search — feeds them through a
knowledge graph, and answers from it. Every routing decision is shown, step by step.

## File

| File | Purpose |
|---|---|
| `Knowledge_Graph_Agent.html` | **The agent.** A single self-contained HTML file — a force-directed knowledge graph plus the full pipeline, all inlined. No build step, no CDN, no dependencies, fully offline. |
| `index.html` | Redirect so GitHub Pages serves the agent at the site root. |

## The pipeline logic

Every question runs through one pipeline. The graph decides *where its facts come from*, then
answers from the graph:

```
Query
  │
  ▼
① ROUTE      parse query → key terms; score how well the graph already covers it
  │
  ▼
② RETRIEVE   • coverage ≥ θ and not a "live value" ask → DATABASE path (the graph itself)
  │          • coverage < θ, or the query asks for a fresh value → WEB SEARCH path
  ▼
③ SEARCH     (web path) run the search adapter → raw results
  │
  ▼
④ EXTRACT    turn results into triples: (subject, relation, object) + value + source + confidence
  │
  ▼
⑤ MERGE      insert triples as PROVISIONAL nodes/edges — entity-resolved, provenance attached,
  │          rendered amber/dashed, never overwriting the trusted core
  ▼
⑥ SYNTHESIZE walk the (now enriched) subgraph → FINAL OUTPUT: answer + reasoning path + sources
```

The agent shows all six steps live in the answer panel, tagged **DB** or **WEB**, so the routing
decision is transparent.

### Explainability — on every answer

**Every** answer — DATABASE and WEB SEARCH alike — presents its reasoning next to the context graph as
the same labelled card, answering five questions:

| Facet | DATABASE answer | WEB SEARCH answer |
|---|---|---|
| **What** | the matched entity + summary | the extracted fact (subject + value) + confidence |
| **Where** | internal knowledge base — the node + how many linked facts | the source — title, publisher, URL |
| **When** | knowledge base *as-of* date (curated, not live) | the **publish date** of the article (+ retrieved this session) |
| **Why** | why it answered from the graph (coverage ≥ θ, no live-value ask) | why it went to the web, and why the fact grafted onto *this* node (entity resolution) |
| **How** | `matched node → traversed its relations → composed the answer` | `web result → extract triple → merge provisional node → answer reads the enriched subgraph` |

Every node name in the card is clickable and highlights the corresponding node in the graph, so the
reasoning and the context graph stay in sync. For web-sourced nodes, the same provenance (source,
publisher, publish date, confidence) also appears in the inspector when you click the node.

## The knowledge base (demo data)

A neutral, fictional example graph — the canonical shape for a knowledge graph agent — with five node
types, colour-coded:

- **Person** (teal) — Ada Lovelace, Grace Hopper, Alan Turing, Katherine Johnson
- **Team** (violet) — Platform, Data, Design
- **Project** (blue) — Atlas, Beacon, Comet
- **Technology** (grey) — Python, GraphQL, graph database, design system
- **Document** (green) — the Atlas and Beacon specs

Edges are typed relationships (`leads`, `member of`, `owns`, `depends on`, `has skill`, `authored`,
`describes`), so you can trace who works on what, what a project depends on, or who knows a technology.

Web-sourced facts arrive as a sixth type, **Web-sourced** (amber, dashed).

## Routing rule

- A question already in the graph — *"who works on Project Atlas?"*, *"what does Beacon depend on?"*,
  *"who knows Python?"* → **DATABASE** path (answered from the graph).
- A question asking for a live value — *"latest Python release?"*, *"GraphQL latest spec?"*,
  *"graph database options?"* → **WEB SEARCH** path: the agent searches, extracts the fact, grafts it
  onto the right node as a **provisional** node, then answers from the enriched graph.

## Trust tiers

Curated nodes come from the internal knowledge base and are trusted. Web-sourced nodes are
**provisional** — amber/dashed, with provenance (source, date) and a confidence flag, and an explicit
*"validate before relying on it."* Web facts never overwrite the curated core. A **✕ clear web-added
nodes** control removes them.

## Source adapter

`webSearch()` is an adapter over a bundled snapshot so the whole flow runs offline. Swap its one-line
body for a real search API (Brave / Serper / Bing) in a hosted build; the `extract` step is where an
NER / LLM extractor plugs in to produce the triples.

## Connect a real backend — Neo4j Labs `llm-graph-builder`

The agent can hydrate its graph and answer from a live [neo4j-labs/llm-graph-builder](https://github.com/neo4j-labs/llm-graph-builder)
instance instead of the demo data. Click the **◍ Demo (offline)** chip in the Agent header to open the
connection panel.

**Prerequisites:** run the llm-graph-builder backend (FastAPI + Neo4j 5.23+ with APOC + an LLM API key)
— typically via its Docker Compose. Because a page served over `https` can't call a `http://localhost`
backend (mixed-content), **open this HTML file locally** (or from the same origin as the backend) when
connecting, and make sure the backend allows CORS from that origin.

**What it wires** (endpoints from the project's `backend/score.py`):

| Step | Endpoint | Use |
|---|---|---|
| Connect | `POST /schema` | validate the Neo4j connection, read node labels |
| Load graph | `POST /graph_query` | pull nodes + relationships → rendered on the canvas as **Neo4j** nodes (blue, dashed) |
| Ask | `POST /chat_bot` | GraphRAG answer in the selected mode (`vector`, `graph`, `graph_vector`, `fulltext`, …) |

Neo4j credentials (`uri`, `userName`, `password`, `database`) and the model / chat mode are entered in
the panel and sent as form fields, exactly as the backend expects.

When connected, a question routes to `/chat_bot` and the answer is shown in the same
**What / Where / When / Why / How** card — badged **NEO4J · GraphRAG** — with the backend's **source
attribution** (cited documents), the response time, and the retrieval mode. If the backend is
unreachable, the agent reports it and falls back to the offline demo; **Use demo (offline)** restores the
demo graph at any time. The connector is a thin client — no keys or data are stored in the file.

## Use it

- **Open / share:** download `Knowledge_Graph_Agent.html` and open in any browser, or host via GitHub Pages.
- **Explore:** drag nodes, click to inspect, scroll / pinch to zoom, toggle node types with the legend chips.
- **Ask:** type a question, or tap a suggested one. Runs entirely offline — no API required.
- Mobile-responsive (graph on top, inspector + agent below).

> Demo data is fictional and for illustration; web-snapshot results are illustrative and flagged provisional.
