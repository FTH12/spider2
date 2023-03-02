import hashlib
import os
from urllib.request import urlretrieve
from bs4 import BeautifulSoup


# 将游戏名转换为md5
def md5tool(str):
    return hashlib.md5(str.encode()).hexdigest()

# 设置img存储的路径
def set_path(year):
    img_path = os.getcwd() + '\gameimg\\'
    t_path = img_path+str(year)+"\\"
    f = os.path.exists(t_path)
    if not f:
        os.mkdir(t_path)
    return t_path

# 获取游戏的封面图像
def get_img(soup:BeautifulSoup,game_dic):
    # print("get_img此处运行")
    k_v = {'g_md5':'','img_name':''}
    try:
        yxxx_l = soup.find("div", class_="YXXX-L")
        img_div = yxxx_l.find('div', class_='img')
        img_url = img_div.find("a").get('href')
        img_url = img_url.split("?")
        img_format = img_url[1][-4:]
        g_md5 = md5tool(game_dic.name)
        img_name = g_md5 + img_format
        urlretrieve(img_url[1], set_path(game_dic.year) + img_name)
    except Exception as e:
        print(f"错误信息：{e}")
        print(f"{game_dic.name}没有图片")
        g_md5=""
        img_name=""
    k_v['g_md5'] = g_md5
    k_v['img_name'] = img_name
    return k_v

# 获取游戏的平台列表
def get_platform(yxxx_r):
    # print("get_platform此处运行")
    k_v = {'pts':[]}
    pt_list = []
    try:
        pts_div = yxxx_r.find("div", class_="win")
        pts = pts_div.find_all("a")
        for pt in pts:
            pt_list.append(pt.text)
    except:
        None
    finally:
        k_v['pts'] = pt_list
        return k_v

# 获取游戏的游玩时长
def get_playtime(yxxx_r):
    # print("get_playtime此处运行")
    k_v = {"g_time":""}
    g_time = ""
    try:
        g_time_div = yxxx_r.find("div", class_="clock")
        g_time = g_time_div.text
        # game_dic.play_time = g_time
        k_v["g_time"] = g_time
    except:
        None
    finally:
        return k_v

# 获取其中的div3 包括上市时间，游戏类型，制作发行
def get_div3_info(yxxx_r):
    # print("get_div3_info此处运行")
    k_v = {"ss_time":"","type":"","company":""}
    ss_time = ""
    g_lx = ""
    g_cpn = ""
    try:
        # 获取其中的div3 包括上市时间，游戏类型，制作发行
        yxxx_r_div3 = yxxx_r.find("div", class_="div3")
        # 获取上市时间
        ss_time = yxxx_r_div3.find("div", class_="time").text
        # 获取游戏类型和制作发行
        tt2_div2 = yxxx_r_div3.find_all("div", class_="tt2")
        # 游戏类型
        g_lx = tt2_div2[0].find("a").text
        # 制作发行
        g_cpn = tt2_div2[1].find("div", class_="txt").text
    except:
        None
    finally:
        k_v["ss_time"] = ss_time
        k_v["type"] = g_lx
        k_v["company"] = g_cpn
        return k_v

# 获取游戏简介
def get_jj(yxxx_r):
    # print("get_jj此处运行")
    g_jj = ""
    k_v = {"jj":""}
    try:
        g_jj = yxxx_r.find("div", class_="con-hide").find("p").text
        print(g_jj)
    except:
        g_jj = yxxx_r.find("div", class_="con").find("p").text
        print(g_jj)
    finally:
        k_v["jj"] = g_jj
        return k_v

# 获取游戏的常用标签
def get_tags(soup):
    # print("get_tags此处运行")
    tag_list = []
    k_v = {"tags":[]}
    try:
        player_tags_div = soup.find("span", class_="tag-con").children
        for tag in player_tags_div:
            tag_list.append(tag.text)
        # game_dic.tags = tag_list
    except:
        None
    finally:
        k_v["tags"] = tag_list
        return k_v