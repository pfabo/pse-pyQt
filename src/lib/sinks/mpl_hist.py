# -*- coding: utf-8 -*-
'''
Klient pre komponent MatplotlibPlot.

Načíta dáta zo súboru vo formáte JSON a zobrazí ich. Pre úpravu dát je použitý backend QT4Agg,
umožňuje doplňujúce úpravy dát.

'''
import json
import sys

import matplotlib

# import qt4 version under python2, qt5 under python3
# usual six.PY2 is not used because it might not be installed
if sys.version_info < (3, 0, 0):
    matplotlib.use('QT4Agg')
else:
    matplotlib.use('QT5Agg')

import pylab as plt  # @NoMove


def jsonImport(obj):
    return obj


if len(sys.argv) < 2:
    exit(0)

fileName = sys.argv[1]

f = open(fileName, 'r')
s = f.readline()
f.close()

# dekodovanie dat zo suboru
data = json.loads(s, object_hook=jsonImport)

title = data[0]
x_label = data[1]
y_label = data[2]
grid = data[3]
num_bins = int(data[4])
y_data = data[5]


if title != '':
    plt.title(title)

if x_label != '':
    plt.xlabel(x_label)

if y_label != '':
    plt.ylabel(y_label)

if grid == 'True':
    plt.grid()

if num_bins <= 0:
    num_bins = 50

n, bins, patches = plt.hist(y_data, num_bins, normed=1, facecolor='green', alpha=0.5)
plt.show()
