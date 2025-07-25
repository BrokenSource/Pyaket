import runpy
from pathlib import Path

from hatchling.metadata.plugin.interface import MetadataHookInterface

# This also detects if running in standalone mode!
for path in (cwd := Path.cwd(), *cwd.parents):
    if (hook := (path/"broken"/"hook.py")).exists():
        globals().update(runpy.run_path(hook))
        break
else:
    class DummyHook(MetadataHookInterface):
        def update(self, metadata: dict):
            metadata["version"] = "0.0.0"
