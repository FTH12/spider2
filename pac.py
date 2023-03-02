import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from Game import Game
from utils import *

service = Service(executable_path='E:\IDE_Tools\WebDriver\Edge\msedgedriver.exe')
option = webdriver.EdgeOptions()
# 使用chrome浏览器配置
option.use_chromium = True
# 设置无图模式
No_Image_loading = {"profile.managed_default_content_settings.images": 2}
option.add_experimental_option("prefs", No_Image_loading)
# 设置无头模式
option.add_argument('--headless')
# 设置静音
option.add_argument("--mute-audio")
# 爬取的页数控制，默认为1,若为10，则爬取10页的内容
pages = 1


def get_game_info(game_dic:Game,id):
    print(f"id:{id},开始爬取{game_dic.name}")
    try:
        g_driver = webdriver.Edge(service=service, options=option)
        g_driver.get(game_dic.url)
    except:
        # 打开网页失败则关闭
        print(f"open {game_dic.name} error")
        g_driver.close()
        return game_dic.__dict__
    time.sleep(1)
    try:
        soup = BeautifulSoup(g_driver.page_source, "html.parser")
        g_driver.close()
        yxxx_r = soup.find("div", class_="YXXX-R")
    except Exception as e:
        print(f"soup解析出错")
        print(e)
        return game_dic.__dict__
    # 获取游戏图片，获取游戏平台，获取游戏时长，获取其中的div3 包括上市时间，游戏类型，制作发行，获取游戏简介，获取玩家常用标签
    fuc_list = [get_img, get_platform, get_playtime, get_div3_info, get_jj, get_tags]
    # 开启线程池控制，最多5个线程 即运行5个函数获取需要的信息
    with ThreadPoolExecutor(max_workers=5) as t:
        obj_list = []
        # flag用于判断当前运行哪个函数，控制参数的传递
        flag = 0
        for flag in range(0,6):
            if flag == 0:
                obj = t.submit(fuc_list[flag],soup,game_dic)
            elif flag == 5:
                obj = t.submit(fuc_list[flag],soup)
            else:
                obj = t.submit(fuc_list[flag],yxxx_r)
            flag = flag + 1
            obj_list.append(obj)
        for future in as_completed(obj_list):
            datas = future.result()
            for k in datas:
                game_dic.__setattr__(k,datas[k])
    print(f"id:{id},爬取{game_dic.name}完成")
    return game_dic.__dict__


# 爬取目标网站
def get_info(year:int):
    # 创建对应年份的json文件
    f = open(f"games_{year}.json", 'a+', encoding='utf-8')
    f.write('{"result": [')
    url = f'https://ku.gamersky.com/sp/0-0-{year}-0-0-0.html'
    print(url)
    driver = webdriver.Edge(service=service, options=option)
    driver.get(url)
    page = 0;
    soup = BeautifulSoup()
    while True:
        print(f"当前在第{page+1}页")
        # 等待3秒，让网页加载完成
        time.sleep(3)
        # 利用BeautifulSoup 解析获取到的html页面
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # 获取当前页的所有游戏的信息
        gamelist = soup.find_all("li", class_="gamelist")
        gamelist.extend(soup.find_all("li",class_="ungamelist"))
        t_listgame = []
        for game in gamelist:
            # 获取当前页面的游戏的url地址，游戏名和评分
            game_url = game.find("a").get("href")
            game_name = game.find("p").text
            try:
                game_num = game.find("div", class_="num").text
            except:
                None
            game_dic = Game(name = game_name,url = game_url,score = game_num,year = year)
            t_listgame.append(game_dic)
        # 开启多线程，最多6个线程，即同时爬取6个游戏
        with ThreadPoolExecutor(max_workers=6) as t:
            obj_list = []
            id = 1
            for game_dic in t_listgame:
                # 开启线程
                obj = t.submit(get_game_info, game_dic, id)
                obj_list.append(obj)
                id += 1
            for future in as_completed(obj_list):
                data = future.result()
                json.dump(data, fp=f, ensure_ascii=False, indent=2)
                f.write(',')
        # 此处用于控制爬取的页数
        if page>=pages:
            break
        try:
            # 寻找下一页的按钮，若无则说明到最后一页，则结束循环
            driver.find_element(By.CLASS_NAME, "nexe").click()
            page = page + 1
        except:
            break
    driver.close()
    f.close()