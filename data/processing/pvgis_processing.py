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
tmy = pd.read_csv(raw_csv_path, skiprows=17, nrows=145,
                  usecols=['time(UTC)', 'T2m', 'G(h)', 'Gb(n)', 'Gd(h)', 'WS10m'],
                  index_col=0)

# rename columns
tmy.index = pd.date_range(start='2021-01-01 12:00', end='2021-01-07 12:00', freq='h')
tmy.columns = ['temp_air', 'ghi', 'dni', 'dhi', 'wind_speed']

# plot with subplots stacked vertically
ax = tmy.plot(
    subplots=True,                  # one subplot per column
    layout=(len(tmy.columns), 1),   # arrange in vertical stack
    figsize=(16, 9),
    sharex=True,                    # same x-axis (time)
    legend=True,
)

# improve layout
for a in ax.flatten():
    a.set_ylabel(a.get_title())   # move title to ylabel
    a.set_title("")               # remove default title
    a.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# save processed CSV in processed data directory
processed_csv_path = os.path.join(os.path.dirname(__file__), "..", "processed", "pvlib_kalkbult_2021_01.csv")
tmy.to_csv(processed_csv_path)
