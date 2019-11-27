import numpy as np
from world_trade_data import get_indicator


def test_single_product_world_vs_regions():
    imports_from_world = get_indicator('MPRT-TRD-VL', reporter='usa', partner='world', product='fuels')
    imports_from_regions = get_indicator('MPRT-TRD-VL', reporter='usa', partner='regions', product='fuels')

    assert len(imports_from_world.index) == 1
    assert len(imports_from_regions.index) > 1
    assert np.isclose(imports_from_regions.Value.sum(), imports_from_world.Value.sum(), rtol=1e-3)


def test_single_product_world_vs_countries():
    imports_from_world = get_indicator('MPRT-TRD-VL', reporter='usa', partner='world', product='fuels')
    imports_from_countries = get_indicator('MPRT-TRD-VL', reporter='usa', partner='countries', product='fuels')

    assert len(imports_from_world.index) == 1
    assert len(imports_from_countries.index) > 1
    assert np.isclose(imports_from_countries.Value.sum(), imports_from_world.Value.sum(), rtol=1e-3)


def test_total_world_vs_regions():
    imports_from_world = get_indicator('MPRT-TRD-VL', reporter='usa', partner='world', product='total')
    imports_from_regions = get_indicator('MPRT-TRD-VL', reporter='usa', partner='regions', product='total')

    assert len(imports_from_world.index) == 1
    assert len(imports_from_regions.index) > 1
    assert np.isclose(imports_from_regions.Value.sum(), imports_from_world.Value.sum(), rtol=0.02)


def test_total_product_world_vs_countries():
    imports_from_world = get_indicator('MPRT-TRD-VL', reporter='usa', partner='world', product='total')
    imports_from_countries = get_indicator('MPRT-TRD-VL', reporter='usa', partner='countries', product='total')

    assert len(imports_from_world.index) == 1
    assert len(imports_from_countries.index) > 1
    assert np.isclose(imports_from_countries.Value.sum(), imports_from_world.Value.sum(), rtol=1e-3)


def test_total_vs_sectors():
    imports_total = get_indicator('MPRT-TRD-VL', reporter='usa', partner='world', product='total')
    imports_by_sector = get_indicator('MPRT-TRD-VL', reporter='usa', partner='world', product='sectors')

    assert len(imports_total.index) == 1
    assert len(imports_by_sector.index) > 1
    assert np.isclose(imports_by_sector.Value.sum(), imports_total.Value.sum(), rtol=0.0)
