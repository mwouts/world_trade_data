# All Countries

```python
%load_ext autoreload
%autoreload 2
```

```python
import world_bank_data.wits as wits
```

```python
wits.get_countries()
```

```python
wits.get_countries(datasource='tradestats-tariff')
```

```python
wits.get_countries(datasource='tradestats-trade')
```

```python
wits.get_countries(datasource='tradestats-trade').loc['AUS']
```

# Nomenclature

```python
wits.get_nomenclatures()
```

```python
wits.get_nomenclatures(datasource='tradestats-tariff')
```

```python
wits.get_nomenclatures(datasource='tradestats-trade')
```

# Products

```python
wits.get_products()
```

```python
wits.get_products(datasource='tradestats-tariff')
```

```python
wits.get_products(datasource='tradestats-trade')
```

# Indicators

```python
wits.get_indicators(datasource='tradestats-tariff')
```

```python
wits.get_indicators(datasource='tradestats-trade')
```

```python
idx = wits.get_indicators(datasource='tradestats-trade')
idx.loc[idx['name'].apply(lambda s: 'US$' in s)]
```

```python
idx.loc[idx['name'].apply(lambda s: 'US$' in s)].definition.to_dict()
```

```python

```

# Data availability

```python
df = wits.get_dataavailability()
df
```

```python
df.loc[('EUN', '2017')]
```

```python
df = wits.get_dataavailability(datasource='tradestats-tariff')
df
```

```python
df.loc[('AUS', '2017')]
```

```python
df = wits.get_dataavailability(datasource='tradestats-trade')
df
```

```python
df.loc[('FRA', '2017')]
```

# Tariff Data

## Reported

```python
df = wits.get_tariff_reported(reporter='840', partner='all', product='010129')
df
```

## Estimated

```python
df = wits.get_tariff_estimated(reporter='840', partner='000', product='010130')
df
```

# Get Indicator

```python
df = wits.get_indicator(reporter='usa', 
                        year='2017', 
                        partner='all',
                        product='all',
                        indicator='MPRT-TRD-VL', 
                        datasource='tradestats-trade')
df
```

```python
df.groupby('Partner').Value.sum().sort_values(ascending=False)
```

```python
df.groupby('ProductCode').Value.sum().sort_values(ascending=False)
```

```python
prd = wits.get_products(datasource='tradestats-trade')
```

```python
prd
```

# SDMX

http://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/wbg_wits/

http://wits.worldbank.org/API/V1/SDMX/V21/rest/codelist/all/

http://wits.worldbank.org/API/V1/SDMX/V21/rest/datastructure/WBG_WITS/TARIFF_TRAINS/


