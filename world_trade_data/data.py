"""WITS Data: indicators and tariffs"""

import logging
import warnings

import requests
import pandas as pd
import world_trade_data.defaults

logging.basicConfig()
LOGGER = logging.getLogger(__name__)

LIMITATIONS = """Please read the **Limitation on Data Request** from https://wits.worldbank.org/witsapiintro.aspx

> In order to avoid server overload, request for entire database is not possible in one query.
> The following are the options to request data:
> - Maximum of two dimension with 'All' value is allowed.
> - Data request with All Reporter and All Partners is not allowed.
> - When two of the dimensions have 'All', then rest of the dimension should have a specific value.
> - Trade Stats data for a single reporter, partner, Indicator and product can be requested for a range of years."""

DATASOURCES = ['trn', 'tradestats-trade', 'tradestats-tariff']


def semicolon_separated_strings(value):
    """Turn lists into semicolon separated strings"""
    if isinstance(value, list):
        return ';'.join(semicolon_separated_strings(v) for v in value)
    return str(value)


def get_tariff_reported(reporter,
                        partner='000',
                        product='all',
                        year=world_trade_data.defaults.DEFAULT_YEAR,
                        name_or_id='name'):
    """Tariffs (reported)"""
    return _get_data(reporter, partner, product, year, is_tariff=True,
                     datatype='reported', datasource='trn', name_or_id=name_or_id)


def get_tariff_estimated(reporter,
                         partner='000',
                         product='all',
                         year=world_trade_data.defaults.DEFAULT_YEAR,
                         name_or_id='name'):
    """Tariffs (estimated)"""
    return _get_data(reporter, partner, product, year,  is_tariff=True,
                     datatype='aveestimated', datasource='trn', name_or_id=name_or_id)


def get_indicator(indicator,
                  reporter,
                  partner='wld',
                  product='all',
                  year=world_trade_data.defaults.DEFAULT_YEAR,
                  datasource=world_trade_data.defaults.DEFAULT_DATASOURCE,
                  name_or_id='name'):
    """Get the values for the desired indicator"""
    return _get_data(reporter, partner, product, year,
                     indicator=indicator, datasource=datasource, name_or_id=name_or_id)


def _get_data(reporter, partner, product, year, datasource, name_or_id, is_tariff=False, **kwargs):
    args = {'reporter': reporter,
            'partner': partner,
            'product': product,
            'year': year,
            'datasource': datasource}
    args.update(kwargs)
    list_args = []

    if datasource == 'trn':
        order = ['datasource', 'reporter', 'partner', 'product', 'year']
    else:
        order = ['datasource', 'reporter', 'year', 'partner', 'product']
    for arg in order + list(kwargs.keys()):
        list_args.append(arg)
        list_args.append(semicolon_separated_strings(args[arg]))

    if ('all' in reporter.lower() and 'all' in partner.lower()) or sum(['all' in args[k] for k in args]) >= 3:
        LOGGER.warning(LIMITATIONS)

    response = requests.get('http://wits.worldbank.org/API/V1/SDMX/V21/{}?format=JSON'
                            .format('/'.join(list_args)))
    response.raise_for_status()
    data = response.json()
    df = _wits_data_to_df(data, name_or_id=name_or_id, is_tariff=is_tariff)
    if is_tariff and not len(df):
        warnings.warn("""Did you know? The reporter-partner combination only yields results
 if the two countries have a preferential trade agreement (PTA).
 Otherwise, all other tariffs to all non-PTA countries
 are found if one enters "000" in partner.""")
    return df


def _wits_data_to_df(data, value_name='Value', is_tariff=False, name_or_id='id'):
    observation = data['structure']['attributes']['observation']
    levels = data['structure']['dimensions']['series']
    obs_levels = data['structure']['dimensions']['observation']
    series = data['dataSets'][0]['series']

    index_names = [level['name'] for level in levels] + [obs_level['name'] for obs_level in obs_levels]
    column_names = [value_name] + [o['name'] for o in observation]

    all_observations = {value_name: []}
    for col in index_names:
        all_observations[col] = []
    for col in column_names:
        all_observations[col] = []

    for i in series:
        loc = [int(j) for j in i.split(':')]

        # When loading tariffs, product is at depth 3, but levels say it's at depth 4
        # - So we invert the two levels
        if is_tariff:
            loc[2], loc[3] = loc[3], loc[2]

        observations = series[i]['observations']
        for obs in observations:
            for level, j in zip(levels, loc):
                all_observations[level['name']].append(level['values'][j][name_or_id])

            o_loc = [int(j) for j in obs.split(':')]
            for level, j in zip(obs_levels, o_loc):
                all_observations[level['name']].append(level['values'][j]['name'])

            values = observations[obs]
            all_observations[value_name].append(float(values[0]))
            for obs_ref, value in zip(observation, values[1:]):
                if isinstance(value, int) and len(obs_ref['values']) > value:
                    all_observations[obs_ref['name']].append(obs_ref['values'][value][name_or_id])
                else:
                    all_observations[obs_ref['name']].append(value)

    table = pd.DataFrame(all_observations).set_index(index_names)[column_names]
    for col in ['NomenCode', 'TariffType', 'OBS_VALUE_MEASURE']:
        if col in table:
            table[col] = table[col].astype('category')

    for col in table:
        if '_Rate' in col or 'Lines' in col or col == 'Value':
            table[col] = table[col].apply(lambda s: pd.np.NaN if s == '' else float(s))

    return table
