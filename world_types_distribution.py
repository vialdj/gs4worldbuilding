# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

d = {'T. Sulfur': 0.0457488,
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
"""colors = ['tab:green' if k in ['Large (Ocean)', 'Large (Garden)',
                               'Standard (Garden)', 'Standard (Ocean)'] else
          'tab:blue' for k in d.keys()]"""
y_pos = np.arange(len(d))
plt.barh(y_pos, d.values())
plt.yticks(y_pos, d.keys())
plt.show()
