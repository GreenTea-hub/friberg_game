import sqlite3
import os
from init_db import init_db

PLAYERS = [
    # (name, country, team, age, position, champions, majors,region)
    ("Niko", "波黑", "Falcons",29,"rifler",1 ,17,"欧洲"),
    ("m0nesy", "俄罗斯", "Falcons", 21, "AWPer",1,7,"独联体"),
    ("kyousuke", "俄罗斯", "Falcons",18, "rifler",1 ,2,"独联体"),
    ("TeSeS", "丹麦", "Falcons",25,"rifler",1, 9,"欧洲"),
    ("karrigan", "丹麦", "Falcons", 36, "rifler", 2, 22,"欧洲"),
    ("apEX", "法国", "Vitality",33 , "rifler", 4,22 , "欧洲"),
    ("ZywOo", "法国", "Vitality",25 , "AWPer",3 ,11 , "欧洲"),
    ("flameZ", "以色列", "Vitality", 23, "rifler",2 ,7 , "亚洲"),
    ("mezii", "英国", "Vitality",27 , "rifler", 2, 7, "欧洲"),
    ("ropz", "爱沙尼亚", "Vitality", 26, "rifler",3 , 13, "欧洲"),
    ("donk", "俄罗斯", "Spirit", 19, "rifler",1 ,5 , "独联体"),
    ("shiro", "俄罗斯", "Spirit", 25, "AWPer", 1, 8, "独联体"),
    ("magixx", "俄罗斯", "Spirit", 23, "rifler", 1, 7, "独联体"),
    ("zont1x", "乌克兰", "Spirit", 21, "rifler", 1, 4, "独联体"),
    ("tN1R", "白俄罗斯", "Spirit", 25, "rifler", 0, 3, "独联体"),
    ("xerion", "以色列", "MOUZ", 22, "rifler", 0, 7, "亚洲"),
    ("torzsi", "匈牙利", "MOUZ", 24, "AWPer", 0, 7, "欧洲"),
    ("xelex", "匈牙利", "MOUZ", 18, "rifler", 0, 1, "欧洲"),
    ("PR", "捷克", "MOUZ", 18, "rifler", 0, 2, "欧洲"),
    ("spinx", "以色列", "MOUZ", 25, "rifler", 1, 9, "亚洲"),
    ("frozen", "斯洛伐克", "FaZe", 24, "rifler", 0, 8, "欧洲"),
    ("jcobbb", "波兰", "FaZe", 22, "rifler", 0, 1, "欧洲"),
    ("JBOEN", "丹麦", "FaZe", 21, "AWPer", 0, 0, "欧洲"),
    ("Twistzz", "加拿大", "FaZe", 26, "rifler", 1, 11, "北美洲"),
    ("Neityu", "法国", "FaZe", 21, "rifler", 0, 0, "欧洲"),
    ("KSCERATO", "巴西", "FURIA", 26, "rifler", 0, 11, "南美洲"),
    ("molodoy", "哈萨克斯坦", "FURIA", 21, "AWPer", 0, 3, "独联体"),
    ("Fallen", "巴西", "FURIA", 35, "rifler", 2, 19, "南美洲"),
    ("yuurih", "巴西", "FURIA", 26, "rifler", 0, 11, "南美洲"),
    ("YEKINDAR", "拉脱维亚", "FURIA", 26, "rifler", 0, 8, "欧洲"),
    ("b1t", "乌克兰", "Natus Vincere", 23, "rifler", 2, 9, "独联体"),
    ("wonderful", "乌克兰", "Natus Vincere", 21, "AWPer", 1, 6, "独联体"),
    ("iM", "罗马尼亚", "Natus Vincere", 27, "rifler", 1, 7, "欧洲"),
    ("makazze", "塞尔维亚科索沃", "Natus Vincere", 19, "rifler", 0, 2, "欧洲"),
    ("Aleksib", "芬兰", "Natus Vincere", 29, "rifler", 1, 10, "欧洲"),
    ("huNter-", "波黑", "G2", 30, "rifler", 0, 9, "欧洲"),
    ("HeavyGod", "以色列", "G2", 24, "rifler", 0, 4, "亚洲"),
    ("MATYS", "斯洛伐克", "G2", 24, "rifler", 0, 3, "欧洲"),
    ("r1nkle", "乌克兰", "G2", 21, "AWPer", 0, 1, "独联体"),
    ("NertZ", "以色列", "G2", 27, "rifler", 0, 6, "亚洲"),
    ("XANTARES", "土耳其", "Aurora", 31, "rifler", 0, 8, "亚洲"),
    ("woxic", "土耳其", "Aurora", 27, "AWPer", 0, 8, "亚洲"),
    ("Wicadia", "土耳其", "Aurora", 21, "rifler", 0, 4, "亚洲"),
    ("Jimpphat", "芬兰", "Aurora", 19, "rifler", 0, 4, "欧洲"),
    ("kyxsan", "北马其顿", "Aurora", 26, "rifler", 0, 5, "欧洲"),
    ("bLitz", "蒙古", "The MongolZ", 25, "rifler", 0, 8, "亚洲"),
    ("910", "蒙古", "The MongolZ", 24, "AWPer", 0, 5, "亚洲"),
    ("techno", "蒙古", "The MongolZ", 21, "rifler", 0, 8, "亚洲"),
    ("senzu", "蒙古", "BC.Game", 20, "rifler", 0, 3, "亚洲"),
    ("mzinho", "蒙古", "BC.Game", 19, "rifler", 0, 5, "亚洲"),
    ("s1mple", "乌克兰", "BC.Game", 28, "AWPer", 1, 14, "独联体"),
    ("electronic", "俄罗斯", "BC.Game", 27, "rifler", 1, 13, "独联体"),
    ("Magisk", "丹麦", "BC.Game", 28, "rifler", 4, 11, "欧洲"),
    ("JamYoung", "中国", "TYLOO", 25, "rifler", 0, 3, "亚洲"),
    ("Jee", "中国", "TYLOO", 21, "AWPer", 0, 4, "亚洲"),
    ("Moseyuh", "中国", "TYLOO", 21, "rifler", 0, 3, "亚洲"),
    ("Mercury", "中国", "TYLOO", 25, "rifler", 0, 3, "亚洲"),
    ("Zero", "中国", "TYLOO", 20, "rifler", 0, 1, "亚洲"),
    ("Westmelon", "中国", "Lynn Vision", 25, "rifler", 0, 4, "亚洲"),
    ("z4KR", "中国", "Lynn Vision", 23, "AWPer", 0, 4, "亚洲"),
    ("EmiliaQAQ", "中国", "Lynn Vision", 21, "rifler", 0, 4, "亚洲"),
    ("Starry", "中国", "Lynn Vision", 21, "rifler", 0, 4, "亚洲"),
    ("C4LLM3SU3", "中国", "Lynn Vision", 22, "rifler", 0, 3, "亚洲"),
    ("Jame", "俄罗斯", "PARIVISION", 27, "AWPer", 1, 10, "独联体"),
    ("xiELO", "俄罗斯", "PARIVISION", 20, "rifler", 0, 2, "独联体"),
    ("FL1T", "俄罗斯", "PARIVISION", 25, "rifler", 1, 7, "独联体"),
    ("zweih", "俄罗斯", "PARIVISION", 18, "rifler", 0, 3, "独联体"),
    ("rain", "挪威", "100 Thieves", 31, "rifler", 1, 19, "欧洲"),
    ("device", "丹麦", "100 Thieves", 30, "AWPer", 4, 2, "欧洲"),
    ("EliGE", "美国", "Liquid", 29, "rifler", 0, 17, "北美洲"),
    ("NAF", "加拿大", "Liquid", 28, "rifler", 0, 14, "北美洲"),
    ("malbsMd", "危地马拉", "Liquid", 23, "rifler", 0, 4, "北美洲"),
    ("Staehr", "丹麦", "Astralis", 22, "rifler", 0, 3, "欧洲"),
    ("Hooxi", "丹麦", "Astralis", 31, "rifler", 0, 6, "欧洲"),
    ("jabbi", "丹麦", "Astralis", 23, "rifler", 0, 6, "欧洲"),
    ("stavn", "丹麦", "Ninjas in Pyjamas", 24, "AWPer", 0, 4, "欧洲"),
]

def seed():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'players.db')
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO players (name, country, team, age, position, champions, majors,region) "
            "VALUES (?, ?, ?, ?, ?, ?, ?,?)", PLAYERS
        )
        conn.commit()
        print(f"已导入 {len(PLAYERS)} 名选手")
    finally:
        conn.close()


if __name__ == '__main__':
    init_db()  # 表不存在就先建表
    seed()