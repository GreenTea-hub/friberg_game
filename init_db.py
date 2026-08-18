import sqlite3
import os

def init_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'players.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        create table if not exists players 
        (   
            id        integer primary key autoincrement,
            name      text not null,
            country   text not null,
            team      text not null,
            age       int not null,
            position  text not null,
            champions int not null,
            majors    int not null,
            region    text not null
        )
        ''')
    conn.commit()
    conn.close()
    print("数据库初始化完成")

if __name__ == '__main__':
    init_db()