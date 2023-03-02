class Game:
    # 游戏名
    name:str
    # 游戏链接
    url:str
    # 游戏评分
    score:str
    # 游戏发行年
    year:int
    # 游戏名的md5
    g_md5:str
    # 游戏的图片名
    img_name:str
    # 游戏平台
    pts:list
    # 游戏预期游玩时长
    play_time:str
    # 游戏上市时间 年月日
    ss_time:str
    # 游戏类型
    type:str
    # 游戏发行制作公司
    company:str
    # 游戏简介
    jj:str
    # 玩家常用标签
    tags:list

    def __init__(self,name='',url='',score="0",year=9999,g_md5='',img_name='',pts=None,play_time='',ss_time='',type="未分类",company='',jj='',tags=None):
        self.name = name
        self.url = url
        self.score = score
        self.year = year
        self.g_md5 = g_md5
        self.img_name = img_name
        self.pts = pts
        self.play_time = play_time
        self.ss_time = ss_time
        self.type = type
        self.company = company
        self.jj = jj
        self.tags = tags


