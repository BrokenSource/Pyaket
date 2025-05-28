
Pyaket is not the first project solving the packaging problem. Many alternatives out there served as inspiration for the design choices and features of the project, but ultimately none solved my needs and requirements. Here's my thoughts, differences and similarities on each of them - feel free to reach me out if I'm wrong and/or a feature has been added solving any of these!

<sup><b>Note</b>: My intention is **not** to discredit or belittle others, rather similar to literature review in academic papers. These are my subjective opinions and experiences, if anything to contribute back ideas and feedback.</sup>

### [PyApp](https://github.com/ofek/pyapp)

Hands down the most similar solution and major source of inspiration used up until [v0.8](https://github.com/BrokenSource/DepthFlow/releases/tag/v0.8.0) of my projects. Mostly decided to write my own from scratch as many opinionated and idiosyncratic changes I needed were extremely unlikely to be accepted upstream; I had a fork implementing some of them, but it felt cheesy using that much external work for my branding and selling files.

:material-arrow-right: Some of the issues I had with it, in order of importance, were:

- Expects a single project wheel or pypi dependency, bad monorepo integration and support.
- No safety against partial installs: Instructing Windows users how to open a powershell in a directory, then typing executable name plus `self restore` is annoying to say the least.
- Variable naming schemes are confusing at times, plus there are a lot of them trying to support everything and nothing at the same time, better to limit the scope and sane defaults.
- Some critical options aren't configurable, such as the installation root directory.

### [PyInstaller](https://github.com/pyinstaller/pyinstaller)

- My main problem is that a `--onefile` executable needs to fully unpack itself to the system temp directory each run, not only being slow but wearing out SSDs quite quickly.
- Compatibility is generally nice, but packages needing to bundle shared libraries are often a huge problem

### [Nuitka](https://github.com/nuitka/nuitka)

-
