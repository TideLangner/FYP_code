# Tide Langner
# 13 August 2025
# PV module according to spec sheet

import pvlib
import pandas as pd
from pvlib.pvsystem import PVSystem

# :: Method 1 - Manual PVWatts DC module
def model_manual(effective_irradiance, temp_cell, p_max=290, gamma_pdc=-0.0047, temp_ref=25):
    """Manual PVWatts DC model for a single module."""
    return pvlib.pvsystem.pvwatts_dc(effective_irradiance, temp_cell,
                                     pdc0=p_max, gamma_pdc=gamma_pdc, temp_ref=temp_ref)

# :: Method 2 - CEC database module
def model_cec(effective_irradiance, temp_cell, module_key):
    """CEC-based single module model."""
    # read csv from GitHub
    cec = pd.read_csv("https://raw.githubusercontent.com/NREL/SAM/refs/heads/develop/deploy/libraries/CEC%20Modules.csv")
    # select row where Name matches module_key
    mod = cec.loc[cec['Name'] == module_key].iloc[0]  # returns a Series for that module

    IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_cec(
        effective_irradiance, temp_cell,
        mod['alpha_sc'], mod['a_ref'], mod['I_L_ref'], mod['I_o_ref'],
        mod['R_sh_ref'], mod['R_s'], mod.get('Adjust', 0)
    )

    return pvlib.pvsystem.max_power_point(IL, I0, Rs, Rsh, nNsVth, method='newton')


'''
# This is the old model 

import os
import pandas as pd
import pvlib
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from scipy.signal import freqs
import matplotlib.pyplot as plt


# :: Method 1 - Manually define module

# electrical parameters
celltype = 'polySi'
p_max = 290
v_mp = 36.4
i_mp = 7.97
v_oc = 44.9
i_sc = 8.89
temp_coeff_pmax = -0.0047       # *p_max # if using pv_watts method
temp_coeff_voc = -0.0040*v_oc   # if using pv_watts method
temp_coeff_isc = 0.0005*i_sc    # if using pv_watts method
cells_in_series = 6*12
temp_ref = 25

# location using pvlib Location function
location = Location(latitude=-30.09318567206943, longitude=24.13940478600872,
                    tz='Africa/Johannesburg',
                    altitude=1400, name='Kalkbult')

# orientation
surface_tilt = 45
surface_azimuth = 0

# analysis duration
start = '2021-01-01 12:00'
end = '2021-01-01 12:00'

# file paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # project root
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_FILE = os.path.join(DATA_DIR, "poa_data_2020_io.csv")

# load POA data
poa_data_2020 = pd.read_csv(CSV_FILE, index_col=0)

# poa_data_2020 = pd.read_csv('poa_data_2020_io.csv', index_col=0)
poa_data_2020.index = pd.date_range(start='2020-01-01',
                                    periods=len(poa_data_2020.index),
                                    freq='h')
poa_data = poa_data_2020[start:end]
# print(poa_data_2020.head())

# solar position throughout time [start:end]
solar_pos = location.get_solarposition(times=pd.date_range(start=start, end=end, freq='h'))

# angle of incidence
aoi = pvlib.irradiance.aoi(surface_tilt, surface_azimuth, solar_pos.apparent_zenith, solar_pos.azimuth)

# incident angle modifier
iam = pvlib.iam.ashrae(aoi)

# effective irradiance
effective_irradiance = poa_data['poa_direct'] * iam + poa_data['poa_diffuse']

# effective temperature on module
temp_cell = pvlib.temperature.faiman(poa_data['poa_global'], poa_data['temp_air'], poa_data['wind_speed'])

# DC output of module at hand
result_dc = pvlib.pvsystem.pvwatts_dc(effective_irradiance, temp_cell,
                                      pdc0=p_max, gamma_pdc=temp_coeff_pmax,
                                      temp_ref=25)

# DC results
result_dc.plot(figsize=(16,8))
plt.title('DC Power')
plt.show()

# AC results
result_ac = pvlib.inverter.pvwatts(pdc=result_dc, pdc0=500,
                                   eta_inv_nom=0.961, eta_inv_ref=0.9637)  # inverter numbers random here

result_ac.plot(figsize=(16,8))
plt.title('AC Power')
plt.show()
'''

'''
# :: Method 2 - CEC module database

# load the CEC module database (bundled with pvlib)
cec = pvlib.pvsystem.retrieve_sam('CECMod')

# find the exact key for the module (print a few candidates to confirm)
candidates = [k for k in cec.columns
              if 'JINKO' in k.upper() and '290' in k and 'P' in k and '72' in k]
# print(candidates)   # e.g. ['Jinko_Solar_JKM290P_72']

# pick the match from the printed list
mod = cec[candidates[0]]

# pull inputs
IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_cec(
    effective_irradiance=effective_irradiance,
    temp_cell=temp_cell,
    alpha_sc=mod['alpha_sc'],
    a_ref=mod['a_ref'],
    I_L_ref=mod['I_L_ref'],
    I_o_ref=mod['I_o_ref'],
    R_sh_ref=mod['R_sh_ref'],
    R_s=mod['R_s'],
    Adjust=mod.get('Adjust', 0)  # some entries may omit Adjust; default 0
)


mpp = pvlib.pvsystem.max_power_point(IL, I0, Rs, Rsh, nNsVth, method='newton')  # DC result 1 module
print(mpp)
mpp.plot(figsize=(16,8))
plt.title('DC Power 1 Module')
plt.show()

# now that we have created the module, we can create the system
system = PVSystem(modules_per_string=5, strings_per_inverter=1)

# DC results when scaled
dc_scaled = system.scale_voltage_current_power(mpp)
dc_scaled.plot(figsize=(16,8))
plt.title('DC Power 5 Modules')
plt.show()

# define inverter from database
cec_inverters = pvlib.pvsystem.retrieve_sam('CECInverter')
inverter = cec_inverters['ABB__PVI_3_0_OUTD_S_US_208V']

# AC results for 1 module
ac_results = pvlib.inverter.sandia(
    v_dc=dc_scaled.v_mp,
    p_dc=dc_scaled.p_mp,
    inverter=inverter
)

# AC results when scaled
ac_scaled = pvlib.inverter.pvwatts(pdc=dc_scaled.p_mp, pdc0=5000,
                                   eta_inv_nom=0.961, eta_inv_ref=0.9637)  # inverter numbers random here
ac_scaled.plot(figsize=(16,8))
# or ac_results.plot(figsize(16,8)) for AC results using inverter from database
plt.title('AC Power')
plt.show()
'''
