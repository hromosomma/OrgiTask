import sys
import os
import random
from datetime import datetime
import sqlite3
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QInputDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt


SCREEN_SIZE = [1000, 1000]


con = sqlite3.connect('tasks.db')
cur = con.cursor()


class OrgaTask(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setFocus()

    def initUI(self):
        self.setGeometry(300, 150, *SCREEN_SIZE)
        self.setWindowTitle('OrgaTask')
        self.setStyleSheet("background-color: pink;")

        self.hi = QLabel(self)
        self.font = QFont("Unbounded", 14, QFont.Weight.DemiBold)
        self.hi.setFont(self.font)

        self.time = int(datetime.now().strftime("%H"))
        if self.time >= 5 and self.time <= 11:
            self.hi.setText("Good Morning! Ready to work?")
        elif self.time >= 12 and self.time <= 16:
            self.hi.setText("Good day! Do you have plans?")
        elif self.time >= 22 or self.time <= 4:
            self.hi.setText("Good night! Are you a night owl?:)")
        else:
            self.hi.setText("Good evening and good luck!")
        self.hi.move(40, 30)

        meme_folder = '/home/hromic/tasks_planner/hehehe'
        if os.path.exists(meme_folder):
            self.memes_list = os.listdir(meme_folder)
            self.meme_path = random.choice(self.memes_list)
            self.today_meme = QPixmap(os.path.join(meme_folder, self.meme_path))
        else:
            self.today_meme = QPixmap()

        self.image = QLabel(self)
        self.image.move(40, 530)
        self.image.setPixmap(self.today_meme)
        self.image.setScaledContents(True)
        self.image.setFixedSize(300, 300)
        self.image.update()

        self.meme_text = QLabel(self)
        self.meme_text.setText('The meme of the day is:')
        self.meme_text.move(100, 500)

        self.add_button = QPushButton(self)
        self.add_button.move(40, 70)
        self.add_button.resize(140, 60)
        self.add_button.setText('Добавить задачу')
        self.add_button.clicked.connect(self.run)

        self.not_started_button = self.create_button('Не начато', 40)
        self.not_started_button.clicked.connect(self.not_started_menu)

        self.in_process_button = self.create_button('В процессе', 260)
        self.in_process_button.clicked.connect(self.in_process_menu)

        self.is_checking_button = self.create_button('На проверке', 480)
        self.is_checking_button.clicked.connect(self.checking_menu)

        self.finish_button = self.create_button('Завершено', 700)
        self.finish_button.clicked.connect(self.finished_menu)

        self.tasks_number = QLabel(self) 
        self.tasks_number.setFont(self.font)
        self.tasks_number.setText('Вот столько дел нужно выполнить:')
        self.tasks_number.move(40, 230)

        self.not_started_tasks = self.tasks_list(1)
        self.in_process_tasks = self.tasks_list(2)
        self.checking_tasks = self.tasks_list(3)

        self.not_started_label = QLabel(self)
        self.not_started_label.setFont(self.font)
        self.not_started_label.setText(f'Не начато: {self.not_started_tasks}')
        self.not_started_label.move(40, 260)

        self.in_process_label = QLabel(self)
        self.in_process_label.setFont(self.font)
        self.in_process_label.setText(f'В процессе: {self.in_process_tasks}')
        self.in_process_label.move(40, 290)

        self.checking_label = QLabel(self)
        self.checking_label.setFont(self.font)
        self.checking_label.setText(f'На проверке: {self.checking_tasks}')
        self.checking_label.move(40, 320)

    def tasks_list(self, idi):
        numb = cur.execute('''
                    SELECT * FROM user_tasks 
                    WHERE id = ?
                    ''', (idi,)).fetchall()  
        return len(numb)

    def create_button(self, text, y_position):
        button = QPushButton(self)
        button.move(620, y_position)
        button.resize(320, 200)
        button.setText(text)
        button.setStyleSheet('background-color: blue')
        return button

    def run(self):
        name, ok_pressed = QInputDialog.getText(self, 'Введите задачу', 'Что за план?')
        if ok_pressed:
            print(name)
            self.addTask(name)

    def addTask(self, name):
        cur.execute('''
                    INSERT INTO user_tasks (id, title) VALUES(?, ?)
                        ''',(1, name))
        con.commit()
        print(name)

    def not_started_menu(self):
        self.hide()
        NotStartedMenu.show()
        NotStartedMenu.show_tasks()

    def in_process_menu(self):
        self.hide()
        InProcessMenu.show()
        InProcessMenu.show_tasks()

    def checking_menu(self):
        self.hide()
        CheckingMenu.show()
        CheckingMenu.show_tasks()

    def finished_menu(self):
        self.hide()
        FinishedMenu.show()
        FinishedMenu.show_tasks()

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            if event.key() == Qt.Key.Key_S:
                self.show()
                NotStartedMenu.hide()
                InProcessMenu.hide()
                CheckingMenu.hide()
                FinishedMenu.hide()
            elif event.key() == Qt.Key.Key_N:
                self.not_started_menu()
            elif event.key() == Qt.Key.Key_I:
                self.in_process_menu()
            elif event.key() == Qt.Key.Key_C:
                self.checking_menu()
            elif event.key() == Qt.Key.Key_F:
                self.finished_menu()

class Menu(QWidget):
    def __init__(self, title, r, g, b, nothing_message, idi, parent):
        super().__init__()
        self.title = title
        self.r = r
        self.g = g
        self.b = b
        self.nothing_message = nothing_message
        self.id = idi
        self.parent = parent

        self.initUI()
        self.setFocus()

    def initUI(self):
        self.setGeometry(300, 150, *SCREEN_SIZE)
        self.setWindowTitle(self.title)
        self.setStyleSheet(f"background-color: rgb({self.r}, {self.g}, {self.b})")

        self.back_button = QPushButton('Назад', self)
        self.back_button.setGeometry(40, 40, 100, 40)
        self.back_button.clicked.connect(self.back)

    def back(self):
        self.parent.show()
        self.close()

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            if event.key() == Qt.Key.Key_S:
                self.close()
                org.show()
            elif event.key() == Qt.Key.Key_N:
                self.close()
                NotStartedMenu.show()
            elif event.key() == Qt.Key.Key_I:
                self.close()
                InProcessMenu.show()
            elif event.key() == Qt.Key.Key_C:
                self.close()
                CheckingMenu.show()
            elif event.key() == Qt.Key.Key_F:
                self.close()
                FinishedMenu.show()

    def show_tasks(self):
        tasks = cur.execute('''
                            SELECT * FROM user_tasks 
                            WHERE id = ?
                            ''', (self.id,)).fetchall()
        
        x = 40  
        y = 150  

        if len(tasks) == 0:
            text = QLabel(self)
            font = QFont("Unbounded", 14, QFont.Weight.DemiBold) 
            text.setFont(font)
            text.setText(self.nothing_message)
            text.move(x, y)
            text.show()
        else:
            text = QLabel(self)
            font = QFont("Unbounded", 14, QFont.Weight.DemiBold) 
            text.setFont(font)
            text.setText('Твои делишки:')
            text.move(x, y)
            text.show() 

            for task in tasks:
                task_title = task[1]

                task_button = QPushButton(task_title, self)
                task_button.move(x, y + 60)
                task_button.clicked.connect(lambda: self.move_task(self.id, task_title))
                task_button.show()

                y += 60

    def move_task(self, idi, task_title):
        if idi != 4:
            changing_state = cur.execute('''
                                        SELECT * FROM tasks_state 
                                            WHERE id = ?
                                            ''', (idi + 1,)).fetchall()
            

            reply = QMessageBox.question(self, 'Переместить в другое состояние', f'Вы хотите отметить задачу как {changing_state[0][1]}?',
                                            QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                cur.execute('''
                            UPDATE user_tasks
                            SET id = ?
                            WHERE title = ?
                            ''', (idi + 1, task_title))
                con.commit()
                self.show_tasks()


            else:
                reply.close()

        else:
            reply = QMessageBox.question(self, 'Переместить в другое состояние', 'Вы хотите удалить задачу?',
                                        QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                cur.execute('''
                            DELETE FROM user_tasks
                            WHERE title = ?
                            ''', (task_title,))
                con.commit()
                self.show_tasks()

            else:
                reply.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    org = OrgaTask()
    org.show()

    NotStartedMenu = Menu('Не начато', 224, 128, 38, 'Тут ничего нет!!! Или ты бездельник, или выполняешь задачи вовремя', 1, org)
    InProcessMenu = Menu('В процессе', 96, 167, 224, 'Дружок, займись хоть чем-то в своей жизни', 2, org)
    CheckingMenu = Menu('На проверке', 96, 224, 163, 'Надеюсь, тебя еще не съели учителя, начальники или родители', 3, org)
    FinishedMenu = Menu('Завершено', 160, 224, 96, 'Доводи дела до конца!', 4, org)

    sys.exit(app.exec())
