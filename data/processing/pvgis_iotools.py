# Tide Langner
# 12 August 2025
# pull POA data from Europa.eu API and
# create poa_data_2021_io CSV with desired data columns

import os
import pandas as pd
import pvlib

# extract 2021 plane of array data from Europa API
poa_data_2021, meta = pvlib.iotools.get_pvgis_hourly(
    latitude=-30.09318567206943, longitude=24.13940478600872,
    start=2021, end=2021,
    raddatabase='PVGIS-SARAH3', components=True,
    surface_tilt=45, surface_azimuth=180,    # 180 = North for PVGIS
    outputformat='json', usehorizon=True, userhorizon=None,
    pvcalculation=False, peakpower=None, pvtechchoice='crystSi',
    mountingplace='free', loss=0, trackingtype=0,
    optimal_surface_tilt=False, optimalangles=False,
    url='https://re.jrc.ec.europa.eu/api/v5_3/', map_variables=True, timeout=30)


# use this for keeping all columns
poa_data_2021['poa_diffuse'] = poa_data_2021['poa_sky_diffuse'] + poa_data_2021['poa_ground_diffuse']
poa_data_2021['poa_global'] = poa_data_2021['poa_diffuse'] + poa_data_2021['poa_direct']

# extract necessary columns
keep_cols = ['poa_global', 'poa_direct', 'poa_diffuse', 'temp_air', 'wind_speed']
poa_data_2021 = poa_data_2021[keep_cols]

print(poa_data_2021)

# save processed CSV in processed data directory
processed_csv_path = os.path.join(os.path.dirname(__file__), "..", "processed", "poa_data_2021_io.csv")
poa_data_2021.to_csv(processed_csv_path)
