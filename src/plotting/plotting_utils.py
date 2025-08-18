# Tide Langner
# 18 August 2025
# System plotting

import matplotlib.pyplot as plt

def plot_dc(dc_result, title="DC Power"):
    dc_result.plot(figsize=(16,8))
    plt.title(title)
    plt.show()

def plot_ac(ac_result, title="AC Power"):
    ac_result.plot(figsize=(16,8))
    plt.title(title)
    plt.show()
