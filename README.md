# Knowledge-Graph

An interactive **knowledge graph agent** for the Kore.ai / ABL contact-center value model.

It maps the whole value thesis as a graph — the moat arguments, the complexity tiers, the
cost/value formulas, the deal inputs, and the Gartner / McKinsey / Forrester benchmarks that
back every number — and puts an **agent** in front of it that answers questions by tracing the
graph.

## File

| File | Purpose |
|---|---|
| `ABL_Knowledge_Graph_Agent.html` | **The agent.** A single self-contained HTML file — force-directed knowledge graph + a retrieval agent, all inlined. No build step, no CDN, no dependencies, fully offline. |
| `index.html` | Redirect so GitHub Pages serves the graph at the site root. |

## What's in the graph

Five node types, colour-coded (dark instrument-panel aesthetic, matching the ABL dashboard lineage):

- **Thesis / moat** (teal) — deterministic workflows, cost-per-resolution moat, seat-decay contradiction, value concentrated in the low tier.
- **Complexity tier** (violet) — Low (0 LLM calls, 90% auto), Medium (1 call, 60%), High (4 calls, 25%).
- **Formula / metric** (blue) — effective deflection, ABL cost/resolution, LLM token cost, tier value, seats released, 3-yr NPV & payback.
- **Deal input** (grey) — 100M volume, 20k agents, $45k/agent, $0.20 platform floor, token prices, $7.16 human cost.
- **Analyst source** (amber) — the Gartner / McKinsey / Forrester findings that ground each claim.

Edges are typed relationships (`grounds`, `feeds`, `drives`, `sizes`, …) so you can trace, for any
number, exactly which formula produces it and which benchmark backs it.

## The agent

Ask a question in plain language — *"why is ABL's cost flat?"*, *"what backs the 80% claim?"*,
*"how are seats freed?"* — and the agent:

1. Matches intent (rules first, then keyword retrieval across every node), and
2. Answers with the relevant formula/benchmark, **focuses the matching node in the graph**, and
   cites the source. Node names in the answer are clickable and jump you around the graph.

Runs entirely offline — no API required. The retrieval is deterministic and self-contained.

## Use it

- **Open / share:** download `ABL_Knowledge_Graph_Agent.html` and open in any browser, or host via GitHub Pages.
- **Explore:** drag nodes, click to inspect, scroll / pinch to zoom, toggle node types with the legend chips.
- Mobile-responsive (graph on top, inspector + agent below).

> The value model here mirrors the shared math documented in `CLAUDE.md` of the value-modeling
> system. Benchmarks are external analyst projections; realized value depends on execution.
