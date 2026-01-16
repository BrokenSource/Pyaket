---
icon: material/github
title: GitHub
status: wip
---

!!! warning "Experimental"
    Untested workflow, yet to be improved and polished.

Create a workflow in your repository:

```yaml title=".github/workflows/pyaket.yml"
name: Make executables

on:
  workflow_dispatch:
    inputs:
      publish:
        type: boolean
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup uv
        uses: astral-sh/setup-uv@v6

      - name: Compile projects
        run: pyaket (...)

      - name: Upload releases
        uses: actions/upload-artifact@v4
        with:
          name: release
          path: release/*

      - name: Get version
        run: echo "VERSION=$(uv version)" >> $GITHUB_ENV

      - name: Create release
        uses: softprops/action-gh-release@v2
        if: ${{inputs.publish}}
        with:
          name: Release v${{env.VERSION}}
          tag_name: v${{env.VERSION}}
          files: release/*
```
