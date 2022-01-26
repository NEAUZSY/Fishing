import numpy as np
from scipy.optimize import leastsq
from Wash_Data import save_data, load_data
from Plot_one_shot import Plot_One_Shot


def init_variable():
    """初始化需要优化的参数"""
    p0 = np.array([0, 0, 0, 0, 0, 0, 0, 0])
    return p0


def func(P, Y, X):
    """
    数据拟合所用的函数: 四元二次函数
    """
    x, y, m, year = X
    A = P[0] * x ** 2 + P[1] * x
    B = P[2] * y ** 2 + P[3] * y
    C = -P[4] * (m - 5) ** 2 + P[5] * m
    D = P[6] * year
    y = A + B + C + D # + P[7]
    return Y - y


def init_data(DATA):
    x_ = []
    y_ = []
    month_ = []
    years_ = []
    temper_ = []
    for i, Month in enumerate(DATA):
        year = i // 12 + 1870
        for j, Lat in enumerate(Month):
            for k in range(0, len(Lat)):
                x_.append(k)
                y_.append(j)
                month_.append(i)
                years_.append(year)
                temper_.append(Lat[k])
    x_ = np.array(x_, dtype='float64').reshape(1418796)
    y_ = np.array(y_, dtype='float64').reshape(1418796)
    month_ = np.array(month_, dtype='float64').reshape(1418796)
    years_ = np.array(years_, dtype='float64').reshape(1418796)
    temper_ = np.array(temper_, dtype='float64').reshape(1418796)
    return x_, y_, month_, years_, temper_


def optimization(DATA):
    x, y, month, year, temperature = init_data(DATA)
    X = x, y, month, year
    p0 = init_variable()
    result_p = leastsq(func, p0, args=(temperature, X))[0]
    print(u"拟合参数", result_p)  # 实验数据拟合后的参数
    print('#=====海洋温度方程为=====#')
    print("F(x, y, Month, Year) = "
          "{0} x^2 + {1} x + "
          "{2} y^2 + {3} y + "
          "{4} Month^2 + {5} Month + "
          "{6} Year + {7}".format(result_p[0],
                                  result_p[1],
                                  result_p[2],
                                  result_p[3],
                                  result_p[4],
                                  result_p[5],
                                  result_p[6],
                                  result_p[7]))
    return result_p


def verification(fun_var, Month, Year):
    x, y = np.mgrid[0:26:27j, 0:28:29j]
    month = np.array([Month] * 27 * 29).reshape([27, 29])
    year = np.array([Year] * 27 * 29).reshape([27, 29])
    z = - func(fun_var, 0, (x, y, month, year))
    return z


def main():
    temperatures = load_data('Two_dimensional_interpolation')
    var = optimization(temperatures)

    save_data(var, "Ocean_equation_parameters")
    var = load_data("Ocean_equation_parameters")
    temperature = verification(var, 6, 899)
    Plot_One_Shot(temperature, 7, 1945)
    print(var)


if __name__ == '__main__':
    main()


