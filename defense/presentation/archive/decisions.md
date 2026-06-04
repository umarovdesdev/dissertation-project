# Decisions and Design Notes

Collected decisions from demo preparation discussions.

---

## 1. Monorepo Media Structure

**Decision:** all media stored in `demo/public/pipeline/`.

| Directory | Purpose |
|-----------|---------|
| `thesis/` | Dissertation text, governance docs |
| `experiments/` | Model code, Python, configs |
| `demo/` | All media and visualizations (pipeline images, charts, diagrams) |
| `defense/` | Slides + references to media from demo |

Defense references demo, never duplicates files.

---

## 2. Unified Color Scheme (project-wide)

### Anatomical Markers

| Element | Color | HEX | BGR (OpenCV) | Style |
|---------|-------|-----|-------------|-------|
| OD center + circle | Cyan | `#00E5FF` | `(255, 229, 0)` | circle, 2px stroke |
| Fovea center + circle | Magenta | `#FF2D95` | `(149, 45, 255)` | circle, 2px stroke |

### Axes and Angles

| Element | Color | HEX | BGR (OpenCV) | Style |
|---------|-------|-----|-------------|-------|
| OD-Fovea axis (original) | White | `#FFFFFF` | `(255, 255, 255)` | line, 2px |
| Corrected axis (after rotation) | Lime | `#00FF66` | `(102, 255, 0)` | line, 2px |
| Angle θ arc + label | Lime | `#00FF66` | `(102, 255, 0)` | arc 2px + monospace label |

### Pipeline Stage Markers

| Element | Color | HEX | BGR (OpenCV) | Style |
|---------|-------|-----|-------------|-------|
| FOV boundary / mask | Yellow | `#FFFF00` | `(0, 255, 255)` | circle/contour, 1px dashed |
| Flat-field illumination grid | Gray 50% | `#808080` | `(128, 128, 128)` | grid lines, 1px |
| CLAHE tile grid | Orange | `#FF9800` | `(0, 152, 255)` | grid lines, 1px dashed |

### Grad-CAM / Results

| Element | Color | HEX | Style |
|---------|-------|-----|-------|
| Heatmap colormap | JET | — | cv2.COLORMAP_JET |
| Overlay alpha | — | — | 0.4 blend |
| Predicted class (bar chart) | Lime | `#00FF66` | highlighted bar |
| Other classes (bar chart) | Gray 40% | `#666666` | default bars |

### Text

| Element | Color | HEX | Style |
|---------|-------|-----|-------|
| Labels on dark background | White | `#FFFFFF` | monospace 14-16px, black outline 1px |
| Labels on light background | Black | `#000000` | monospace 14-16px |
| Angle values | Lime | `#00FF66` | monospace, e.g. `θ = −9.1°` |

### What NOT to draw
- OD/Fovea search bounding boxes — debug clutter
- Candidate points — algorithm internals
- Rejected candidates — algorithm internals
- Confidence score text — mention verbally if needed

**Principle:** the committee cares about WHAT the pipeline does, not HOW it searches. Minimal elements, readable in 2 seconds.

### Angle Labels
On rotated images, show two lines:
- Tilted: `θ = −9.1°` (original angle)
- Horizontal: `θ = 0°` (after correction)
