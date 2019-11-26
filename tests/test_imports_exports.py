import numpy as np
import pandas as pd
from world_trade_data import get_indicator


def test_imports_match_exports():
    """The imports in the USA reported by the USA match, more or less, the exports reported by the other
    countries to the USA"""
    exports_to_usa = get_indicator('XPRT-TRD-VL', reporter='regions', partner='usa', product='fuels')
    usa_imports = get_indicator('MPRT-TRD-VL', reporter='usa', partner='regions', product='fuels')

    usa_imports_by_reporter = pd.DataFrame(
        {'USA': usa_imports.reset_index().set_index('Partner').Value.sort_index(),
         'Others': exports_to_usa.reset_index().set_index('Reporter').Value.sort_index()})
    usa_imports_by_reporter['ratio'] = usa_imports_by_reporter['Others'] / usa_imports_by_reporter['USA']

    assert not usa_imports_by_reporter['ratio'].isnull().any()
    assert np.isclose(usa_imports_by_reporter.loc['North America', 'ratio'], 1.0, 0.01)

    for region in usa_imports_by_reporter.index:
        if 'Asia' in region:
            assert np.isclose(usa_imports_by_reporter.loc[region, 'ratio'], 1.0, 0.2)
