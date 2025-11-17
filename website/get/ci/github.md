---
icon: material/github
---

# GitHub

!!! example "Experimental"
    Developer experience is yet to be improved and polished

Create a workflow in your repository:

```yaml title=".github/workflows/pyaket.yml"
name: Make executables

on:
  workflow_dispatch:
    inputs:
      release:
        description: "Create a release"
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Setup pyaket
        uses: BrokenSource/Pyaket@main

      # Todo: Finish and test
```
