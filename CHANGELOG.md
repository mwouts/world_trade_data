0.1.1 (2022-08-09)
==================

**Fixed**
- Fixed an IndexError when calling `wits.get_tariff_reported` ([#3](https://github.com/mwouts/world_trade_data/issues/3)). Now the `get_tariff_*` functions return a `Rate` rather than a `Value`.

**Changed**
- Versions of Python supported are 3.6 to 3.10.


0.1.0 (2019-11-25)
==================

Initial release
