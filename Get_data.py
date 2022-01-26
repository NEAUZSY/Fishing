# -*- codeing = utf-8 -*-
import gzip
import re
import urllib.error
import urllib.request
import requests

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.96 Safari/537.36'}


def askURL(url):
    # 用户代理，告诉豆瓣服务器，我们是什么类型的浏览器，本质上是告诉浏览器我们可以接受什么水平的文件内容
    # 模拟浏览器头部信息，向服务器发送消息

    requests = urllib.request.Request(url, headers=head)
    try:
        response = urllib.request.urlopen(requests)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(e)
    return html


# 创建正则表达式的规则
# find_UrlSrc = re.compile(r'style="vertical-align: inherit;">(.*)</font')
find_UrlSrc = re.compile(r'<a href="(.*)">')


# 爬取网页
def get_data(url):
    img_list = []
    html = askURL(url)  # 保存获取到的网页源码
    # print(html)

    print('开始解析')
    urlsrc = re.findall(find_UrlSrc, html)
    url_list = urlsrc[6:28]
    print('解析结束')
    return url_list


def down_data(src_list):
    print('开始下载数据')
    path = './data/'
    path_txt = "./data-txt/"
    for i in range(0, len(src_list)):
        src = 'https://www.metoffice.gov.uk/hadobs/hadisst/data/' + src_list[i]
        paths = path + src_list[i]
        print('正在下载第{0}组数据'.format(i))
        r = requests.get(src, headers=head)
        print('正在解压第{0}组数据'.format(i))

        f_name = src_list[i].replace(".gz", "")
        g_file = gzip.GzipFile(paths)
        open(path_txt + f_name, "wb+").write(g_file.read())
        g_file.close()

        # 打开imglist中保存的图片网址，并下载图片保存在本地，format格式化字符串
    return 0


def main():
    base_url = 'https://www.metoffice.gov.uk/hadobs/hadisst/data/download.html'
    print('log in')
    data_list = get_data(base_url)
    down_data(data_list)
    print('ok')


if __name__ == '__main__':
    main()
