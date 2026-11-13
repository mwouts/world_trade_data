import pytest

from world_trade_data import (
    DATASOURCES,
    get_countries,
    get_dataavailability,
    get_indicators,
    get_nomenclatures,
    get_products,
)

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("datasource", DATASOURCES)
def test_get_countries(datasource):
    df = get_countries(datasource=datasource)
    if "EUN" in df.index:
        assert df.loc["EUN", "name"] == "European Union"
    else:
        assert df.loc["FRA", "name"] == "France"


@pytest.mark.parametrize("datasource", DATASOURCES)
def test_get_nomenclatures(datasource):
    df = get_nomenclatures(datasource=datasource)
    assert "H0" in df.index


@pytest.mark.parametrize("datasource", DATASOURCES)
def test_get_products(datasource):
    df = get_products(datasource=datasource)
    if datasource == "trn":
        assert any("sculptures" in s for s in df["productdescription"])
    else:
        assert "Textiles" in df.index


@pytest.mark.parametrize("datasource", DATASOURCES)
def test_get_indicators(datasource):
    if datasource == "trn":
        with pytest.raises(
            ValueError, match="No indicator is available on datasource='trn'"
        ):
            get_indicators(datasource=datasource)
    else:
        df = get_indicators(datasource=datasource)
        assert len(df.index)


@pytest.mark.parametrize("datasource", DATASOURCES)
def test_get_dataavailability(datasource):
    df = get_dataavailability(datasource=datasource)
    if "EUN" in df.index.get_level_values(0):
        assert ("EUN", "2017") in df.index
        x = df.loc[("EUN", "2017")]
        assert x.loc["name"] == "European Union"
        assert "000" in x.partnerlist.split(";")
    else:
        assert ("AUS", "2017") in df.index
        x = df.loc[("AUS", "2017")]
        assert x.loc["name"] == "Australia"
        assert x.partnerlist == "All Partners"
