---
icon: material/pin
status: deprecated
---

!!! warning
    This page needs a cleanup/rewrite:

    - Better options are now known, like using lockfiles


It's a good idea to pin all of your wheels dependencies to a specific version for building the executables, to ensure they'll work after any upstream changes.

<!-- Add example of fastapi, transformers updates causing issues -->

When building the wheels of your project, pyaket sets the environment variable `PYAKET_RELEASE` to `1` for detecting whether

## Hatchling

Add a [metadata hook](https://hatch.pypa.io/1.6/plugins/metadata-hook/reference/) in your project like I do with [other projects](https://github.com/BrokenSource/BrokenSource/blob/main/broken/hook.py):

!!! note "**Note**: At least one field must be dynamic to trigger the hook, redefining version is the easiest"

```toml title="<small>pyproject.toml</small>"
[project]
dynamic = ["version"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.metadata.hooks.custom]
path = "hatch_build.py"
```

!!! note "**Note**: Feel free to change where the version is being fetched"

```python title="<small>hatch_build.py</small>"
import os
import runpy
from pathlib import Path

from hatchling.metadata.plugin.interface import MetadataHookInterface


class PyaketHook(MetadataHookInterface):
    def update(self, metadata: dict) -> None:
        repository = Path(__file__).parent

        # Get the version from the main package
        context = runpy.run_path(repository/"package"/"__init__.py")
        version = metadata["version"] = context["__version__"]

        # Trick to replace all list items in place
        def patch(items: list[str]) -> None:
            for (x, item) in enumerate(items):
                if (os.environ.get("PYAKET_RELEASE", "0") == "1"):
                    item = item.replace("~=", "==")
                    item = item.replace(">=", "==")
                items[x] = item

        # Patch all normal and optional dependencies
        list(map(patch, metadata.get("optional-dependencies", {}).values()))
        patch(metadata.get("dependencies", {}))
```

This doesn't _fully_ guarantee a locked environment as dependencies of dependencies might not be pinned. A better way is to send a `uv.lock` file, but it kills iterative development.

:material-arrow-right: **Todo**: Improve and find a method without such drawbacks
