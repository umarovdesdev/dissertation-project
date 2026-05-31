"""
fig6_model_graph.py
===================

Analog of Omarov's Figure 6 ("Proposed CNN" — Keras `plot_model` graph).

Hybrid (Option B) rendering of the architecture of our model
(EfficientNet-B3 / Config D). A single PNG composed of two side-by-side panels:

  * LEFT  — "Outer architecture": the 13-node block-level top-down sequence
            (Input -> Stem -> Stage 1..7 -> Head -> GAP -> Dropout -> FC).
  * RIGHT — "MBConv6 block (zoom-in)": one representative MBConv6 block expanded
            into individual layers in Keras `plot_model` style, each box carrying
            a "layer_name (LayerType)" row and an "input -> output" shape row.

This preserves Omarov's per-layer "shape graph" character while staying readable
at document scale, instead of the ~12k x 30k pixel full-network autograd dump.

Two outputs are produced:
    ../figures_mine/fig6_model_graph.png       (hybrid two-panel diagram)
    ../figures_mine/fig6_model_summary.txt     (torchinfo summary)

The textual summary is only (re)generated when it is missing, so an existing
summary is never clobbered. If `graphviz` is unavailable the diagram render is
skipped (and, when a model is built, an ONNX export at fig6_model.onnx is
written instead — open with Netron at https://netron.app).

Usage:
    pip install torchviz torchinfo  # + system graphviz binary
    python fig6_model_graph.py
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
WEBAPP_DIR = HERE.parent
PROJECT_ROOT = WEBAPP_DIR.parent.parent.parent  # E:/dissertation-project
EXPERIMENTS = PROJECT_ROOT / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

OUTPUT_GRAPH = WEBAPP_DIR / "figures_mine" / "fig6_model_graph.png"
OUTPUT_SUMMARY = WEBAPP_DIR / "figures_mine" / "fig6_model_summary.txt"
OUTPUT_ONNX = WEBAPP_DIR / "figures_mine" / "fig6_model.onnx"

# Config D uses 4-channel input (RGB + FOV mask) and EfficientNet-B3.
INPUT_SHAPE = (1, 4, 512, 512)


def build_model():
    """Instantiate Config D (EfficientNet-B3, 4 input channels, 5 classes)."""
    import torch

    # Try the project factory first; fall back to a timm baseline if unavailable.
    try:
        from src.models.factory import create_model  # type: ignore
        model = create_model(
            "efficientnet_b3",
            in_channels=INPUT_SHAPE[1],
            num_classes=5,
        )
    except Exception as exc:  # pragma: no cover - fallback path
        print(f"[warn] project factory unavailable ({exc}); using timm fallback.")
        import timm

        model = timm.create_model(
            "efficientnet_b3",
            pretrained=False,
            in_chans=INPUT_SHAPE[1],
            num_classes=5,
        )

    return model.eval()


def write_summary(model) -> None:
    OUTPUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    try:
        from torchinfo import summary  # type: ignore

        info = summary(
            model,
            input_size=INPUT_SHAPE,
            depth=4,
            col_names=("input_size", "output_size", "num_params", "trainable"),
            row_settings=("var_names",),
            verbose=0,
        )
        OUTPUT_SUMMARY.write_text(str(info), encoding="utf-8")
        print(f"Saved: {OUTPUT_SUMMARY}")
    except Exception as exc:
        OUTPUT_SUMMARY.write_text(
            f"torchinfo unavailable: {exc}\nInstall with: pip install torchinfo\n",
            encoding="utf-8",
        )
        print(f"[warn] torchinfo failed: {exc}")


# EfficientNet-B3 block-level architecture (width 1.2x, depth 1.4x).
# Per-stage out-channels and repeat counts follow the standard B3 scaling of the
# EfficientNet base config; kernel sizes and the MBConv expansion ratios match
# the reference implementation. Drawn as a compact top-down block diagram so the
# figure is readable at document scale instead of a ~30k-pixel autograd dump.
STEM_FILL = "#dbe9f6"
BLOCK_FILL = "#cfe8d8"
HEAD_FILL = "#fde6cf"
CLS_FILL = "#e8d9f0"

ARCH_NODES = [
    ("in",   "Input\n4 x 512 x 512  (RGB + FOV mask)", STEM_FILL),
    ("stem", "Stem: Conv 3x3, stride 2  ->  40 ch\nBatchNorm + SiLU", STEM_FILL),
    ("s1",   "Stage 1: MBConv1, k3x3  ->  24 ch  (x2)", BLOCK_FILL),
    ("s2",   "Stage 2: MBConv6, k3x3  ->  32 ch  (x3)", BLOCK_FILL),
    ("s3",   "Stage 3: MBConv6, k5x5  ->  48 ch  (x3)", BLOCK_FILL),
    ("s4",   "Stage 4: MBConv6, k3x3  ->  96 ch  (x5)", BLOCK_FILL),
    ("s5",   "Stage 5: MBConv6, k5x5  ->  136 ch  (x5)", BLOCK_FILL),
    ("s6",   "Stage 6: MBConv6, k5x5  ->  232 ch  (x6)", BLOCK_FILL),
    ("s7",   "Stage 7: MBConv6, k3x3  ->  384 ch  (x2)", BLOCK_FILL),
    ("head", "Head: Conv 1x1  ->  1536 ch\nBatchNorm + SiLU", HEAD_FILL),
    ("gap",  "Global Average Pooling", HEAD_FILL),
    ("drop", "Dropout (p=0.3)", HEAD_FILL),
    ("fc",   "Fully Connected  ->  5 classes\nSoftmax (DR 0 .. DR 4)", CLS_FILL),
]


# ---------------------------------------------------------------------------
# Inner panel: one representative MBConv6 block expanded to individual layers,
# using Stage 4 dimensions as the concrete example (input 96 x 32 x 32, 6x
# expansion, depthwise k3x3, SE ratio 0.25, residual output 96 x 32 x 32).
# Each box: "layer_name (LayerType)" over "input: <shape>  ->  output: <shape>".
# ---------------------------------------------------------------------------
CONV_FILL = "#cfe8d8"   # Conv / Linear (same green as outer Stage blocks)
BN_FILL = "#f5f0d0"     # BatchNorm
ACT_FILL = "#f1d5d5"    # Activation
SE_FILL = "#e0e6f5"     # SE sub-block
ADDOUT_FILL = "#fde6cf"  # Add / boundary (input / output)

# (node_id, top_row, bottom_row, fill)
INNER_NODES = [
    ("in",           "in (Input)",
     "output: (1, 96, 32, 32)", ADDOUT_FILL),
    ("conv_pw_exp",  "conv_pw_exp (Conv2d 1x1)",
     "input: (1, 96, 32, 32)  ->  output: (1, 576, 32, 32)", CONV_FILL),
    ("bn1",          "bn1 (BatchNorm2d)",
     "input: (1, 576, 32, 32)  ->  output: (1, 576, 32, 32)", BN_FILL),
    ("act1",         "act1 (SiLU)",
     "input: (1, 576, 32, 32)  ->  output: (1, 576, 32, 32)", ACT_FILL),
    ("conv_dw",      "conv_dw (Conv2d 3x3 depthwise)",
     "input: (1, 576, 32, 32)  ->  output: (1, 576, 32, 32)", CONV_FILL),
    ("bn2",          "bn2 (BatchNorm2d)",
     "input: (1, 576, 32, 32)  ->  output: (1, 576, 32, 32)", BN_FILL),
    ("act2",         "act2 (SiLU)",
     "input: (1, 576, 32, 32)  ->  output: (1, 576, 32, 32)", ACT_FILL),
    ("se_pool",      "se_pool (AdaptiveAvgPool2d)",
     "input: (1, 576, 32, 32)  ->  output: (1, 576, 1, 1)", SE_FILL),
    ("se_fc1",       "se_fc1 (Conv2d 1x1)",
     "input: (1, 576, 1, 1)  ->  output: (1, 24, 1, 1)", SE_FILL),
    ("se_act",       "se_act (SiLU)",
     "input: (1, 24, 1, 1)  ->  output: (1, 24, 1, 1)", SE_FILL),
    ("se_fc2",       "se_fc2 (Conv2d 1x1)",
     "input: (1, 24, 1, 1)  ->  output: (1, 576, 1, 1)", SE_FILL),
    ("se_gate",      "se_gate (Sigmoid)",
     "input: (1, 576, 1, 1)  ->  output: (1, 576, 1, 1)", SE_FILL),
    ("se_mul",       "se_mul (Mul, channel scale)",
     "input: (1, 576, 32, 32) x (1, 576, 1, 1)  ->  output: (1, 576, 32, 32)", SE_FILL),
    ("conv_pw_proj", "conv_pw_proj (Conv2d 1x1)",
     "input: (1, 576, 32, 32)  ->  output: (1, 96, 32, 32)", CONV_FILL),
    ("bn3",          "bn3 (BatchNorm2d)",
     "input: (1, 96, 32, 32)  ->  output: (1, 96, 32, 32)", BN_FILL),
    ("drop_path",    "drop_path (StochasticDepth, p=0.10)",
     "input: (1, 96, 32, 32)  ->  output: (1, 96, 32, 32)", ADDOUT_FILL),
    ("add",          "add (Residual Add)",
     "input: (1, 96, 32, 32) + (1, 96, 32, 32)  ->  output: (1, 96, 32, 32)", ADDOUT_FILL),
    ("out",          "out (Output)",
     "output: (1, 96, 32, 32)", ADDOUT_FILL),
]

# Folded layout: each panel's flow is split into two side-by-side sub-columns,
# so the figure reads as two columns (the second continues the first) and is far
# less tall than a single vertical chain.
ARCH_BY_ID = {nid: (label, fill) for nid, label, fill in ARCH_NODES}
INNER_BY_ID = {nid: (top, bottom, fill) for nid, top, bottom, fill in INNER_NODES}

# Outer architecture split (13 nodes -> 7 + 6).
OUTER_A = ["in", "stem", "s1", "s2", "s3", "s4", "s5"]
OUTER_B = ["s6", "s7", "head", "gap", "drop", "fc"]
OUTER_CONT = ("s5", "s6")  # continuation: bottom of column A -> top of column B

# MBConv6 expansion split. Column A keeps expansion + depthwise + the full SE
# branch (ending at se_mul); column B is projection + residual add + output. The
# residual skip spans the whole block, so in column B it is drawn as a small
# "residual skip" marker feeding the Add -- this keeps every edge inside a single
# column instead of crossing between them.
INNER_A = ["in", "conv_pw_exp", "bn1", "act1", "conv_dw", "bn2", "act2",
           "se_pool", "se_fc1", "se_act", "se_fc2", "se_gate", "se_mul"]
INNER_A_TRUNK = [
    ("in", "conv_pw_exp"), ("conv_pw_exp", "bn1"), ("bn1", "act1"),
    ("act1", "conv_dw"), ("conv_dw", "bn2"), ("bn2", "act2"), ("act2", "se_mul"),
]
INNER_A_SE = [
    ("act2", "se_pool"), ("se_pool", "se_fc1"), ("se_fc1", "se_act"),
    ("se_act", "se_fc2"), ("se_fc2", "se_gate"), ("se_gate", "se_mul"),
]
INNER_B = ["conv_pw_proj", "bn3", "drop_path", "add", "out"]
INNER_B_CHAIN = [
    ("conv_pw_proj", "bn3"), ("bn3", "drop_path"), ("drop_path", "add"),
    ("add", "out"),
]
RESID_NODE = ("resid_in", "residual skip (from block input)",
              "(1, 96, 32, 32)", ADDOUT_FILL)
INNER_CONT = ("se_mul", "conv_pw_proj")  # continuation: column A -> column B

LEFT_HEADING = "Outer architecture"
RIGHT_HEADING = "MBConv6 block (zoom-in, Stage 4 dims, Keras plot_model style)"
NOTE_TEXT = (
    "Outer architecture (left) summarizes the seven MBConv stages of "
    "EfficientNet-B3. The MBConv6 block (right) is shown expanded to individual "
    "layers in Keras plot_model style; the same block repeats inside Stages 2 "
    "through 7 with the channel and kernel parameters listed in the left panel. "
    "Each panel is folded into two columns -- the second column (blue arrow) "
    "continues the first."
)


def _base_digraph(graphviz, name: str):
    """A vertical Graphviz digraph with the shared node/edge styling."""
    g = graphviz.Digraph(name, format="png")
    g.attr(rankdir="TB", bgcolor="white", dpi="200")
    g.attr("node", shape="box", style="rounded,filled", fontname="Helvetica",
           fontsize="11", margin="0.20,0.11", penwidth="1.1",
           color="#444444", fontcolor="#1a1a1a")
    g.attr("edge", color="#555555", penwidth="1.2", arrowsize="0.8")
    return g


def _render_outer_half(graphviz, directory: str, name: str, ids: list[str]) -> Path:
    """Render one sub-column of the block-level outer architecture (dpi=200)."""
    g = _base_digraph(graphviz, name)
    g.attr("node", width="3.4", fixedsize="false")
    for nid in ids:
        label, fill = ARCH_BY_ID[nid]
        g.node(nid, label, fillcolor=fill)
    for src, dst in zip(ids, ids[1:]):
        g.edge(src, dst)
    return Path(g.render(filename=name, directory=directory, cleanup=True))


def _render_inner_a(graphviz, directory: str, name: str) -> Path:
    """Render column A of the MBConv6 expansion: expansion + depthwise + SE."""
    g = _base_digraph(graphviz, name)
    for nid in INNER_A:
        top, bottom, fill = INNER_BY_ID[nid]
        g.node(nid, f"{top}\n{bottom}", fillcolor=fill)
    for src, dst in INNER_A_TRUNK:
        g.edge(src, dst)  # solid trunk
    for src, dst in INNER_A_SE:
        g.edge(src, dst, style="dashed", color="#888888", arrowsize="0.7")
    return Path(g.render(filename=name, directory=directory, cleanup=True))


def _render_inner_b(graphviz, directory: str, name: str) -> Path:
    """Render column B of the MBConv6 expansion: projection + residual + output."""
    g = _base_digraph(graphviz, name)
    for nid in INNER_B:
        top, bottom, fill = INNER_BY_ID[nid]
        g.node(nid, f"{top}\n{bottom}", fillcolor=fill)
    rid, rtop, rbottom, rfill = RESID_NODE
    g.node(rid, f"{rtop}\n{rbottom}", fillcolor=rfill)
    for src, dst in INNER_B_CHAIN:
        g.edge(src, dst)  # solid trunk
    g.edge(rid, "add", style="dashed", color="#888888", arrowsize="0.7")
    return Path(g.render(filename=name, directory=directory, cleanup=True))


def _load_font(size_px: int, bold: bool):
    """Load a TrueType font at the given pixel size with robust fallbacks."""
    import os
    from PIL import ImageFont

    names = (["arialbd.ttf", "DejaVuSans-Bold.ttf"] if bold
             else ["arial.ttf", "DejaVuSans.ttf"])
    search_dirs = [r"C:\Windows\Fonts"]
    try:
        import matplotlib
        search_dirs.append(
            os.path.join(os.path.dirname(matplotlib.__file__),
                         "mpl-data", "fonts", "ttf"))
    except Exception:
        pass
    for d in search_dirs:
        for n in names:
            p = os.path.join(d, n)
            if os.path.isfile(p):
                try:
                    return ImageFont.truetype(p, size_px)
                except Exception:
                    pass
    for n in names:
        try:
            return ImageFont.truetype(n, size_px)
        except Exception:
            pass
    return ImageFont.load_default()


def _wrap(text: str, font, max_w: int, draw) -> list[str]:
    """Greedy word-wrap `text` to `max_w` pixels using `font`."""
    lines: list[str] = []
    cur = ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _fold_arrow(draw, x_a, w_a, h_a, x_b, w_b, y_panel, color="#378ADD"):
    """Draw a continuation arrow from the bottom of column A to the top of B."""
    ax = x_a + w_a / 2
    aby = y_panel + h_a          # bottom-centre of column A
    bx = x_b + w_b / 2
    bty = y_panel                # top of column B
    gx = (x_a + w_a + x_b) / 2   # middle of the fold gutter
    pts = [(ax, aby), (ax, aby + 26), (gx, aby + 26),
           (gx, bty - 34), (bx, bty - 34), (bx, bty - 16)]
    draw.line(pts, fill=color, width=5, joint="curve")
    # Arrowhead pointing down into the top of column B.
    draw.polygon([(bx, bty + 4), (bx - 12, bty - 16), (bx + 12, bty - 16)],
                 fill=color)


def _compose_folded(oa_png: Path, ob_png: Path,
                    ia_png: Path, ib_png: Path) -> tuple[int, int]:
    """Compose the four folded sub-columns, headings, and note into one PNG.

    Each panel is folded into two side-by-side sub-columns (A then B). All four
    sub-columns share one uniform scale (so box sizes stay consistent) and are
    top-aligned; a blue arrow marks where column B continues column A.
    """
    from PIL import Image, ImageDraw

    oa = Image.open(oa_png).convert("RGB")
    ob = Image.open(ob_png).convert("RGB")
    ia = Image.open(ia_png).convert("RGB")
    ib = Image.open(ib_png).convert("RGB")

    # Uniform scale so the tallest sub-column meets the target content height.
    target_h = 1850
    tallest = max(oa.height, ob.height, ia.height, ib.height)
    s = target_h / tallest

    def _sc(im):
        return im.resize(
            (max(1, round(im.width * s)), max(1, round(im.height * s))),
            Image.LANCZOS)

    oa, ob, ia, ib = _sc(oa), _sc(ob), _sc(ia), _sc(ib)

    margin = 50
    fold_gut = 95     # gutter between the two sub-columns of one panel
    panel_gut = 150   # gutter between the outer panel and the inner panel
    head_px = round(22 / 72 * 200)   # 22 pt at 200 dpi
    note_px = round(16 / 72 * 200)   # 16 pt at 200 dpi
    head_font = _load_font(head_px, bold=True)
    note_font = _load_font(note_px, bold=False)

    x_oa = margin
    x_ob = x_oa + oa.width + fold_gut
    outer_right = x_ob + ob.width
    x_ia = outer_right + panel_gut
    x_ib = x_ia + ia.width + fold_gut
    canvas_w = x_ib + ib.width + margin
    panels_h = max(oa.height, ob.height, ia.height, ib.height)

    probe = Image.new("RGB", (10, 10), "white")
    pdraw = ImageDraw.Draw(probe)

    outer_block_w = outer_right - x_oa
    inner_block_w = (x_ib + ib.width) - x_ia
    left_lines = _wrap(LEFT_HEADING, head_font, outer_block_w, pdraw)
    right_lines = _wrap(RIGHT_HEADING, head_font, inner_block_w, pdraw)
    head_line_h = head_px + 8
    head_band = max(len(left_lines), len(right_lines)) * head_line_h + 30

    note_lines = _wrap(NOTE_TEXT, note_font, canvas_w - 100, pdraw)
    note_line_h = note_px + 12
    note_band = len(note_lines) * note_line_h + 24

    canvas_h = margin + head_band + panels_h + 28 + note_band + margin
    canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(canvas)

    y_panel = margin + head_band
    canvas.paste(oa, (x_oa, y_panel))
    canvas.paste(ob, (x_ob, y_panel))
    canvas.paste(ia, (x_ia, y_panel))
    canvas.paste(ib, (x_ib, y_panel))

    # Continuation (fold) arrows for each panel.
    _fold_arrow(draw, x_oa, oa.width, oa.height, x_ob, ob.width, y_panel)
    _fold_arrow(draw, x_ia, ia.width, ia.height, x_ib, ib.width, y_panel)

    # Faint divider between the outer panel and the inner panel.
    div_x = outer_right + panel_gut / 2
    draw.line([(div_x, y_panel - 10), (div_x, y_panel + panels_h + 10)],
              fill="#cccccc", width=2)

    def _draw_block(lines, cx, top_y, font, line_h):
        y = top_y
        for line in lines:
            w = draw.textlength(line, font=font)
            draw.text((cx - w / 2, y), line, font=font, fill="#1a1a1a")
            y += line_h

    left_top = margin + (head_band - len(left_lines) * head_line_h) // 2
    right_top = margin + (head_band - len(right_lines) * head_line_h) // 2
    _draw_block(left_lines, (x_oa + outer_right) / 2, left_top,
                head_font, head_line_h)
    _draw_block(right_lines, (x_ia + x_ib + ib.width) / 2, right_top,
                head_font, head_line_h)

    _draw_block(note_lines, canvas_w / 2, y_panel + panels_h + 28,
                note_font, note_line_h)

    # Clamp to the allowed envelope (<= 4000 px in either dimension).
    max_dim = max(canvas.width, canvas.height)
    if max_dim > 4000:
        scale = 4000 / max_dim
        canvas = canvas.resize(
            (round(canvas.width * scale), round(canvas.height * scale)),
            Image.LANCZOS)

    OUTPUT_GRAPH.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT_GRAPH)
    return canvas.width, canvas.height


def render_graph(model=None) -> None:
    """Render the hybrid two-panel EfficientNet-B3 figure (Graphviz + Pillow)."""
    import tempfile

    try:
        import graphviz  # type: ignore
    except Exception as exc:
        print(f"[warn] graphviz unavailable ({exc}); skipping graph render.")
        if model is not None:
            export_onnx(model)
        return

    try:
        with tempfile.TemporaryDirectory() as tmp:
            oa = _render_outer_half(graphviz, tmp, "fig6_outer_a", OUTER_A)
            ob = _render_outer_half(graphviz, tmp, "fig6_outer_b", OUTER_B)
            ia = _render_inner_a(graphviz, tmp, "fig6_inner_a")
            ib = _render_inner_b(graphviz, tmp, "fig6_inner_b")
            w, h = _compose_folded(oa, ob, ia, ib)
    except Exception as exc:
        print(f"[warn] folded render failed ({exc}).")
        traceback.print_exc()
        if model is not None:
            export_onnx(model)
        return

    inner_total = len(INNER_NODES) + 1  # + residual-skip marker in column B
    print(f"Saved: {OUTPUT_GRAPH}")
    print(f"fig6 folded (two-column panels): outer {len(ARCH_NODES)} nodes "
          f"(7+6), inner {inner_total} nodes (13+6), canvas {w}x{h} px")


def export_onnx(model) -> None:
    """ONNX fallback for users without graphviz. Open with https://netron.app."""
    import torch

    OUTPUT_ONNX.parent.mkdir(parents=True, exist_ok=True)
    x = torch.zeros(INPUT_SHAPE)
    try:
        torch.onnx.export(
            model,
            x,
            str(OUTPUT_ONNX),
            input_names=["input"],
            output_names=["logits"],
            opset_version=14,
            dynamic_axes={"input": {0: "batch"}, "logits": {0: "batch"}},
        )
        print(f"Saved: {OUTPUT_ONNX}  (open in https://netron.app)")
    except Exception as exc:
        print(f"[warn] ONNX export failed: {exc}")
        traceback.print_exc()


def main() -> None:
    # The architecture diagram is self-contained and does not require the heavy
    # model build, so render it first.
    render_graph()

    # Preserve the existing textual summary; only (re)generate it when missing,
    # so a transient model/torchinfo issue never clobbers a good summary file.
    if OUTPUT_SUMMARY.exists():
        print(f"Kept existing summary: {OUTPUT_SUMMARY}")
        return
    try:
        model = build_model()
        write_summary(model)
    except Exception as exc:
        print(f"[warn] textual summary skipped ({exc}).")


if __name__ == "__main__":
    main()
