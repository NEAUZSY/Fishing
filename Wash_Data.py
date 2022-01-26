import csv
import os
import shelve
import re
import numpy as np

# 经度数据由于跨越了格林尼治，故需要两个范围
Longitude_Range = list(range(350, 360)) + list(range(0, 5))
# 纬度范围要用91减去北纬经度范围的道数据中的行号
Latitude_Range = list(range(26, 36))
# 读写数据所用根路径
WR_ROOT = './Intermediate data/'

is_interpolation = True


def cat_data():
    root = "./data-txt/"
    file_list = os.listdir(root)
    DATA = []
    for i in range(0, len(file_list)):
        file_dir = root + file_list[i]
        print('正在读取第{0}组数据'.format(i))
        with open(file_dir, "r") as f:  # 打开文件
            while True:
                line = f.readline()
                if not line:
                    break
                DATA.append(line)

    print('读取完毕')
    return DATA


def save_data(DATA, name, key='default'):
    print('开始保存%s数据' % name)
    db = shelve.open(WR_ROOT + name)
    db[key] = DATA
    db.close()
    print('保存%s完毕' % name)


def load_data(name, key='default'):
    print('开始读取%s数据' % name)
    db = shelve.open(WR_ROOT + name)
    DATA = db[key]
    db.close()
    print('读取%s完毕' % name)
    return DATA


def format_data(DATA):
    """获取数据文件中的日期信息,并且抓取特定经纬度范围内的数据"""
    i = 0
    # 初始化温度表 形式为[month][Lat][Lon]
    if is_interpolation:
        temperature_ = np.zeros((int(len(DATA) / 181),
                                 len(Latitude_Range),
                                 len(Lontitude_Inter(Longitude_Range, 1))), dtype='float64')
    else:
        temperature_ = np.zeros((int(len(DATA) / 181),
                                 len(Latitude_Range),
                                 len(Longitude_Range)), dtype='float64')
    while i < len(DATA):
        # i 代表的是年份字段
        title = list(filter(None, DATA[i].split(' ')))
        month = (int(title[2]) - 1870) * 12 + int(title[1]) - 1
        for j in range(0, len(Latitude_Range)):
            # 在固定纬度区间进行遍历
            # temperatures = list(filter(None, DATA[Latitude_Range[j]].split(' ')))
            current_row = i + Latitude_Range[j]
            temperatures = [int(s) for s in re.findall(r'-?\d+', DATA[current_row])]
            # print(len(temperatures))
            for k in range(0, len(Longitude_Range)):
                # 在固定经度区间进行遍历
                temp = temperatures[Longitude_Range[k]]
                if temp == -1000:
                    temperature_[month][j][k] = -5
                elif temp == -32768:
                    temperature_[month][j][k] = 10
                else:
                    temperature_[month][j][k] = temperatures[Longitude_Range[k]] / float(100)
            if is_interpolation:
                temperature_[month][j] = Lontitude_Inter(temperature_[month][j][0:len(Longitude_Range)], 1)
            # else:
            #     temperature_[month][j] = temperature_[month][j][0:len(Longitude_Range)]

            # print('已经处理完第 %s 行了' % current_row)
        # print(temperature)
        # print('已经处理完 %s 个月了' % month)
        i += 181
    return temperature_


# def save_as_csv(data):
#     new_item_csv = 'datas'
#     with open('{}.csv'.format(new_item_csv), 'w', encoding='utf-8', newline='') as f:
#         writer = csv.writer(f, dialect='excel')
#         for item in data:
#             writer.writerow(item)
#     print('保存完毕')

def Lontitude_Inter(DATA, density=1):
    """
    对已有数据进行插值
    :param DATA:
    :param density: 差值密度，即两个数据间插入几个数据，默认为1
    :return: 经过插值的数据
    """
    x = np.arange(1 / float(density + 1), len(DATA), 1 / float(density + 1))
    xp = np.array(range(len(DATA)))
    fp = DATA
    return np.interp(x, xp, fp)


# def Latitude_Inter(DATA, density=1):
#     """
#     在纬度数据间进行插值
#     :return:
#     """
#     shapes = list(DATA.shape)
#     shapes[1] = (shapes[1] - 1) * (density + 1) + 1
#     shape = tuple(shapes)
#     TEMPER = np.empty(shape=shape)
#     for month, month_data in enumerate(DATA):
#         for lat in range(0, len(month_data) - 1):
#             x_ = month_data[lat]
#             y_ = month_data[lat + 1]
#             for k, (i, j) in enumerate(np.nditer([x_, y_])):
#                 TEMPER[month][lat] = np.linspace(i, j, num=density)
#         print('已经处理完第 %s 行了' % month)
#     return TEMPER


def Latitude_Inter(DATA, density=1):
    """
    在纬度数据间进行插值
    :return:
    """
    print('开始进行纬度维插值，在数据间插入%d个点' % density)
    shapes = list(DATA.shape)
    # 求出插值后月矩阵的行数
    shapes[1] = (shapes[1] - 1) * (density + 1) + 1
    shape = tuple(shapes)
    TEMPER = np.empty(shape=shape)
    for month, month_data in enumerate(DATA):
        lat_new = 0
        lat_last = 0
        while lat_last < len(month_data) - 1:
            x_ = month_data[lat_last]
            y_ = month_data[lat_last + 1]
            temp = np.empty(shape=(len(month_data[lat_last]), density + 1))
            for k, (i, j) in enumerate(np.nditer([x_, y_])):
                temp[k, :] = np.linspace(i, j, num=density + 1)
            TEMPER[month][lat_new: lat_new + density + 1] = temp.T
            lat_new += density + 1
            lat_last += 1
        # print('已经处理完第 %s 行了' % month)
    print('完成了纬度间插值')
    # 结尾由于插值建立了一个恒为0的数据，此处需要去掉
    return TEMPER[:, :-1, :]


def main():
    datas = cat_data()
    save_data(datas, 'Whole_data_txt', 'default')
    #
    temperature = load_data('Whole_data_txt')
    temperature = format_data(temperature)
    if is_interpolation:
        save_data(temperature, 'Temperature_3_Dimension_InterDensity{0}'.format(1))
    else:
        save_data(temperature, 'Temperature_3_Dimension')

    temperature = load_data('Temperature_3_Dimension_InterDensity1')
    temperature = Latitude_Inter(temperature, density=2)
    save_data(temperature, 'Two_dimensional_interpolation')
    temperature = load_data('Two_dimensional_interpolation')


if __name__ == '__main__':
    main()
    # print(temperature[0])
