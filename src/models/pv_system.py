# Tide Langner
# 18 August 2025
# Groups modules into a string/system

from pvlib.pvsystem import PVSystem

def scale_modules(mpp, modules_per_string=5, strings_per_inverter=1):
    """Scale a single module MPP to a string/system."""
    system = PVSystem(modules_per_string=modules_per_string,
                      strings_per_inverter=strings_per_inverter)
    return system.scale_voltage_current_power(mpp)
