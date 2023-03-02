
from pac import *


if __name__ == '__main__':
    # game = Game.Game("霍格沃茨之遗","https://ku.gamersky.com/2021/hogwarts-legacy/",9)
    # get_game_info(game)
    # 爬取2003-2023年的游戏
    for year in range(2023,2002,-1):
        get_info(year)
        print(f"{year}已经爬完")