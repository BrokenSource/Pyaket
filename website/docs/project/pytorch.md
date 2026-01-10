---
icon: material/robot
---

# PyTorch

This section covers [PyTorch](https://pytorch.org/) configuration for ML and AI projects.

- **Note**: Will be installed before others, to avoid using a platform default in the dependencies. Pip should skip ok, unless you specify `x.y.z==flavor`, which overrides it.

- **Warn**: Version 2.7.0+ with cu128 or newer is required for RTX 5000+ series! [[1]](https://en.wikipedia.org/wiki/CUDA#GPUs_supported)


## Version

An optional version of PyTorch to be installed at runtime.

=== ":simple-python: Python"
    ```python
    project.torch.version = "2.8.0"
    ```

=== ":simple-toml: Toml"
    ```toml
    [torch]
    version = "2.8.0"
    ```

Torchaudio and torchvision will also be installed under any compatible version.

<hr>

## Backend

The hardware acceleration backend to use.

=== ":simple-python: Python"
    ```python
    project.torch.backend = "auto"
    ```

=== ":simple-toml: Toml"
    ```toml
    [torch]
    backend = "auto"
    ```

- When set to auto, uv will decide the best one ([experimental](https://docs.astral.sh/uv/guides/integration/pytorch/#automatic-backend-selection))
- Other values will be passed to the `--extra-index-url` as:

```sh
uv pip install torch==${VERSION}$+${BACKEND}
    --extra-index-url https://download.pytorch.org/whl/${BACKEND}
```

The allowed values depends on the PyTorch version. You can check [this page](https://pytorch.org/get-started/locally/) for the latest values, and this [other page](https://pytorch.org/get-started/previous-versions/) for older ones. ROCm is for AMD GPUs. Use empty for default.
