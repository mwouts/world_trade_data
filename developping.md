# Developing World Trade Data

The development process follows the [Jupytext repository](https://github.com/jupytext/jupytext):
use Pixi for the editable package and developer tools, pre-commit for formatting
and linting, Pyright for type checking, and pytest for tests. The environment and
tasks are defined in `pyproject.toml`; resolved dependencies are in `pixi.lock`.

## Set up the environment

Install [Pixi](https://pixi.sh/), clone this repository, and run from its root:

```sh
pixi install --locked
pixi run pre-commit install
```

The environment installs `world-trade-data` in editable mode, so changes in
`world_trade_data/` are available immediately. Run commands with `pixi run`, or
use `pixi shell` to activate the environment. Keep changes compatible with the
Python versions declared in `pyproject.toml`; the default Pixi environment tests
only its resolved Python version.

The local `pixi-lock` pre-commit hook invokes Pixi. Commit from `pixi shell` or
use `pixi run git commit` so the hook can find Pixi alongside the developer tools.

## Use the development container

Install VS Code, its Dev Containers extension, and a container engine. Open this
repository and run **Dev Containers: Reopen in Container**. Pixi is installed
inside the container, and the current configuration runs `pixi install` on
creation. VS Code selects `.pixi/envs/default/bin/python`, enables pytest
discovery in `tests/`, and uses Pyright and Ruff.

Run commands through `pixi run` in the container terminal too. Interpreter
selection in VS Code does not activate every terminal command automatically.
After rebuilding or changing environments, verify that VS Code still selects
the Pixi interpreter.

## Run checks

```sh
pixi run test
pixi run lint
pixi run typecheck
pixi run build
```

For a focused change, run its tests and hooks first:

```sh
pixi run pytest tests/test_data.py -k data_to_df
pixi run pre-commit run --files developping.md README.md
```

The fixture conversion command above runs offline. Most other tests contact the
live WITS service and require network access; service outages can affect results.
`tests/test_readme.py` executes `README.md`, creates an ignored `README.ipynb`,
and regenerates the tracked `index.html`. Review that generated diff before
including it in a commit. Do not hand-edit generated output to fix its source.

Lint hooks can modify files. Review their changes and rerun failed hooks before
committing. `pixi run build` creates an sdist and wheel in `dist/`.

## Update dependencies intentionally

Edit dependencies in `pyproject.toml`, then run:

```sh
pixi install
```

Review and commit both `pyproject.toml` and `pixi.lock`. Use `pixi install --locked`
for routine setup so an inconsistent manifest and lockfile fail visibly. Keep
the Pixi versions used in the container and CI compatible with the lockfile.

## Prepare a pull request

Explain the resulting behavior and report the checks that actually ran,
including live-service or container validation limits. Update `CHANGELOG.md`
for user-visible changes. Preserve full commit SHA pins and limited permissions
when changing GitHub Actions. Changes to the container should be verified by
building it and checking the editable import and relevant tests inside it;
running checks on the host alone does not validate the container.
