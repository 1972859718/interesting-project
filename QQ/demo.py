#coding: utf-8
from imp import reload
import time
from selenium import webdriver
from lxml import etree

def PrintInfo():
    print('提示信息'.center(70,'*'))
    print("本软件用以爬取Q好友的说说，默认爬取最近10页左右".center(70,' '))
    print("请放心输入密码，除了以明文展示以外没有任何风险".center(70,' '))
    print("在爬取过程中会调用浏览器并进行一系列的自动操作".center(70,' '))
    print("请不要在程序运行完成前关闭任何自动打开的软件".center(70,' '))
    print(''.center(70,'*'))
    
def text(friend, user , pw):
    # 获取浏览器驱动
    driver = webdriver.Chrome(executable_path='chromedriver')

    # 浏览器窗口最大化
    driver.maximize_window()

    # 浏览器地址定向为 qq 登陆页面
    driver.get('http://i.qq.com')

    # 所以这里需要选中一下 frame，否则找不到下面需要的网页元素
    driver.switch_to.frame('login_frame')

    # 自动点击账号登陆方式
    driver.find_element_by_id('switcher_plogin').click()

    # 账号输入框输入已知 QQ 账号
    driver.find_element_by_id('u').send_keys(user)

    # 密码框输入已知密码
    driver.find_element_by_id('p').send_keys(pw)

    # 自动点击登陆按钮
    driver.find_element_by_id('login_button').click()

    # 让 webdriver 操纵当前页
    driver.switch_to.default_content()

    # 跳到说说的 url，friend 你可以任意改成你想访问的空间
    driver.get('http://user.qzone.qq.com/' + friend + '/311')

    next_num = 0 # 初始“下一页”的 id
    count = 0 #初始化转发计数器
    max_num = 9 #默认爬取最近10页的说说

    while True:
        # 下拉滚动条，使浏览器加载出动态加载的内容
        # 我这里是从 1 开始到 6 结束分 5 次加载完每页数据
        for i in range(1, 6):
            height = 20000 * i# 每次滑动 20000 像素
            strWord = "window.scrollBy(0," + str(height) + ")"
            driver.execute_script(strWord)
            time.sleep(5)

        # 很多时候网页由多个<frame>或<iframe>组成，webdriver 默认定位的是最外层的 frame
        # 所以这里需要选中一下说说所在的 frame，否则找不到下面需要的网页元素
        driver.switch_to.frame('app_canvas_frame')
        selector = etree.HTML(driver.page_source)
        divs = selector.xpath('//*[@id="msgList"]/li/div[3]')

        # 这里使用 a 表示内容可以连续不清空写入
        with open('qq_word.txt', 'a', encoding='utf-8') as f:
            for div in divs:
                qq_name = div.xpath('./div[2]/a/text()')
                qq_content = div.xpath('./div[2]/pre/text()')
                qq_time = div.xpath('./div[4]/div[1]/span/a/text()')
                qq_name = qq_name[0] if len(qq_name) > 0 else ''
                qq_content = qq_content[0] if len(qq_content) > 0 else ''
                if len(qq_content) == 0:
                    count = count + 1
                qq_time = qq_time[0] if len(qq_time) > 0 else ''
                print(qq_name, qq_time, qq_content)
                f.write(qq_content+"\n")

        # 当已经到了尾页，“下一页”这个按钮就没有 id 了，可以结束了
        if driver.page_source.find('pager_next_' + str(next_num)) == -1:
            break

        #当转发无评论数量每累计超过7条时，多爬取一页
        if count % 7 == 6:
            max_num = max_num + 1

        #当爬取了10页以后，停止爬取
        if next_num >= max_num:
            break

        # 找到“下一页”的按钮，因为下一页的按钮是动态变化的，这里需要动态记录一下
        driver.find_element_by_id('pager_next_' + str(next_num))

        # "下一页"的 id
        driver.find_element_by_id('pager_next_' + str(next_num)).click()

        # "下一页"的 id
        next_num += 1

        # 因为在下一个循环里首先还要把页面下拉，所以要跳到外层的 frame 上
        driver.switch_to.parent_frame()

if __name__ == '__main__':
    PrintInfo()
    friend = input('请输入你朋友的 QQ 号（朋友的空间要求允许你能访问）：')
    user = input('请输入你的 QQ 号：')
    pw = input('请输入你的 QQ 密码：')
    print("\n爬取开始，请稍后。。。\n")
    text(friend, user, pw)
    print("\n爬取完成")
