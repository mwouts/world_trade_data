0.1.2 (2026-06-11)
==================

**Changed**
- The project metadata and build configuration were moved to `pyproject.toml`, and the development environment is now managed with [Pixi](https://pixi.sh)
- The continuous integration was migrated from Travis CI to GitHub Actions
- The code is now linted and formatted with [ruff](https://docs.astral.sh/ruff/), through [pre-commit](https://pre-commit.com) hooks
- Versions of Python supported are 3.10 to 3.14
- `world_trade_data.__version__` is now exposed

**Fixed**
- Replaced `pd.np`, removed in pandas 2.0, with `float('nan')` in `data.py` and with `numpy` in the README


0.1.1 (2022-08-15)
==================

**Fixed**
- Fixed an IndexError when calling `wits.get_tariff_reported` ([#3](https://github.com/mwouts/world_trade_data/issues/3))

**Changed**
- Versions of Python supported are 3.6 to 3.10.


0.1.0 (2019-11-25)
==================

Initial release
