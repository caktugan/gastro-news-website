"""Test bootstrap: the scripts import their shared helpers by bare name
(`from pipeline_common import …`) because they run as plain files, not as a
package. Tests import them as `scripts.<name>`, so the scripts directory must
also be importable directly."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
