import sqlite3


con = sqlite3.connect('tasks.db')

cursor = con.cursor()

cursor.execute(''' 
               CREATE TABLE IF NOT EXISTS tasks_state (
               id INTEGER PRIMARY KEY,
               title TEXT NOT NULL)
               ''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS user_tasks (
               id INTEGER NOT NULL,
               title TEXT NOT NULL)
               ''')

cursor.execute('''
                    INSERT INTO tasks_state (id, title) VALUES(1, 'Not started')
               ''')

cursor.execute('''
                    INSERT INTO tasks_state (id, title) VALUES(2, 'In process')
               ''')

cursor.execute('''
                    INSERT INTO tasks_state (id, title) VALUES(3, 'Checking')
               ''')

cursor.execute('''
                    INSERT INTO tasks_state (id, title) VALUES(4, 'Finished')
               ''')
con.commit()
con.close()
