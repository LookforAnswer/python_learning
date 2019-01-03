import urllib.request
from tkinter import *
from lxml import etree
import webbrowser
import time

def get_one_page(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')


def parse_one_page(html, base_path):
    html = etree.HTML(html)
    items = html.xpath('//div[@class="sse_common_wrap_cn"]')
    count = 0
    result_array = []
    for item in items:
        if count > 3:
            break
        # 获取title信息
        result = {'title': '', 'data': {}}
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

    html = get_one_page(url)

    # 上交所公告
    re_str = '<span>(.*?)</span>.*?<a.*?href="(.*?)".*?title="(.*?)"'

    # 构造信息对象
    for item in parse_one_page(html, re_str, base_path):
        item_data = item["data"]
        for each_item_data in item_data:
            data_map[each_item_data["title"]] = each_item_data

    return parse_one_page(html, re_str, base_path)


data_map = {}

widget_list = []


def refresh():
    print("刷新了！！")
    global widget_list
    for each_widget in widget_list:
        each_widget.destroy()
    time.sleep(0.5)
    app.generate_content()
    widget_list = []





class App:
    def __init__(self, root):
        self.root = root
        button_refresh = Button(root,
                                text="刷新",
                                width=15,
                                height=2,
                                command=refresh)
        button_refresh.pack()

    def generate_content(self):
        global widget_list
        for item in main():
            title = item["title"]
            title_label = Label(text=title, foreground="red")
            title_label.pack()
            widget_list.append(title_label)

            for content in item["data"]:
                desc = content['title'] + ' [' + content['date'] + ']\n'
                link = Label(text=desc, foreground="#0000ff", height=2)
                link.bind("<1>", lambda event, text=desc: self.click_link(text))
                link.pack()
                widget_list.append(link)

    def click_link(self, text):

        str = text.replace('\n', '')
        key = str[0: len(str)-13]
        url = data_map[key]['url']
        # webbrowser.open(url, new=0, autoraise=True)
        # webbrowser.open_new(url)
        webbrowser.open_new_tab(url)


root = Tk()
scrollbar = Scrollbar(root)
# scrollbar.pack(side=RIGHT, fill=Y)
root.geometry("600x450")

app = App(root)
app.generate_content()
root.mainloop()
