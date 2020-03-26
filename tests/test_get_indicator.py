import pytest
import pandas as pd
from world_trade_data import get_indicator, get_indicators


def test_get_indicators():
    df = get_indicators()
    assert isinstance(df, pd.DataFrame)
    assert len(df.index)
    assert 'TRD-CMPLMNTRTY-NDX' in df.index


@pytest.mark.parametrize('indicator', ['MPRT-TRD-VL', 'XPRT-TRD-VL', 'WRLD_GRWTH', 'TRD-CMPLMNTRTY-NDX'])
def test_get_indicator(indicator):
    df = get_indicator(indicator, 'usa')
    assert isinstance(df, pd.DataFrame)
    assert len(df.index)
