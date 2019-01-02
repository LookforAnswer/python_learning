import urllib.request
from lxml import etree

def get_one_page(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')


def parse_one_page(html, base_path):

    html = etree.HTML(html)

    # 匹配最外层 DIV
    items = html.xpath('//div[@class="sse_common_wrap_cn"]')

    count = 0
    result_array = []
    for item in items:

        if count > 3:
            break

        # 定义一个字典对象
        result = {'title': '', 'data': {}}

        # 获取类别名称
        result['title'] = item.xpath('child::div//h2/text()')[0].replace('\n', '')

        # 获取content信息
        content_result = []
        dd_node = item.xpath('child::div//div[@class="sse_list_1"]//dd')
        for dd in dd_node:
            date = dd.xpath('child::span/text()')[0]
            url = dd.xpath('child::a/@href')[0]
            title = dd.xpath('child::a/@title')[0]
            content_result.append({
                'date': date,
                'url': base_path + url,
                'title': title
            })

        result['data'] = content_result

        result_array.append(result)
        count += 1

    return result_array


def main():
    global data_map
    # 基础路径
    base_path = 'http://www.sse.com.cn'
    # 正常url
    url = base_path + '/disclosure/overview/'

    # 通过请求获取页面html
    html = get_one_page(url)

    # 匹配正则表达式
    # re_str = '<span>(.*?)</span>.*?<a.*?href="(.*?)".*?title="(.*?)"'

    # 解析html数据拿到结果
    result = parse_one_page(html, base_path)

    # 打印结果信息
    for each in result:
        print(each["title"])
        print("----------------------------------------------------------")

        data_list = each["data"]
        for data in data_list:
            print(data["title"] + ' [' + data["date"] + ']' + " 访问地址：" + data['url'])

        print("\n")

# 执行 main 函数
main()
