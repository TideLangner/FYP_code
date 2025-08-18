# Tide Langner
# 18 August 2025
# Loads/prepares data
# Runs models (pv_module, pv_string)
# Calls plotting

import os
import pandas as pd
from pvlib.location import Location

from src.analysis.irradiance import compute_effective_irradiance, compute_cell_temperature
from src.models.pv_module import model_manual, model_cec
from src.models.pv_system import scale_modules
from src.plotting.plotting_utils import plot_dc, plot_ac

# :: Setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

start = '2021-01-01 12:00'
end = '2021-01-07 12:00'

location = Location(latitude=-30.09318567206943,
                    longitude=24.13940478600872,
                    tz='Africa/Johannesburg',
                    altitude=1400, name='Kalkbult')

# :: Load POA data
csv_path = os.path.join(DATA_DIR, "processed", "poa_data_2021_io.csv")
poa_data = pd.read_csv(csv_path, index_col=0)
poa_data.index = pd.date_range(start='2021-01-01',
                               periods=len(poa_data.index),
                               freq='h')
poa_data = poa_data[start:end]

# :: Compute irradiance + temp
effective_irradiance = compute_effective_irradiance(poa_data, location, tilt=45, azimuth=0,
                                                    start=start, end=end)
temp_cell = compute_cell_temperature(poa_data)

# :: Method 1 - Manual model
dc_manual = model_manual(effective_irradiance, temp_cell)
plot_dc(dc_manual, "Manual PVWatts DC Output")

''' attempted but failed
# :: Method 2 - CEC model
mpp = model_cec(effective_irradiance, temp_cell, module_key="Jinko Solar Co. Ltd JKM290P-72")
plot_dc(mpp, "CEC Model - 1 Module")

dc_scaled = scale_modules(mpp, modules_per_string=5, strings_per_inverter=1)
plot_dc(dc_scaled, "CEC Model - 5 Modules")
'''
