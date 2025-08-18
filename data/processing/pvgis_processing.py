# Tide Langner
# 12 August 2025
# extract data from pvgis_kalkbult.csv, clean it and
# create pvlib_kalbult_2021 CSV with desired data columns

import os
import pandas as pd
from matplotlib import pyplot as plt

# raw CSV path relative to this script
raw_csv_path = os.path.join(os.path.dirname(__file__), "..", "raw", "pvgis_kalkbult.csv")

# create a proper datetime index
tmy = pd.read_csv(raw_csv_path, skiprows=17, nrows=8760,
                  usecols=['time(UTC)', 'T2m', 'G(h)', 'Gb(n)', 'Gd(h)', 'WS10m'],
                  index_col=0)

# rename columns
tmy.index = pd.date_range(start='2021-01-01 00:00', end='2021-12-31 23:00', freq='h')

tmy.columns = ['temp_air', 'ghi', 'dni', 'dhi', 'wind_speed']

# print and plot
print(tmy)
tmy.plot(figsize=(16,8))
plt.show()

# save processed CSV in processed data directory
processed_csv_path = os.path.join(os.path.dirname(__file__), "..", "processed", "pvlib_kalkbult_2021.csv")
tmy.to_csv(processed_csv_path)
