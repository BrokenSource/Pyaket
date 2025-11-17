---
icon: material/torch
---

## PyTorch

This section covers [PyTorch](https://pytorch.org/) configuration for ML and AI projects.

- **Note**: Will be installed before others, to avoid using a platform default in the dependencies. Pip should skip ok, unless you specify `x.y.z==flavor`, which errors out.

- **Warn**: Version 2.7.0+ with cu128 is required for RTX 5000+ series! [[1]](https://en.wikipedia.org/wiki/CUDA#GPUs_supported)

<hr>

### <kbd>PYAKET_TORCH_VERSION</kbd> {#pytorch-version}
> 📦 <b>Type:</b> Version string • <b>Default:</b> None

An optional version of PyTorch to be installed at runtime.

<hr>

### <kbd>PYAKET_TORCH_BACKEND</kbd> {#pytorch-backend}
> 📦 <b>Type:</b> String • <b>Default:</b> auto

The hardware acceleration backend of PyTorch to be installed at runtime.

- When set to auto, uv will decide the best one ([experimental](https://docs.astral.sh/uv/guides/integration/pytorch/#automatic-backend-selection))
- Other values will be passed to the `--extra-index-url` as:

```sh
uv pip install torch==${VERSION}$+${BACKEND}
    --extra-index-url https://download.pytorch.org/whl/${BACKEND}
```

:material-arrow-right: The allowed values depends on the PyTorch version. You can check [this page](https://pytorch.org/get-started/locally/) for the latest values, and this [other page](https://pytorch.org/get-started/previous-versions/) for older ones. ROCm is for AMD GPUs. Use empty for default.
