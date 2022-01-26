import time

from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import numpy as np
from Wash_Data import load_data
from matplotlib.animation import FuncAnimation


def axis(DATA):
    nrows, ncols = DATA.shape
    x_array = np.zeros((nrows, ncols))
    y_array = np.zeros((nrows, ncols))
    for i in range(0, nrows):
        x_array[i, :] = i

    for i in range(0, ncols):
        y_array[:, i] = i

    return x_array, y_array


def update():
    global step
    ax.set_zlim(-8, 1)
    step += 1
    z_ = temperature[step]
    ax.plot_surface(x, y, z_)
    # ax2.plot_surface(x, y, z_p)
    year = int(step // 12) + 1869
    month = step - 12 * int(step // 12)
    txt = 'Year:{0} Month:{1} Step:{2}'.format(year, month, step)
    ax.set_title(txt)
    # print('Update!')


step = 0
vel = 0.1
# 读取数据文件
temperature = load_data('Gradient')
x, y = axis(temperature[0])
# 获取设置温度数据
z = abs(temperature[step])
fig, ax, = plt.subplots(subplot_kw=dict(projection='3d'))
surf = ax.plot_surface(x, y, z)


def main():
    plt.ion()
    while step <= len(temperature):
        plt.pause(vel)
        plt.cla()
        update()
    # plt.show()


if __name__ == '__main__':
    main()
