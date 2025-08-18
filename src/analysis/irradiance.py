# Tide Langner
# 18 August 2025
# Computes solar geometry, AOI, IAM, effective irradiance, cell temperature

import pvlib
import pandas as pd

def compute_effective_irradiance(poa_data, location, tilt, azimuth, start, end):
    times = pd.date_range(start=start, end=end, freq='h')
    solar_pos = location.get_solarposition(times=times)
    aoi = pvlib.irradiance.aoi(tilt, azimuth,
                               solar_pos.apparent_zenith,
                               solar_pos.azimuth)
    iam = pvlib.iam.ashrae(aoi)
    return poa_data['poa_direct'] * iam + poa_data['poa_diffuse']

def compute_cell_temperature(poa_data):
    return pvlib.temperature.faiman(
        poa_data['poa_global'],
        poa_data['temp_air'],
        poa_data['wind_speed']
    )