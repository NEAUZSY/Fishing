import numpy as np
from Wash_Data import load_data, save_data


def Init_Fishing_Ground(a, b):
    a, b = a * 3 / 111, b * 3 / 111
    fg = np.empty((a, b))
    return fg


def main():
    temperature = load_data("Two_dimensional_interpolation")
    fg = Init_Fishing_Ground(20, 20)


if __name__ == '__main__':
    main()
