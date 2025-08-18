# PV Mismatch Loss Simulation Project

## Overview

This project simulates the performance of photovoltaic (PV) systems under various mismatch loss scenarios, including degradation, shading, and bypass diode failures. It uses `pvlib` and `pvmismatch` for modeling and analysis.

## Folder Structure

- **data/processing**: Scripts for cleaning raw data.
- **data/raw**: Raw data.
- **src/models/**: Core classes for PV cells, modules, strings, and systems.
- **src/simulation/**: Scripts for running mismatch loss scenarios.
- **src/analysis/**: Tools for metrics calculation and reporting.
- **src/plotting/**: Plotting utilities for results.
- **tests/**: Unit tests for code validation.
- **initial_system.py**: Example script for basic system setup.
- **requirements.txt**: Python dependencies.

## Getting Started

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the example system:
   ```
   python initial_system.py
   ```
3. Explore and modify scenarios in `simulation/`.

## Customization

- Add new modules or scenarios by extending the classes in `models/` and `simulation/`.
- Place new data files in `data/`.
- Use `analysis/` and `plotting/` for reporting and plotting.

## References

- [pvlib documentation](https://pvlib-python.readthedocs.io/)
- [pvmismatch documentation](https://sunpower.github.io/pvmismatch/)

---

For further details, see the docstrings in each module.