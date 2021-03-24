# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

"""d = {'T. Sulfur': 0.0457488,
     'T. Ice': 0.16274024,
     'T. Rock': 0.11266216,
     'Sm. Hadean': 0.00312988,
     'Sm. Ice': 0.00938964,
     'Sm. Rock': 0.05007808,
     'S. Chthonian': 0.00300024,
     'S. Greenhouse': 0.01200096,
     'S. Ammonia': 0.05924988,
     'S. Hadean': 0.01877928,
     'S. Ice': 0.0312988,
     'S. Ocean': 0.11266216,
     'S. Garden': 0.15899976,
     'L. Chthonian': 0.00300024,
     'L. Greenhouse': 0.01200096,
     'L. Ammonia': 0.02699892,
     'L. Ice': 0.00312988,
     'L. Garden': 0.00300024,
     'L. Ocean': 0.00938964,
     'Asteroid B.': 0.16274024}

d = {k: v for k, v in sorted(d.items(), key= lambda item: item[1])}
colors = ['tab:green' if k in ['Large (Ocean)', 'Large (Garden)',
                               'Standard (Garden)', 'Standard (Ocean)'] else
          'tab:blue' for k in d.keys()]
y_pos = np.arange(len(d))
plt.barh(y_pos, d.values())
plt.yticks(y_pos, d.keys())
plt.show()"""
plt.figure(1)
mu = 10.5
sigma = 2.958040
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
plt.subplot(211)
plt.plot(x, stats.norm.pdf(x, mu, sigma))
n_mu = mu / 15
n_sigma = sigma / 15
n_x = np.linspace(n_mu - 3*n_sigma, n_mu + 3*n_sigma, 100)
plt.subplot(212)
plt.plot(n_x, stats.norm.pdf(n_x, n_mu, n_sigma))
plt.show()
