"""
fig4_flowchart.py
=================

Render the system flowchart (figure 4) as a top-down block diagram, mirroring
the Mermaid stub in TASK.md. mermaid-cli depends on a headless Chromium that is
not reliably available here, so this script uses the Graphviz Python binding
(the `dot` engine) to produce the PNG deterministically. English-only labels.

Flow:
    Browse Left + Right Fundus
      -> Preprocessing v5 (flip -> OD-Fovea rotation -> crop -> mask
                           -> flat-field -> polar CLAHE -> normalize)
      -> EfficientNet-B3 / Config D
      -> Per-eye softmax (5 classes)
      -> Patient-level aggregation (worst-eye rule)
      -> Result: DR Grade + Referable + Confidence
      -> Grad-CAM + Attention overlay
      -> Ophthalmologist review (Confirm / Reject + corrected grade)

Output:
    ../figures_mine/fig4_flowchart.png

Requires the system Graphviz `dot` binary on PATH.
"""

from __future__ import annotations

from pathlib import Path

import graphviz

HERE = Path(__file__).resolve().parent
FIGURES_MINE = HERE.parent / "figures_mine"

NODES = [
    ("A", "Browse Left + Right Fundus", "#dbe9f6"),
    ("B", "Preprocessing v5\n"
          "flip -> OD-Fovea rotation -> crop -> mask\n"
          "-> flat-field -> polar CLAHE -> normalize", "#cfe8d8"),
    ("C", "EfficientNet-B3 / Config D", "#cfe8d8"),
    ("D", "Per-eye softmax (5 classes)", "#cfe8d8"),
    ("E", "Patient-level aggregation\nworst-eye rule", "#cfe8d8"),
    ("F", "Result: DR Grade + Referable + Confidence", "#fde6cf"),
    ("G", "Grad-CAM + Attention overlay", "#fde6cf"),
    ("H", "Ophthalmologist review\nConfirm / Reject + corrected grade", "#e8d9f0"),
]
EDGES = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"),
         ("E", "F"), ("F", "G"), ("G", "H")]


def main() -> None:
    FIGURES_MINE.mkdir(parents=True, exist_ok=True)

    g = graphviz.Digraph("system_flowchart", format="png")
    g.attr(rankdir="TB", bgcolor="white", dpi="180")
    g.attr("node", shape="box", style="rounded,filled", fontname="Helvetica",
           fontsize="12", margin="0.30,0.18", width="3.2", fixedsize="false",
           penwidth="1.2", color="#444444", fontcolor="#1a1a1a")
    g.attr("edge", color="#555555", penwidth="1.4", arrowsize="0.9")

    for node_id, label, fill in NODES:
        g.node(node_id, label, fillcolor=fill)
    for src, dst in EDGES:
        g.edge(src, dst)

    out_base = FIGURES_MINE / "fig4_flowchart"
    g.render(out_base, cleanup=True)
    print(f"[fig4] saved: {out_base.with_suffix('.png')}")


if __name__ == "__main__":
    main()
