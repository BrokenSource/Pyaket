---
icon: octicons/versions-16
---

Pyaket is not the first project solving the packaging problem. Many alternatives out there served as inspiration for the design choices and features of the project, but ultimately none solved my needs and requirements. Here's my thoughts, differences and similarities on each of them - feel free to reach out if any feature has been added solving any of these and/or I'm wrong.

<!-- Ordered by how much each item blocked my usage of it -->
:material-arrow-right: Items are generally ordered by how much each blocked or limited my usage.

<sup><b>Note</b>: My intention is **not** to discredit others, but something similar to literature review in academic papers. These are my subjective opinions and experiences, if anything, to contribute back ideas for improvements.</sup>

## [PyApp](https://github.com/ofek/pyapp)

Hands down the most similar solution and major source of inspiration used up until [v0.8](https://github.com/BrokenSource/DepthFlow/releases/tag/v0.8.0) of my projects. Mostly decided to write my own from scratch as many opinionated and idiosyncratic changes I needed were extremely unlikely to be accepted upstream; I had a fork implementing some of them, but it felt cheesy using that much external work for my branding and selling files.

- Expects a single project wheel or pypi dependency, bad monorepo integration and support.
- No safety against partial installs: Instructing Windows users how to open a powershell in a directory, then typing executable name plus `self restore` is annoying to say the least.
- Variable naming schemes are confusing at times, tries to support everything and nothing at the same time, better to limit the scope, have sane defaults, go all in pip or uv exclusively.
- Some critical options aren't configurable, such as the installation's root directory.
- No version management, removing unused previous installations, etc.

## [PyInstaller](https://github.com/pyinstaller/pyinstaller)

- A `--onefile` executable needs to fully unpack itself to the system temp directory each run, not only being slow but wearing out SSDs quickly
- Compatibility is generally nice, but packages needing to bundle shared libraries are often a huge problem with unecessarily complex build hooks passing the hot potato around.
- Attempts to bundle a whole virtual environment with a python interpreter, may have issues with platform executable sizes hard limits when including pytorch.
- Doesn't utilizes a shared cache for wheels as installs don't go through a pip-like tool.


## [Nuitka](https://github.com/nuitka/nuitka)

Amazing how it works at all

- Generating C code is very slow on a single python thread and might diverge from cpython.
- Compatibility issues with many packages, especially ones with C extensions. Requires many hooks to bundle shared libraries, of which may not be compatible with all user systems.
