# By.Zeno
 
 
import requests
from lxml import etree
import os
 
 
# 封装从栏目页进入内容页连接解析函数
def name(url, type_name, headers):
    url = url + page_list_url[int(type_name)]
    doc_name = './' + page_list_name[int(type_name)].encode('ISO-8859-1').decode('gbk')
    page_list_text = requests.get(url=url, headers=headers).text
    page_list_tree = etree.HTML(page_list_text)
    page_list_limit = page_list_tree.xpath('//*[@id="main"]/div[4]/a[7]/text()')[0]
    while True:
        print("{}上限页数为{}页".format(page_list_name[int(type_name)].encode('ISO-8859-1').decode('gbk'), page_list_limit))
        page_need = input("请输入您要爬取{}的页数: ".format(page_list_name[int(type_name)].encode('ISO-8859-1').decode('gbk')))
 
        if page_need.isdigit() and 1 <= int(page_need) <= int(page_list_limit):  # 判断是否填写有误(包括页数判断)
            if not os.path.exists(doc_name):
                os.mkdir(doc_name)
            for i in range(1, int(page_need) + 1):
                if i == 1:  # 第1页爬取
                    crawler(page_list_tree, doc_name)
                else:  # 第2页及以上爬取
                    page_url = url + 'index_' + str(i) + '.html'
                    page_list_text = requests.get(url=page_url, headers=headers).text
                    page_list_tree = etree.HTML(page_list_text)
                    crawler(page_list_tree, doc_name)
            break
        else:
            print("请重新输入正确的数字")
 
 
# 封装内容页图片连接解析函数
def crawler(page_list_tree, doc_name):
    img_list_url = page_list_tree.xpath('//*[@id="main"]/div[3]/ul/li/a/@href')
    img_name = page_list_tree.xpath('//*[@id="main"]/div[3]/ul/li/a/b/text()')
    for i in range(len(img_name)):
        img_url = 'http://pic.netbian.com' + img_list_url[i]
        name = img_name[i].encode('ISO-8859-1').decode('gbk') + '.jpg'
        img_page = requests.get(url=img_url, headers=headers).text
        img_page_tree = etree.HTML(img_page)
        page_img_src = img_page_tree.xpath('//*[@id="img"]/img/@src')[0]
        page_img_src = 'http://pic.netbian.com' + page_img_src
        img = requests.get(url=page_img_src, headers=headers).content
        img_path = doc_name + '/' + name
        with open(img_path, 'wb') as fp:
            fp.write(img)
            print(name + '下载成功!!!')
 
 
url = 'http://pic.netbian.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400'
}
response = requests.get(url=url, headers=headers).text
tree = etree.HTML(response)
page_list_url = tree.xpath('//*[@id="main"]/div[2]/a/@href')
page_list_name = tree.xpath('//*[@id="main"]/div[2]/a/text()')
while True:
    print("0.风景 1.美女 2.游戏 3.动漫 4.影视 5.明星 6.汽车 7.动物 8.人物 9.美食 10.宗教 11.背景")
    type_name = input("请输入对应数字: ")
    if type_name.isdigit() and 0 <= int(type_name) <= 11: #判断是否数字且是否超出可爬取范围
        name(url, type_name, headers)
        break
    else:
        print("请重新输入正确的数字")
        continue