import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from Wash_Data import load_data


def Plot_One_Shot(DATA, Month, Year):
    nrows, ncols = DATA.shape
    x_edges, y_edges = np.mgrid[0:nrows - 1:complex(str(nrows) + 'j'), 0:ncols - 1:complex(str(ncols) + 'j')]
    # x_edges, y_edges = np.mgrid[0:15:16j, 0:9:11j]
    # x_edges, y_edges = np.mgrid[-1:1:21j, -1:1:21j]
    x = (x_edges[:-1, :-1] + np.diff(x_edges[:2, 0])[0] / 2.) / 2 - 5
    y = (y_edges[:-1, :-1] + np.diff(y_edges[0, :2])[0] / 2.) / 2 + 55
    z = DATA
    plt.figure()
    # lims = dict(cmap='RdBu_r', vmin=np.min(z), vmax=np.max(z))
    lims = dict(cmap='RdBu_r', vmin=-6, vmax=10)
    plt.pcolormesh(x_edges, y_edges, z, shading='flat', **lims)
    # plt.xlim((-5, 10))
    # plt.ylim((55, 65))
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    plt.colorbar()
    plt.title("Ocean Temperature  |  Date:{}-{}".format(Year, Month))
    plt.show()


if __name__ == '__main__':
    temperature = load_data('Two_dimensional_interpolation')
    Plot_One_Shot(temperature[1799], 7, 2020)
