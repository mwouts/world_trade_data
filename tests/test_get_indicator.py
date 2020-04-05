import pytest
import requests
import pandas as pd
from world_trade_data import get_indicator, get_indicators


def test_get_indicators():
    df = get_indicators()
    assert isinstance(df, pd.DataFrame)
    assert len(df.index)
    assert 'TRD-CMPLMNTRTY-NDX' in df.index


@pytest.mark.parametrize('indicator', ['MPRT-TRD-VL', 'XPRT-TRD-VL', 'WRLD-GRWTH'])
def test_get_indicator(indicator):
    df = get_indicator(indicator, 'usa')
    assert isinstance(df, pd.DataFrame)
    assert len(df.index)


def test_error_on_wrong_indicator(indicator='INCORRECT'):
    with pytest.raises(requests.exceptions.RequestException, match='http://wits.worldbank.org'):
        get_indicator(indicator, 'usa')


def test_error_on_wrong_partner(indicator='NMBR-XPRT-PRTNR'):
    with pytest.raises(requests.exceptions.RequestException, match='http://wits.worldbank.org'):
        get_indicator(indicator, 'usa')


@pytest.mark.parametrize('indicator', get_indicators().query('SDMX_partnervalue==""').index)
def test_get_all_indicators(indicator):
    if indicator == 'TRD-CMPLMNTRTY-NDX':
        pytest.xfail('TRD-CMPLMNTRTY-NDX is not available - cf. https://github.com/mwouts/world_trade_data/issues/1')
    df = get_indicator(indicator, 'usa')
    assert isinstance(df, pd.DataFrame)
    assert len(df.index)


@pytest.mark.parametrize('indicator', get_indicators().query('SDMX_partnervalue=="999"').index)
def test_get_all_indicators_no_partner(indicator):
    df = get_indicator(indicator, 'usa', partner='999')
    assert isinstance(df, pd.DataFrame)
    assert len(df.index)
