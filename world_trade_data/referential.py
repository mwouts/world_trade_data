"""Referential: countries, products, indicators..."""

import pandas as pd
import requests
import xmltodict
import world_trade_data.defaults


def true_or_false(value):
    """Replace Yes/No with True/False"""
    if value in {'0', 'Yes'}:
        return True
    if value in {'1', 'No'}:
        return False
    raise ValueError('{} is neither True nor False'.format(value))


def get_referential(name, datasource=world_trade_data.defaults.DEFAULT_DATASOURCE):
    """Return the desired referential"""
    args = ['datasource', datasource, name]
    response = requests.get('http://wits.worldbank.org/API/V1/wits/{}/'.format('/'.join(args)))
    response.raise_for_status()
    data_dict = xmltodict.parse(response.content)

    if 'wits:error' in data_dict:
        if name == 'indicator' and datasource == 'trn':
            msg = "No indicator is available on datasource='trn'. " \
                  "Please use either {}".format(' or '.join("datasource='{}'".format(src)
                                                            for src in world_trade_data.DATASOURCES if
                                                            src != datasource))
        else:
            msg = data_dict['wits:error']['wits:message']['#text']
        raise ValueError(msg)

    def deeper(key, ignore_if_missing=False):
        if key not in data_dict:
            if ignore_if_missing:
                return data_dict
            raise KeyError('{} not in {}'.format(key, data_dict.keys()))
        return data_dict[key]

    if name == 'country':
        level1 = 'countries'
        level2 = name
    elif name == 'dataavailability':
        level1 = name
        level2 = 'reporter'
    else:
        level1 = name + 's'
        level2 = name

    data_dict = deeper('wits:datasource')
    data_dict = deeper('wits:{}'.format(level1))
    data_dict = deeper('wits:{}'.format(level2))

    for obs in data_dict:
        if 'wits:reporternernomenclature' in obs:
            obs['wits:reporternernomenclature'] = obs['wits:reporternernomenclature']['@reporternernomenclaturecode']

    table = pd.DataFrame(data_dict)
    table.columns = [col.replace('@', '').replace('#', '').replace('wits:', '') for col in table.columns]

    for col in table:
        if col == 'notes':
            table[col] = table[col].apply(lambda note: '' if note is None else note)
        if col.startswith('is') and not col.startswith('iso'):
            try:
                table[col] = table[col].apply(true_or_false)
            except ValueError:
                pass

    return table


def get_countries(datasource=world_trade_data.defaults.DEFAULT_DATASOURCE):
    """List of countries for the given datasource"""
    table = get_referential('country', datasource=datasource)
    table = table.set_index('iso3Code')[
        ['name', 'notes', 'countrycode', 'isreporter', 'ispartner', 'isgroup', 'grouptype']]

    return table


def get_nomenclatures(datasource=world_trade_data.defaults.DEFAULT_DATASOURCE):
    """List of nomenclatures for the given datasource"""
    table = get_referential('nomenclature', datasource=datasource)
    return table.set_index('nomenclaturecode')[['text', 'description']]


def get_products(datasource=world_trade_data.defaults.DEFAULT_DATASOURCE):
    """List of products for the given datasource"""
    table = get_referential('product', datasource=datasource)
    return table.set_index('productcode')


def get_dataavailability(datasource=world_trade_data.defaults.DEFAULT_DATASOURCE):
    """Data availability for the given datasource"""
    table = get_referential('dataavailability', datasource=datasource)
    return table.set_index(['iso3Code', 'year']).sort_index()


def get_indicators(datasource=world_trade_data.defaults.DEFAULT_DATASOURCE):
    """List of indicators for the given datasource"""
    table = get_referential('indicator', datasource=datasource)
    return table.set_index(['indicatorcode']).sort_index()
