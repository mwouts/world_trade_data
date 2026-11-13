"""Exercise request construction and parsing without the WITS service."""

import json
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests

from world_trade_data import get_countries, get_indicator, get_tariff_reported
from world_trade_data.data import semicolon_separated_strings
from world_trade_data.referential import true_or_false


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def unexpected_request(*args, **kwargs):
        pytest.fail("Offline tests must mock HTTP requests")

    monkeypatch.setattr(requests.sessions.Session, "request", unexpected_request)


@pytest.mark.parametrize("is_tariff", [False, True])
def test_data_request(monkeypatch, is_tariff):
    sample = "sample_tariff_data.json" if is_tariff else "sample_trade_data.json"
    payload = json.loads((Path(__file__).parent / "data" / sample).read_text())
    response = Mock()
    response.json.return_value = payload
    get = Mock(return_value=response)
    monkeypatch.setattr(requests, "get", get)
    if is_tariff:
        frame = get_tariff_reported("840", name_or_id="id")
        expected = "datasource/trn/reporter/840/partner/000/product/all/year/2017/datatype/reported"
    else:
        frame = get_indicator("MPRT-TRD-VL", "usa", year=[2016, 2017])
        expected = "datasource/tradestats-trade/reporter/usa/year/2016;2017/partner/wld/product/all/indicator/MPRT-TRD-VL"
    assert expected in get.call_args.args[0]
    assert get.call_args.args[0].startswith("https://")
    assert get.call_args.kwargs["timeout"] == 60
    response.raise_for_status.assert_called_once_with()
    assert not frame.empty
    assert frame.Value.dtype == "float64"


def test_http_error(monkeypatch):
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError("unavailable")
    monkeypatch.setattr(requests, "get", Mock(return_value=response))
    with pytest.raises(requests.HTTPError, match="unavailable"):
        get_indicator("MPRT-TRD-VL", "usa")
    response.json.assert_not_called()


def test_countries_request(monkeypatch):
    response = Mock(
        content=b"""<wits:datasource xmlns:wits="urn:wits">
      <wits:countries>
        <wits:country iso3Code="FRA" name="France" countrycode="250"
          isreporter="Yes" ispartner="Yes" isgroup="No" grouptype="" />
        <wits:country iso3Code="USA" name="United States" countrycode="840"
          isreporter="Yes" ispartner="Yes" isgroup="No" grouptype="" />
      </wits:countries>
    </wits:datasource>"""
    )
    # Include the optional notes field as WITS does.
    response.content = response.content.replace(
        b"countrycode=", b'notes="" countrycode='
    )
    monkeypatch.setattr(requests, "get", Mock(return_value=response))
    frame = get_countries()
    assert frame.loc["FRA", "name"] == "France"
    assert frame.loc["USA", "isreporter"]
    assert not frame.loc["FRA", "isgroup"]
    response.raise_for_status.assert_called_once_with()


@pytest.mark.parametrize(
    "value, expected", [("Yes", True), ("0", True), ("No", False), ("1", False)]
)
def test_boolean_values(value, expected):
    assert true_or_false(value) is expected


def test_invalid_boolean():
    with pytest.raises(ValueError):
        true_or_false("maybe")


def test_list_argument():
    assert semicolon_separated_strings([2016, 2017]) == "2016;2017"
