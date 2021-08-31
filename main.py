from threading import Thread

import xlrd
from selenium import webdriver
from time import sleep, ctime


# 读取文件
from selenium.webdriver.support.select import Select


def read_file():
    #  读取文件
    excel = xlrd.open_workbook("test.xls")
    excel.sheet_names()  # 获取excel里的工作表sheet名称数组
    sheet = excel.sheet_by_index(0)  # 根据下标获取对应的sheet表

    # 循环读取数据
    empty_dict = {}
    for i in range(0, sheet.nrows):
        row_list = sheet.row_values(i)  # 每一行的数据在row_list 数组里
        empty_dict.setdefault(i, row_list)
    print(empty_dict)
    return empty_dict


# 浏览器自动化
def test_baidu(index, info):
    print('start: %s' % ctime())
    print(index, info)

    driver = webdriver.Chrome()  # 本机运行
    driver.get('http://www.beidaihe.com.cn/demolregist')
    driver.find_element_by_name('username').send_keys(info[0])
    driver.find_element_by_name('mobile').send_keys(info[1])
    driver.find_element_by_name('password').send_keys(info[2])
    driver.find_element_by_name('confirm_password').send_keys(info[2])
    driver.find_element_by_name('email').send_keys(info[3])

    # 单选框
    driver.find_element_by_xpath("//input[@value='2']").click()
    # 下拉列表(option value值) , 相同option值 , 有可能出错
    driver.find_element_by_xpath("//option[@value='2017']").click()
    driver.find_element_by_xpath("//option[@value='1']").click()
    # 下拉列表 复杂(选择器 , option_value值)
    Select(driver.find_element_by_css_selector("[id='sel_day']")).select_by_value('14')

    #最后一步 提交!
    #driver.find_element_by_id("next").click()

    sleep(360)

    sleep(180)
    driver.close()


if __name__ == '__main__':

    # 定义分布式运行环境
    env = read_file()

    # 定义空线程数组
    threads = []

    # 获取线程数
    print(len(env))
    loops = range(len(env))

    # 创建线程，并追加入线程数组
    for index, info in env.items():
        thread = Thread(target=test_baidu, args=(index, info))
        threads.append(thread)

    # 启动线程
    for i in loops:
        threads[i].start()

    # 守护线程
    for i in loops:
        threads[i].join()

    print('end: %s' % ctime)
