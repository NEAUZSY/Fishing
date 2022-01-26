import numpy as np
from Wash_Data import load_data, save_data


def Gradient(DATA):
    shape_ = DATA.shape
    shape = (shape_[0], shape_[1] - 1, shape_[2] - 1)
    gradient_ = np.empty(shape, dtype=complex)
    for i, month_data in enumerate(DATA):
        for j in range(0, shape[1]):
            for k in range(0, shape[2]):
                real = month_data[j][k + 1] - month_data[j][k]
                imag = month_data[j + 1][k] - month_data[j][k]
                gradient_[i][j][k] = real + imag * 1j
    return gradient_


def main():
    temperature = load_data("Two_dimensional_interpolation")
    gradient = Gradient(temperature)
    save_data(gradient, 'Gradient')
    save_data(abs(gradient), 'Gradient_abs')


if __name__ == '__main__':
    main()
