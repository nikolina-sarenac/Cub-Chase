from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication, QPushButton, QLineEdit)
from PyQt5.QtCore import (Qt, QSize)
from PyQt5.QtGui import (QPixmap, QIcon)
from multiprocessing import Process, Queue, Value
from threading import Timer
from network import Network
import sys
import pygame
import CubMaze
import PlayerProcess
import CubPaws
import EnemyProcess


class CubChase(QWidget):
    def __init__(self):
        super().__init__()
        self.maze = CubMaze.Maze()
        self.paws1 = CubPaws.Paws()
        self.paws2 = CubPaws.Paws()
        self._block_surf = None
        self._display_surf = None
        self._background = None
        self._backgroundResult = None
        self._paws_image = None
        self._paws_image2 = None
        self.screen = None
        self.playerOne = None
        self.playerTwo = None
        self.enemyOne = None
        self.enemyTwo = None
        self.playerOneFinished = False
        self.playerTwoFinished = False
        self.playerOnePoints = 0
        self.playerTwoPoints = 0
        self.playerOneTotal = 0
        self.playerTwoTotal = 0
        self._trap = None
        self._board = None
        self._life = None
        self.add_force = False
        self.crown = None
        self.continue_img = None
        self.name1 = ""
        self.name2 = ""

        self.windowWidth = 640
        self.windowHeight = 480
        self.x = Value('i', 379)
        self.y = Value('i', 210)
        self.x2 = Value('i', 237)
        self.y2 = Value('i', 210)
        self.ex1 = Value('i', 437)
        self.ey1 = Value('i', 420)
        self.ex2 = Value('i', 175)
        self.ey2 = Value('i', 420)
        self.life1 = Value('i', 3)
        self.life2 = Value('i', 3)
        self.EnemyChase1 = Value('i', 1)
        self.EnemyChase2 = Value('i', 1)
        self.cought1 = Value('i', 0)
        self.cought2 = Value('i', 0)
        self.caught3 = Value('i', 0)
        self.add_trap1 = Value('i', 1)
        self.add_trap2 = Value('i', 1)
        self.waitEnemy = Value('i', 70)
        self.width = 25
        self.height = 25
        self.matW = 640 / 22
        self.matH = 480 / 16
        self.run = True
        self.player_one_dead = False
        self.player_two_dead = False
        self.game_finished = False
        self.timer_t1 = None
        self.timer_t2 = None
        self.is_tournament = False
        self.one_winner = False
        self.online = 0
        self.me = 0
        self.n = None

        self.initUI()

    def initUI(self):
        self.hbox = QHBoxLayout(self)
        self.pixmap = QPixmap("pocetna.jpg")
        self.setMaximumSize(640, 480)
        self.setMinimumSize(640, 480)

        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)

        self.hbox.addWidget(self.lbl)
        self.setLayout(self.hbox)

        self.move(150, 100)
        self.setWindowTitle('Cub Chase')

        self.txtbox1 = QLineEdit(self)
        self.txtbox1.move(228, 315)
        self.txtbox1.resize(96, 23)
        self.txtbox1.setStyleSheet('background-color: #f5deb3; border: 2px solid teal; font: Bold')
        self.txtbox1.setAlignment(Qt.AlignCenter)
        self.txtbox1.setVisible(False)

        self.txtbox2 = QLineEdit(self)
        self.txtbox2.move(344, 315)
        self.txtbox2.resize(100, 23)
        self.txtbox2.setStyleSheet('background-color: #f5deb3; border: 2px solid teal; font: Bold')
        self.txtbox2.setAlignment(Qt.AlignCenter)
        self.txtbox2.setVisible(False)

        self.txtbox3 = QLineEdit(self)
        self.txtbox3.move(30, 160)
        self.txtbox3.resize(200, 35)
        self.txtbox3.setStyleSheet('background-color: rgba(143,188,143, 90); border: 2px solid burlywood; font: Bold')
        self.txtbox3.setAlignment(Qt.AlignCenter)
        self.txtbox3.setVisible(False)

        # T U R N I R
        self.txtbox4 = QLineEdit(self)
        self.txtbox4.move(55, 130)
        self.txtbox4.resize(200, 35)
        self.txtbox4.setStyleSheet('background-color: #f5deb3; border: 2px solid peru; font: Bold')
        self.txtbox4.setAlignment(Qt.AlignCenter)
        self.txtbox4.setVisible(False)

        self.txtbox5 = QLineEdit(self)
        self.txtbox5.move(55, 180)
        self.txtbox5.resize(200, 35)
        self.txtbox5.setStyleSheet('background-color: #f5deb3; border: 2px solid peru; font: Bold')
        self.txtbox5.setAlignment(Qt.AlignCenter)
        self.txtbox5.setVisible(False)

        self.txtbox6 = QLineEdit(self)
        self.txtbox6.move(55, 230)
        self.txtbox6.resize(200, 35)
        self.txtbox6.setStyleSheet('background-color: #f5deb3; border: 2px solid peru; font: Bold')
        self.txtbox6.setAlignment(Qt.AlignCenter)
        self.txtbox6.setVisible(False)

        self.txtbox7 = QLineEdit(self)
        self.txtbox7.move(55, 280)
        self.txtbox7.resize(200, 35)
        self.txtbox7.setStyleSheet('background-color: #f5deb3; border: 2px solid peru; font: Bold')
        self.txtbox7.setAlignment(Qt.AlignCenter)
        self.txtbox7.setVisible(False)

        self.txtbox8 = QLineEdit(self)
        self.txtbox8.move(385, 130)
        self.txtbox8.resize(200, 35)
        self.txtbox8.setStyleSheet('background-color: #f5deb3; border: 2px solid peru; font: Bold')
        self.txtbox8.setAlignment(Qt.AlignCenter)
        self.txtbox8.setVisible(False)

        self.txtbox9 = QLineEdit(self)
        self.txtbox9.move(385, 180)
        self.txtbox9.resize(200, 35)
        self.txtbox9.setStyleSheet('background-color: #f5deb3; border: 2px solid peru; font: Bold')
        self.txtbox9.setAlignment(Qt.AlignCenter)
        self.txtbox9.setVisible(False)

        self.txtbox10 = QLineEdit(self)
        self.txtbox10.move(385, 230)
        self.txtbox10.resize(200, 35)
        self.txtbox10.setStyleSheet('background-color: #f5deb3; border: 2px solid peru; font: Bold')
        self.txtbox10.setAlignment(Qt.AlignCenter)
        self.txtbox10.setVisible(False)

        self.txtbox11 = QLineEdit(self)
        self.txtbox11.move(385, 280)
        self.txtbox11.resize(200, 35)
        self.txtbox11.setStyleSheet('background-color: #f5deb3; border: 2px solid peru; font: Bold')
        self.txtbox11.setAlignment(Qt.AlignCenter)
        self.txtbox11.setVisible(False)

        self.btn = QPushButton('', self)
        self.btn.clicked.connect(self.showDialog)
        self.btn.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.setIconSize(QSize(89, 46))
        self.btn.resize(160, 35)
        self.btn.move(90, 245)
        self.btn.setVisible(True)

        self.btnT = QPushButton('', self)
        self.btnT.clicked.connect(self.show_tournament)
        self.btnT.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        self.btnT.setCursor(Qt.PointingHandCursor)
        self.btnT.setIconSize(QSize(89, 46))
        self.btnT.resize(155, 35)
        self.btnT.move(97, 323)
        self.btnT.setVisible(True)

        self.btnOnline = QPushButton('', self)
        self.btnOnline.clicked.connect(self.show_network)
        self.btnOnline.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        self.btnOnline.setCursor(Qt.PointingHandCursor)
        self.btnOnline.setIconSize(QSize(89, 46))
        self.btnOnline.resize(135, 30)
        self.btnOnline.move(105, 400)
        self.btnOnline.setVisible(True)

        self.btn1 = QPushButton('', self)
        self.btn1.setText('')
        self.btn1.resize(150, 50)
        self.btn1.move(100, 400)
        self.btn1.setIcon(QIcon("startdugme.jpg"))
        self.btn1.setIconSize(QSize(89, 46))
        self.btn1.resize(93, 50)
        self.btn1.move(285, 355)
        self.btn1.setCursor(Qt.PointingHandCursor)
        self.btn1.clicked.connect(self.get_player_names)
        self.btn1.setVisible(False)

        self.btnStartT = QPushButton('', self)
        self.btnStartT.clicked.connect(self.start_tournament)
        self.btnStartT.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        self.btnStartT.setCursor(Qt.PointingHandCursor)
        self.btnStartT.resize(140, 47)
        self.btnStartT.move(250, 380)
        self.btnStartT.setVisible(False)

        self.btnBack = QPushButton('', self)
        self.btnBack.clicked.connect(self.show_back)
        self.btnBack.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        self.btnBack.setCursor(Qt.PointingHandCursor)
        self.btnBack.resize(90, 29)
        self.btnBack.move(230, 429)
        self.btnBack.setVisible(False)

        self.btnBack2 = QPushButton('', self)
        self.btnBack2.clicked.connect(self.show_back)
        self.btnBack2.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        self.btnBack2.setCursor(Qt.PointingHandCursor)
        self.btnBack2.resize(74, 40)
        self.btnBack2.move(35, 423)
        self.btnBack2.setVisible(False)

        self.btnConnect = QPushButton('', self)
        self.btnConnect.clicked.connect(self.make_connection)
        self.btnConnect.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        self.btnConnect.setCursor(Qt.PointingHandCursor)
        self.btnConnect.resize(130, 30)
        self.btnConnect.move(260, 353)
        self.btnConnect.setVisible(False)

        self.btnBackOnline = QPushButton('', self)
        self.btnBackOnline.clicked.connect(self.show_back)
        self.btnBackOnline.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        self.btnBackOnline.setCursor(Qt.PointingHandCursor)
        self.btnBackOnline.resize(90, 25)
        self.btnBackOnline.move(30, 437)
        self.btnBackOnline.setVisible(False)

        self.show()

    def hide_all(self):
        self.txtbox1.setVisible(False)
        self.txtbox2.setVisible(False)
        self.txtbox3.setVisible(False)
        self.txtbox4.setVisible(False)
        self.txtbox5.setVisible(False)
        self.txtbox6.setVisible(False)
        self.txtbox7.setVisible(False)
        self.txtbox8.setVisible(False)
        self.txtbox9.setVisible(False)
        self.txtbox10.setVisible(False)
        self.txtbox11.setVisible(False)
        self.btn.setVisible(False)
        self.btn1.setVisible(False)
        self.btnT.setVisible(False)
        self.btnBack.setVisible(False)
        self.btnBack2.setVisible(False)
        self.btnBackOnline.setVisible(False)
        self.btnOnline.setVisible(False)
        self.btnStartT.setVisible(False)
        self.btnConnect.setVisible(False)

    def showDialog(self):
        self.pixmap = QPixmap("pozadina2.jpg")
        self.lbl.setPixmap(self.pixmap)
        self.hide_all()

        self.txtbox1.setVisible(True)
        self.txtbox2.setVisible(True)
        self.btn1.setVisible(True)
        self.btnBack2.setVisible(True)
        self.waitEnemy.value = 70
        self.show()

    def show_tournament(self):
        self.pixmap = QPixmap("turnirPozadina.jpg")
        self.lbl.setPixmap(self.pixmap)
        self.hide_all()

        self.txtbox4.setVisible(True)
        self.txtbox5.setVisible(True)
        self.txtbox6.setVisible(True)
        self.txtbox7.setVisible(True)
        self.txtbox8.setVisible(True)
        self.txtbox9.setVisible(True)
        self.txtbox10.setVisible(True)
        self.txtbox11.setVisible(True)

        self.btnStartT.setVisible(True)
        self.btnBack.setVisible(True)

    def show_network(self):
        self.pixmap = QPixmap("connect.png")
        self.lbl.setPixmap(self.pixmap)
        self.hide_all()

        self.txtbox3.setVisible(True)
        self.btnBackOnline.setVisible(True)
        self.btnConnect.setVisible(True)

    def show_back(self):
        self.pixmap = QPixmap("pocetna.jpg")
        self.lbl.setPixmap(self.pixmap)
        self.hide_all()

        self.btn.setVisible(True)
        self.btnT.setVisible(True)
        self.btnOnline.setVisible(True)

    def continue_tournament(self):
        self.is_tournament = True

        if self.counter % 2 == 0:
            for i in range(0, self.counter, 2):
                self.player1 = i
                self.player2 = i + 1
                self.playerOneTotal = 0
                self.playerTwoTotal = 0
                self.enemyVel = 1
                self.showMaze(self.users[self.player1]['name'], self.users[self.player2]['name'])
                self.showGameOver()
            self.num_of_winners = self.counter // 2
        else:
            for i in range(0, self.counter - 1, 2):
                self.player1 = i
                self.player2 = i + 1
                self.playerOneTotal = 0
                self.playerTwoTotal = 0
                self.enemyVel = 1
                self.showMaze(self.users[self.player1]['name'], self.users[self.player2]['name'])
                self.showGameOver()
            self.users[self.counter - 1]['winner'] = True         # neparan broj igraca -> poslednji ide direktno dalje
            self.num_of_winners = self.counter // 2 + 1

        # DRUGI KRUG TURNIRA:
        while self.num_of_winners > 1:
            self.users_winners = [{} for i in range(self.num_of_winners)]    # niz sa pobednicima
            win_positions = []                                               # pozicija pobednika u nizu self.users

            j = 0
            for i in range(0, self.counter):
                if self.users[i]['winner']:
                    self.users_winners[j] = self.users[i]               # kopiranje pobednika u novi niz
                    win_positions.insert(j, i)                          # i = pozicija u nizu self.users
                    j += 1                                              # j = pozicija u nizu users_winners

            if self.num_of_winners % 2 == 0:
                for i in range(0,  self.num_of_winners, 2):
                    self.player1 = win_positions[i]
                    k = i + 1
                    self.player2 = win_positions[k]
                    self.playerOneTotal = 0
                    self.playerTwoTotal = 0
                    self.enemyVel = 1
                    self.showMaze(self.users_winners[i]['name'], self.users_winners[k]['name'])
                    self.num_of_winners -= 1        # posle svake partije -> broj pobednika se smanjuje za 1
                    if self.num_of_winners == 1:
                        self.one_winner = True
                    self.showGameOver()
            else:
                for i in range(0,  self.num_of_winners - 1, 2):
                    self.player1 = win_positions[i]
                    k = i + 1
                    self.player2 = win_positions[k]
                    self.playerOneTotal = 0
                    self.playerTwoTotal = 0
                    self.enemyVel = 1
                    self.showMaze(self.users_winners[i]['name'], self.users_winners[k]['name'])
                    self.num_of_winners -= 1        # posle svake partije -> broj pobednika se smanjuje za 1
                    if self.num_of_winners == 1:
                        self.one_winner = True
                    self.showGameOver()

    def start_tournament(self):
        self.users = [{} for i in range(8)]
        self.counter = 0

        if len(self.txtbox4.text()) > 0 and not self.txtbox4.text().isspace():
            self.users[self.counter]['name'] = self.txtbox4.text()
            self.users[self.counter]['points'] = 0
            self.users[self.counter]['winner'] = False
            self.counter += 1
        if len(self.txtbox5.text()) > 0 and not self.txtbox5.text().isspace():
            self.users[self.counter]['name'] = self.txtbox5.text()
            self.users[self.counter]['points'] = 0
            self.users[self.counter]['winner'] = False
            self.counter += 1
        if len(self.txtbox6.text()) > 0 and not self.txtbox6.text().isspace():
            self.users[self.counter]['name'] = self.txtbox6.text()
            self.users[self.counter]['points'] = 0
            self.users[self.counter]['winner'] = False
            self.counter += 1
        if len(self.txtbox7.text()) > 0 and not self.txtbox7.text().isspace():
            self.users[self.counter]['name'] = self.txtbox7.text()
            self.users[self.counter]['points'] = 0
            self.users[self.counter]['winner'] = False
            self.counter += 1
        if len(self.txtbox8.text()) > 0 and not self.txtbox8.text().isspace():
            self.users[self.counter]['name'] = self.txtbox8.text()
            self.users[self.counter]['points'] = 0
            self.users[self.counter]['winner'] = False
            self.counter += 1
        if len(self.txtbox9.text()) > 0 and not self.txtbox9.text().isspace():
            self.users[self.counter]['name'] = self.txtbox9.text()
            self.users[self.counter]['points'] = 0
            self.users[self.counter]['winner'] = False
            self.counter += 1
        if len(self.txtbox10.text()) > 0 and not self.txtbox10.text().isspace():
            self.users[self.counter]['name'] = self.txtbox10.text()
            self.users[self.counter]['points'] = 0
            self.users[self.counter]['winner'] = False
            self.counter += 1
        if len(self.txtbox11.text()) > 0 and not self.txtbox11.text().isspace():
            self.users[self.counter]['name'] = self.txtbox11.text()
            self.users[self.counter]['points'] = 0
            self.users[self.counter]['winner'] = False
            self.counter += 1

        if 4 <= self.counter <= 8:
            self.continue_tournament()

    def timer_stopped(self):
        self.add_force = True

    #nakon 10 sekundi ce se ove vrednost setovati
    def timer_trap1(self):
        self.add_trap1.value = 0
        self.caught3.value = 0

    def timer_trap2(self):
        self.add_trap2.value = 0
        self.caught3.value = 0

    def get_player_names(self):
        self.is_tournament = False
        self.playerOneTotal = 0
        self.playerTwoTotal = 0
        self.showMaze(self.txtbox1.text(), self.txtbox2.text())

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption('Cub Chase')
        self.move(150, 100)
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self._paws_image = pygame.image.load("paws.png")
        self._paws_image2 = pygame.image.load("whitePaws.png")
        self._block_surf = pygame.image.load("block3.jpg").convert()
        self._background = pygame.image.load("grass.jpg").convert()
        self.playerOne = pygame.image.load('simba.png')
        self.playerTwo = pygame.image.load('Nalaa.png')
        self.enemyOne = pygame.image.load('timon.png')
        self.enemyTwo = pygame.image.load('pumbaa.png')
        self._trap = pygame.image.load("zamka.png")
        self._board = pygame.image.load("daska.png")
        self._life = pygame.image.load("life.png")

    def init_players_and_maze(self):
        # inicijalizacija igraca i mape
        self.playerOneFinished = False
        self.playerTwoFinished = False
        self.player_one_dead = False
        self.player_two_dead = False
        self.x.value = 379
        self.y.value = 210
        self.x2.value = 237
        self.y2.value = 210
        self.ex1.value = 379
        self.ey1.value = 420
        self.ex2.value = 237
        self.ey2.value = 420
        self.EnemyChase1.value = 1
        self.EnemyChase2.value = 1
        self.paws1.reset()
        self.paws2.reset()
        self.life1.value = 3
        self.life2.value = 3
        self.add_force = False
        self.add_trap1 = Value('i', 1)
        self.add_trap2 = Value('i', 1)
        self.caught3.value = 0
        self.game_finished = False

    def showMaze(self, name1, name2):
        self.hide()
        self.init_pygame()
        self.init_players_and_maze()

        self.name1 = name1
        self.name2 = name2

        if self.timer_t2 is not None:
            self.timer_t2.cancel()

        if self.timer_t1 is not None:
            self.timer_t1.cancel()

        self.on_render()

        q1input = Queue()
        q2input = Queue()
        quit_queue = Queue()

        p1 = Process(target=PlayerProcess.player_function, args=(self.x, self.y, q1input, quit_queue))
        p2 = Process(target=PlayerProcess.player_function, args=(self.x2, self.y2, q2input, quit_queue))
        p3 = Process(target=EnemyProcess.move_enemy, args=(self.ex1, self.ey1, self.x, self.y, self.x2, self.y2,
                                                           quit_queue, self.life1, self.life2, self.EnemyChase1,
                                                           self.cought1, self.cought2, self.add_trap1, self.add_trap2,
                                                           self.caught3, self.waitEnemy))
        p4 = Process(target=EnemyProcess.move_enemy, args=(self.ex2, self.ey2, self.x2, self.y2, self.x, self.y,
                                                           quit_queue, self.life2, self.life1, self.EnemyChase2,
                                                           self.cought2, self.cought1, self.add_trap1, self.add_trap2,
                                                           self.caught3, self.waitEnemy))
        p1.start()
        p2.start()
        p3.start()
        p4.start()

        quit = False
        timer = Timer(10.0, self.timer_stopped)
        timer.start()

        while not self.playerOneFinished or not self.playerTwoFinished:
            pygame.time.delay(20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playerOneFinished = True
                    self.playerTwoFinished = True
                    quit_queue.put(1)
                    quit = True

            keys = pygame.key.get_pressed()

            if not self.player_one_dead and not self.playerOneFinished:
                if keys[pygame.K_LEFT]:
                    q1input.put(1)
                if keys[pygame.K_RIGHT]:
                    q1input.put(2)
                if keys[pygame.K_UP]:
                    q1input.put(3)
                if keys[pygame.K_DOWN]:
                    q1input.put(4)

            if not self.player_two_dead and not self.playerTwoFinished:
                if keys[pygame.K_a]:
                    q2input.put(1)
                if keys[pygame.K_d]:
                    q2input.put(2)
                if keys[pygame.K_w]:
                    q2input.put(3)
                if keys[pygame.K_s]:
                    q2input.put(4)

            if self.life1.value == 0:
                p1.kill()
            if self.life2.value == 0:
                p2.kill()
            self.redraw_window()

        self.playerOneTotal += self.playerOnePoints
        self.playerTwoTotal += self.playerTwoPoints

        p1.kill()
        p2.kill()
        p3.kill()
        p4.kill()

        if not quit and not self.game_finished:
            pygame.time.delay(1000)
            self.showResults()
        if self.game_finished:
            if self.is_tournament:
                self.users[self.player1]['points'] = self.playerTwoTotal
                self.users[self.player2]['points'] = self.playerOneTotal

                if self.users[self.player1]['points'] > self.users[self.player2]['points']:
                    self.users[self.player1]['winner'] = True
                    self.users[self.player2]['winner'] = False
                elif self.users[self.player1]['points'] < self.users[self.player2]['points']:
                    self.users[self.player2]['winner'] = True
                    self.users[self.player1]['winner'] = False
                else:
                    #ako je nereseno -> bonus nivo
                    self.player_one_dead = False
                    self.player_two_dead = False
                    self.game_finished = False
                    self.showResults()
                return
            else:
                self.showGameOver()
        pygame.quit()

    def make_connection(self):
        self.pixmap = QPixmap("connect2.jpg")
        self.lbl.setPixmap(self.pixmap)

        self.n = Network()
        startPos = read_pos1(self.n.getPos())
        self.me = startPos[2]
        if self.me == 0:
            self.x.value = startPos[0]
            self.y.value = startPos[1]
            self.x2.value = 237
            self.y2.value = 210
        else:
            self.x2.value = startPos[0]
            self.y2.value = startPos[1]
            self.x.value = 379
            self.y.value = 210

        # primio poziciju, salje svoje ime
        data = ""
        if len(self.txtbox3.text()) > 0:
            data += self.txtbox3.text()
        else:
            data += "player"
        self.n.client.send(str.encode(data))
        # ceka da primi ime protivnika
        opponent = self.n.client.recv(2048).decode()
        myName = self.txtbox3.text()
        if len(myName) == 0:
            myName = "player" + str(self.me)

        if self.me == 1:
            self.name1 = myName
            self.name2 = opponent
        else:
            self.name1 = opponent
            self.name2 = myName

        self.showMazeOnline()

    def showMazeOnline(self):
        self.online = 1
        self.hide()
        self.init_pygame()
        self.init_players_and_maze()

        if self.timer_t2 is not None:
            self.timer_t2.cancel()

        if self.timer_t1 is not None:
            self.timer_t1.cancel()

        qinput = Queue()
        quit_queue = Queue()

        if self.me == 0:
            p = Process(target=PlayerProcess.player_function, args=(self.x, self.y, qinput, quit_queue))
        else:
            p = Process(target=PlayerProcess.player_function, args=(self.x2, self.y2, qinput, quit_queue))

        p3 = Process(target=EnemyProcess.move_enemy, args=(self.ex1, self.ey1, self.x, self.y, self.x2, self.y2,
                                                           quit_queue, self.life1, self.life2, self.EnemyChase1,
                                                           self.cought1, self.cought2, self.add_trap1, self.add_trap2,
                                                           self.caught3, self.waitEnemy))
        p4 = Process(target=EnemyProcess.move_enemy, args=(self.ex2, self.ey2, self.x2, self.y2, self.x, self.y,
                                                           quit_queue, self.life2, self.life1, self.EnemyChase2,
                                                           self.cought2, self.cought1, self.add_trap1, self.add_trap2,
                                                           self.caught3, self.waitEnemy))

        p.start()
        p3.start()
        p4.start()

        while not p.is_alive() or not p3.is_alive() or not p4.is_alive():
            pass

        self.n.client.send(str.encode("ready"))
        rec = self.n.client.recv(2048).decode()

        self.on_render()

        quit = False
        timer = Timer(15.0, self.timer_stopped)
        # timerBomb = Timer(25.0, self.timer_bomb_stopped)
        # timerBomb.start()
        timer.start()

        while not self.playerOneFinished or not self.playerTwoFinished:
            pygame.time.delay(20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playerOneFinished = True
                    self.playerTwoFinished = True
                    quit_queue.put(1)
                    quit = True

            keys = pygame.key.get_pressed()

            if (not self.player_one_dead and not self.playerOneFinished and self.me == 0) or (
                    not self.player_two_dead and not self.playerTwoFinished and self.me == 1):
                if keys[pygame.K_LEFT]:
                    qinput.put(1)
                if keys[pygame.K_RIGHT]:
                    qinput.put(2)
                if keys[pygame.K_UP]:
                    qinput.put(3)
                if keys[pygame.K_DOWN]:
                    qinput.put(4)

            if self.me == 0:
                if self.life1.value == 0:
                    p.kill()
            else:
                if self.life2.value == 0:
                    p.kill()

            p2Pos = (0, 0)
            if self.me == 0:
                p2Pos = read_pos(self.n.send(make_pos((self.x.value, self.y.value))))
                self.x2.value = p2Pos[0]
                self.y2.value = p2Pos[1]
            else:
                p2Pos = read_pos(self.n.send(make_pos((self.x2.value, self.y2.value))))
                self.x.value = p2Pos[0]
                self.y.value = p2Pos[1]

            self.redraw_window()

        if self.me == 0:
            self.n.send(make_pos((self.x.value, self.y.value)))
        else:
            self.n.send(make_pos((self.x2.value, self.y2.value)))

        self.playerOneTotal += self.playerOnePoints
        self.playerTwoTotal += self.playerTwoPoints

        p.kill()
        p3.kill()
        p4.kill()
        if not quit and not self.game_finished:
            pygame.time.delay(5000)
            self.showResults()
        if self.game_finished:
            pygame.time.delay(5000)
            self.showGameOver()
        pygame.quit()

    def showResults(self):
        self.x.value = 379
        self.y.value = 210
        self.x2.value = 237
        self.y2.value = 210

        if self.online == 1:
            if self.me == 0:
                self.n.send(make_pos((self.x.value, self.y.value)))
            else:
                self.n.send(make_pos((self.x2.value, self.y2.value)))
            self.n.client.send(str.encode("finished"))

        self._backgroundResult = pygame.image.load("rezultatKonacno.jpg")
        self.screen.blit(self._backgroundResult, [0, 0])

        font = pygame.font.Font('Sketch_Block.ttf', 20)
        black = (255, 255, 255)

        text = font.render(self.name1, True, black)
        result = font.render(str(self.playerTwoTotal), True, black)
        total_results = font.render(str(self.playerTwoPoints), True, black)
        textRect = text.get_rect()
        resRect = result.get_rect()
        totalRect = total_results.get_rect()
        textRect.center = (96, 130)
        resRect.center = (102, 317)
        totalRect.center = (102, 247)
        self._display_surf.blit(text, textRect)
        self._display_surf.blit(result, resRect)
        self._display_surf.blit(total_results, totalRect)

        text2 = font.render(self.name2, True, black)
        result2 = font.render(str(self.playerOnePoints), True, black)
        total_results2 = font.render(str(self.playerOneTotal), True, black)
        textRect2 = text2.get_rect()
        res2Rect = result2.get_rect()
        totalRect2 = total_results2.get_rect()
        textRect2.center = (533, 122)
        res2Rect.center = (534, 195)
        totalRect2.center = (535, 272)
        self._display_surf.blit(text2, textRect2)
        self._display_surf.blit(result2, res2Rect)
        self._display_surf.blit(total_results2, totalRect2)
        pygame.display.update()

        self.playerTwoPoints = self.paws1.get_score()
        self.playerOnePoints = self.paws2.get_score()

        if self.waitEnemy.value > 20:
            self.waitEnemy.value -= 10

        wait = True
        wait2 = True # za NEXT LEVEL
        while wait and wait2: # and wait1:
            # pratiti poziciju kursora
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if 495 < mouse_pos[0] < 585 and 430 < mouse_pos[1] < 460:
                        wait2 = False
        if not wait2:
            if self.online == 1:
                self.showMazeOnline()
            else:
                self.showMaze(self.name1, self.name2)

    def showGameOver(self):

        if self.is_tournament and not self.one_winner:
            self.continue_img = pygame.image.load("GameOverTurnirContinue.jpg")
            self.screen.blit(self.continue_img, [0, 0])
        else:
            self._backgroundResult = pygame.image.load("GameOverKonacno.jpg")
            self.screen.blit(self._backgroundResult, [0, 0])

        font = pygame.font.Font('Sketch_Block.ttf', 20)
        black = (255, 255, 255)

        text = font.render(self.name1, True, black)
        result = font.render(str(self.playerTwoTotal), True, black)
        total_results = font.render(str(self.playerTwoPoints), True, black)
        textRect = text.get_rect()
        resRect = result.get_rect()
        totalRect = total_results.get_rect()
        textRect.center = (96, 130)
        resRect.center = (102, 317)
        totalRect.center = (102, 247)
        self._display_surf.blit(text, textRect)
        self._display_surf.blit(result, resRect)
        self._display_surf.blit(total_results, totalRect)

        text2 = font.render(self.name2, True, black)
        result2 = font.render(str(self.playerOnePoints), True, black)
        total_results2 = font.render(str(self.playerOneTotal), True, black)
        textRect2 = text2.get_rect()
        res2Rect = result2.get_rect()
        totalRect2 = total_results2.get_rect()
        textRect2.center = (533, 122)
        res2Rect.center = (534, 195)
        totalRect2.center = (535, 272)
        self._display_surf.blit(text2, textRect2)
        self._display_surf.blit(result2, res2Rect)
        self._display_surf.blit(total_results2, totalRect2)

        self.crown = pygame.image.load("kruna.png")
        if self.playerOneTotal < self.playerTwoTotal:
            self.screen.blit(self.crown, [29, 72])
        elif self.playerOneTotal > self.playerTwoTotal:
            self.screen.blit(self.crown, [468, 72])

        pygame.display.update()

        wait = True
        wait1 = True
        while wait and wait1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.is_tournament:
                        if 488 < mouse_pos[0] < 600 and 425 < mouse_pos[1] < 465:
                            wait1 = False
        if not wait1:
            return

    def on_render(self):
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.screen.blit(self._background, [0, 0])
        self.maze.draw(self._display_surf, self._block_surf, self._trap)
        if self.life1.value > 0:
            self.screen.blit(self.playerOne, (self.x.value, self.y.value))
        if self.life2.value > 0:
            self.screen.blit(self.playerTwo, (self.x2.value, self.y2.value))
        self.screen.blit(self.enemyOne, (self.ex1.value, self.ey1.value))
        self.screen.blit(self.enemyTwo, (self.ex2.value, self.ey2.value))

        # ispis za ime, poene i zivote igraca
        self.screen.blit(self._board, [5, 5])
        self.screen.blit(self._board, [480, 5])
        font = pygame.font.Font('freesansbold.ttf', 12)

        black = (255, 255, 255)
        text = font.render(self.name1, True, black)
        result = font.render(str(self.playerTwoPoints), True, black)
        textRect = text.get_rect()
        resRect = result.get_rect()
        textRect.center = (70, 35)
        resRect.center = (70, 55)
        self._display_surf.blit(text, textRect)
        self._display_surf.blit(result, resRect)

        text2 = font.render(self.name2, True, black)
        result2 = font.render(str(self.playerOnePoints), True, black)
        textRect2 = text2.get_rect()
        res2Rect = result2.get_rect()
        textRect2.center = (550, 35)
        res2Rect.center = (550, 55)
        self._display_surf.blit(text2, textRect2)
        self._display_surf.blit(result2, res2Rect)

        xl = 35
        yl = 65
        for i in range(0, self.life2.value):
            self._display_surf.blit(self._life, [xl, yl])
            xl = xl + 25
        xl = 515
        for i in range(0, self.life1.value):
            self._display_surf.blit(self._life, [xl, yl])
            xl = xl + 25
        pygame.display.flip()

    def redraw_window(self):
        self.check_paws()
        self.screen.blit(self._background, [0, 0])
        self.maze.draw(self._display_surf, self._block_surf, self._trap)
        self.paws1.draw(self._display_surf, self._paws_image)
        self.paws2.draw(self._display_surf, self._paws_image2)

        if self.cought1.value == 1:
            self.cought1.value = 0
            self.x.value = 379
            self.y.value = 210
        if self.cought2.value == 1:
            self.cought2.value = 0
            self.x2.value = 237
            self.y2.value = 210

        if not self.player_one_dead:
            self.screen.blit(self.playerOne, (self.x.value, self.y.value))
        if not self.player_two_dead:
            self.screen.blit(self.playerTwo, (self.x2.value, self.y2.value))

        self.screen.blit(self.enemyOne, (self.ex1.value, self.ey1.value))
        self.screen.blit(self.enemyTwo, (self.ex2.value, self.ey2.value))

        self.screen.blit(self._board, [5, 5])
        self.screen.blit(self._board, [480, 5])
        self.playerOnePoints = self.paws1.get_score()
        self.playerTwoPoints = self.paws2.get_score()

        font = pygame.font.Font('Sketch_Block.ttf', 12)
        black = (255, 255, 255)

        text = font.render(self.name1, True, black)
        result = font.render(str(self.playerTwoPoints), True, black)
        textRect = text.get_rect()
        resRect = result.get_rect()
        textRect.center = (70, 35)
        resRect.center = (70, 55)
        self._display_surf.blit(text, textRect)
        self._display_surf.blit(result, resRect)
        text2 = font.render(self.name2, True, black)
        result2 = font.render(str(self.playerOnePoints), True, black)
        textRect2 = text2.get_rect()
        res2Rect = result2.get_rect()
        textRect2.center = (550, 35)
        res2Rect.center = (550, 55)
        self._display_surf.blit(text2, textRect2)
        self._display_surf.blit(result2, res2Rect)

        xl = 35
        yl = 65
        for i in range(0, self.life2.value):
            self._display_surf.blit(self._life, [xl, yl])
            xl = xl + 25
        xl = 515
        for i in range(0, self.life1.value):
            self._display_surf.blit(self._life, [xl, yl])
            xl = xl + 25

        total = self.maze.get_total()
        #if (self.paws1.get_score() + self.paws2.get_score()) == total:
        if self.x.value > (640 - self.matW) and self.y.value > (480 - 2 * self.matH):
            self.playerOneFinished = True
            self.EnemyChase1.value = 0
        if self.x2.value > (640 - self.matW) and self.y2.value > (480 - 2 * self.matH):
            self.playerTwoFinished = True
            self.EnemyChase2.value = 0

        if self.life1.value == 0:
            self.playerOneFinished = True
            self.player_one_dead = True
            # self.p1.terminate()
        if self.life2.value == 0:
            self.playerTwoFinished = True
            self.player_two_dead = True
            # self.p2.terminate()
        if self.player_one_dead and self.player_two_dead:
            self.game_finished = True

        if self.add_force:
            self._display_surf.blit(self._life, [307, 303])
            if 303 < self.x.value < 335 and 300 < self.y.value < 330:
                self.life1.value = self.life1.value + 1
                self.add_force = False
            elif 303 < self.x2.value < 335 and 300 < self.y2.value < 330:
                self.life2.value = self.life2.value + 1
                self.add_force = False

        #kad igrac dodirne zamku, bude aktivna jos 10 sekundi i onda nestane i tad kad je neprijatelj dodirnuo setuje
        # se vrednost na 2, da bi se znalo da je zamka aktivirana
        if self.add_trap1.value == 1 or self.add_trap1.value == 2:
            self._display_surf.blit(self._trap, [87, 95])

            if 87 < self.x.value < 112 and 95 < self.y.value < 120:
                if self.add_trap1.value == 1:
                    self.add_trap1.value = 2
                    self.timer_t1 = Timer(10.0, self.timer_trap1)
                    self.timer_t1.start()

            elif 87 < self.x2.value < 112 and 95 < self.y2.value < 120:
                if self.add_trap1.value == 1:
                    self.add_trap1.value = 2
                    self.timer_t1 = Timer(10.0, self.timer_trap1)
                    self.timer_t1.start()

        if self.add_trap2.value == 1 or self.add_trap2.value == 2:
            self._display_surf.blit(self._trap, [467, 422])
            if 455 < self.x.value < 480 and 410 < self.y.value < 435:
                if self.add_trap2.value == 1:
                    self.add_trap2.value = 2
                    self.timer_t2 = Timer(10.0, self.timer_trap2)
                    self.timer_t2.start()

            elif 455 < self.x2.value < 480 and 410 < self.y2.value < 435:
                if self.add_trap2.value == 1:
                    self.add_trap2.value = 2
                    self.timer_t2 = Timer(10.0, self.timer_trap2)
                    self.timer_t2.start()

        pygame.display.update()

    def check_paws(self):
        x = self.x.value + 12
        y = self.y.value + 12
        mx = int(x // self.matW)
        my = int(y // self.matH)

        if self.paws1.get_value(mx, my) == 0 and self.paws2.get_value(mx, my) == 0:
            self.paws1.set_value(mx, my)

        x = self.x2.value + 12
        y = self.y2.value + 12
        mx = int(x // self.matW)
        my = int(y // self.matH)

        if self.paws1.get_value(mx, my) == 0 and self.paws2.get_value(mx, my) == 0:
            self.paws2.set_value(mx, my)


def read_pos1(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2])

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    cubChase = CubChase()
    sys.exit(app.exec_())