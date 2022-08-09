import os
import json
import numpy as np
import pytest
from requests import HTTPError
from world_trade_data import get_indicator, get_tariff_reported, get_tariff_estimated
from world_trade_data.data import _wits_data_to_df


def test_get_indicator():
    df = get_indicator(reporter='usa',
                       year='2000',
                       partner='wld',
                       product='fuels',
                       indicator='AHS-SMPL-AVRG',
                       datasource='tradestats-tariff')
    assert len(df.index)


def test_get_indicator2():
    df = get_indicator(reporter='usa',
                       year='2017',
                       partner='wld',
                       product='all',
                       indicator='MPRT-TRD-VL',
                       datasource='tradestats-trade')
    assert len(df.index)


def test_get_tariff_reported():
    df = get_tariff_reported(reporter='840', partner='all', product='970600')
    assert len(df.index) == 1
    assert df.Rate.dtype == np.float64


def test_get_tariff_reported_issue_3():
    df = get_tariff_reported(reporter='840', partner='124', product='all', year='2012')
    assert df.Rate.dtype == np.float64
    assert len(df.index) > 100


def test_get_tariff_estimated():
    df = get_tariff_estimated(reporter='840', partner='000', product='970600')
    assert len(df.index) == 1
    assert df.Rate.dtype == np.float64


def test_get_tariff_estimated_3():
    df = get_tariff_estimated(reporter='840', partner='124', product='all', year='2012')
    assert df.Rate.dtype == np.float64
    assert len(df.index) > 100


def test_tariff_data_to_df():
    current_path = os.path.dirname(__file__)
    sample_file = os.path.join(current_path, 'data', 'sample_tariff_data.json')
    with open(sample_file) as fp:
        data = json.load(fp)
    df = _wits_data_to_df(data, value_name='Rate')
    assert len(df.index) > 1
    assert len(df.columns) > 1


def test_trade_data_to_df():
    current_path = os.path.dirname(__file__)
    sample_file = os.path.join(current_path, 'data', 'sample_trade_data.json')
    with open(sample_file) as fp:
        data = json.load(fp)
    df = _wits_data_to_df(data)
    assert len(df.index) > 1
    assert len(df.columns) > 1


def test_warning_on_request_all_reporter_partner(caplog):
    with pytest.raises(HTTPError, match='Request Entity Too Large'):
        get_indicator(reporter='all',
                      partner='all',
                      year='2017',
                      product='fuels',
                      indicator='MPRT-TRD-VL',
                      datasource='tradestats-trade')
    assert 'Limitation on Data Request' in caplog.text


def test_warning_on_allx3(caplog):
    with pytest.raises(HTTPError, match='Request Entity Too Large'):
        get_indicator(reporter='usa',
                      partner='all',
                      year='all',
                      product='all',
                      indicator='MPRT-TRD-VL',
                      datasource='tradestats-trade')
    assert 'Limitation on Data Request' in caplog.text
