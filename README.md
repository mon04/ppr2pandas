# ppr2pandas

Download Ireland's Property Price Register for data analysis in Python/pandas.

## Examples

### Getting data

```python
from ppr2pandas import ppr

# Get the entire PPR data
df = ppr.get_ppr()

# Filter to a date range
df = ppr.get_ppr(min_date="2024-01-01", max_date="2024-01-31")

# Filter to a price range
df = ppr.get_ppr(min_price=250_000, max_price=350_000)

# Filter by counties
df = ppr.get_ppr(counties=['Dublin', 'Kildare', 'Meath'])
```

Columns are automatically parsed into their relevant [dtypes][1].

```python
df = ppr.get_ppr()

print(df.dtypes)
# Date of Sale (dd/mm/yyyy)    datetime64[ns]
# Address                              object
# County                               object
# Eircode                              object
# Price (€)                           float64
# Not Full Market Price                  bool
# VAT Exclusive                          bool
# Description of Property              object
# Property Size Description            object
# dtype: object
```

### Filtering, selecting, and analyzing data

The pandas DataFrame format provides a powerful API for data manipulation and analysis.

```python
# Filter the dataframe based on conditional expressions
expensive_properties = df[df['Price (€)'] >= 500_000]
dublin_data = df[df['County'] == 'Dublin']

# Select a single column
dub_prices = dublin_data['Price (€)']

print("max:   ", dub_prices.max())
print("min:   ", dub_prices.min())
print("mean:  ", dub_prices.mean())
print("median:", dub_prices.median())
# max:    225000000.0
# min:    5250.0
# mean:   460559.4193276385
# median: 330000.0
```

More information is available in the [pandas documentation][2].

<!-- References -->

[1]: https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html#dtypes

[2]: https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html#how-do-i-filter-specific-rows-from-a-dataframe