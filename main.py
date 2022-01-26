import time
import Get_data
import Wash_Data
import Fitting_Temperature_Fun


def Try_Whole_Demo():
    t1 = time.time()
    Get_data.main()
    Wash_Data.main()
    Fitting_Temperature_Fun.main()
    t2 = time.time()
    print('用时: {}秒'.format(t2 - t1))


if __name__ == '__main__':
    Try_Whole_Demo()


