"""FastAPI inference server for the DR-Classifier demo.

Imports preprocessing + model code directly from the sibling ``experiments/``
tree (no duplication). The path insert below makes ``import src.*`` resolve to
``experiments/src`` regardless of where uvicorn is launched from.
"""

import sys
from pathlib import Path

EXPERIMENTS_ROOT = Path(__file__).resolve().parents[2] / "experiments"
if str(EXPERIMENTS_ROOT) not in sys.path:
    sys.path.insert(0, str(EXPERIMENTS_ROOT))
