# Development info

## Folder structure

```
docs/ - main documentation
k1lib/ - start of library files
test-envs/ - testing environments, integration tests for all python versions
export.py - after developing in notebooks, run this at the end to export to `.py` files
upload.sh - script to upload to PyPI
```

## Development path

- Open notebook files and change as necessary
- Run preconfigured `./export.py` cell at the end of each notebook to extract to `.py` files
- Run unit/integration/regression tests at `k1lib/tests.ipynb`
- Run tests against multiple Python versions using `test-envs/build.sh`
- Generate docs using `docs/compile.py`
- Commit everything to github
- Commit docs to github (at `~/repos/labs/k1lib.github.io`)
- Push new release to PyPI using `./upload.sh`

## Random notes

So here're some tips so that you can easily develop this further. Not much at the moment, but I just want to note down all of my throughts right away:

- There is an internal settings object at `k1lib._settings`. You can disable bioinformatic tests using it, so that you don't have to install a bunch of dependencies.
