from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication, QPushButton, QLineEdit)
from PyQt5.QtCore import (Qt, QSize)
from PyQt5.QtGui import (QPixmap, QIcon)
from multiprocessing import Process, Queue, Value
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
        self._paws_image = None
        self._paws_image2 = None
        self.screen = None
        self.playerOne = None
        self.playerTwo = None
        self.enemyOne = None
        self.enemyTwo = None
        self.playerOneFinished = False
        self.playerTwoFinished = False

        self.windowWidth = 640
        self.windowHeight = 480
        self.x = Value('i', 379)
        self.y = Value('i', 210)
        self.x2 = Value('i', 237)
        self.y2 = Value('i', 210)
        self.ex1 = Value('i', 437)
        self.ey1 = Value('i', 390)
        self.ex2 = Value('i', 175)
        self.ey2 = Value('i', 390)
        self.life1 = Value('i', 3)
        self.life2 = Value('i', 3)
        self.width = 25
        self.height = 25
        self.vel = 3
        self.matW = 640 / 22
        self.matH = 480 / 16
        self.run = True

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
        self.txtbox1.resize(93, 23)
        self.txtbox1.setStyleSheet('background-color: #f5deb3; border: 2px solid teal; font: Bold')
        self.txtbox1.setAlignment(Qt.AlignCenter)
        self.txtbox1.setVisible(False)

        self.txtbox2 = QLineEdit(self)
        self.txtbox2.move(344, 315)
        self.txtbox2.resize(93, 23)
        self.txtbox2.setStyleSheet('background-color: #f5deb3; border: 2px solid teal; font: Bold')
        self.txtbox2.setAlignment(Qt.AlignCenter)
        self.txtbox2.setVisible(False)

        self.btn = QPushButton('', self)
        self.btn.clicked.connect(self.showDialog)
        self.btn.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.setIconSize(QSize(89, 46))
        self.btn.resize(100, 50)
        self.btn.move(120, 323)

        self.btn1 = QPushButton('', self)
        self.btn1.setVisible(False)

        self.show()

    def showDialog(self):
        self.pixmap = QPixmap("pozadina2.png")
        self.lbl.setPixmap(self.pixmap)

        self.txtbox1.setVisible(True)
        self.txtbox2.setVisible(True)

        self.btn1.setVisible(True)
        self.btn1.setText('')
        self.btn1.resize(150, 50)
        self.btn1.move(100, 400)
        self.btn1.setIcon(QIcon("startdugme.jpg"))
        self.btn1.setIconSize(QSize(89, 46))
        self.btn1.resize(93, 50)
        self.btn1.move(285, 355)
        self.btn1.setCursor(Qt.PointingHandCursor)
        self.btn1.clicked.connect(self.showMaze)
        self.show()

    def showMaze(self):
        self.hide()
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
        self.on_render()

        q1input = Queue()
        q2input = Queue()
        quit_queue = Queue()

        p1 = Process(target=PlayerProcess.player_function, args=(self.x, self.y, q1input, quit_queue))
        p2 = Process(target=PlayerProcess.player_function, args=(self.x2, self.y2, q2input, quit_queue))
        p3 = Process(target=EnemyProcess.move_enemy, args=(self.ex1, self.ey1, self.x, self.y, self.x2, self.y2,
                                                           quit_queue, self.life1, self.life2))
        p4 = Process(target=EnemyProcess.move_enemy, args=(self.ex2, self.ey2, self.x2, self.y2, self.x, self.y,
                                                           quit_queue, self.life2, self.life1))
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        #do = True

        while not self.playerOneFinished or not self.playerTwoFinished:
            pygame.time.delay(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    do = False
                    quit_queue.put(1)

            keys = pygame.key.get_pressed()

            if not self.playerOneFinished:
                if keys[pygame.K_LEFT]:
                    q1input.put(1)
                if keys[pygame.K_RIGHT]:
                    q1input.put(2)
                if keys[pygame.K_UP]:
                    q1input.put(3)
                if keys[pygame.K_DOWN]:
                    q1input.put(4)

            if not self.playerTwoFinished:
                if keys[pygame.K_a]:
                    q2input.put(1)
                if keys[pygame.K_d]:
                    q2input.put(2)
                if keys[pygame.K_w]:
                    q2input.put(3)
                if keys[pygame.K_s]:
                    q2input.put(4)

            self.redraw_window()

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        pygame.quit()

    def on_render(self):
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.screen.blit(self._background, [0, 0])
        self.maze.draw(self._display_surf, self._block_surf)
        self.screen.blit(self.playerOne, (self.x.value, self.y.value))
        self.screen.blit(self.playerTwo, (self.x2.value, self.y2.value))
        self.screen.blit(self.enemyOne, (self.ex1.value, self.ey1.value))
        self.screen.blit(self.enemyTwo, (self.ex2.value, self.ey2.value))
        pygame.display.flip()

    def redraw_window(self):
        self.check_paws()
        self.screen.blit(self._background, [0, 0])
        self.maze.draw(self._display_surf, self._block_surf)
        self.paws1.draw(self._display_surf, self._paws_image)
        self.paws2.draw(self._display_surf, self._paws_image2)
        self.screen.blit(self.playerOne, (self.x.value, self.y.value))
        self.screen.blit(self.playerTwo, (self.x2.value, self.y2.value))
        self.screen.blit(self.enemyOne, (self.ex1.value, self.ey1.value))
        self.screen.blit(self.enemyTwo, (self.ex2.value, self.ey2.value))

        if self.life1.value == 0:
            self.playerOneFinished = True
            #self.p1.terminate()
        if self.life2.value == 0:
            self.playerTwoFinished = True
            #self.p2.terminate()
        pygame.display.update()

    def check_paws(self):
        mx1 = int(self.x.value // self.matW)
        mx2 = int((self.x.value + self.width) // self.matW)
        my1 = int((self.y.value + self.height) // self.matH)
        my2 = int(self.y.value // self.matH)
        val111 = self.paws1.get_value(mx1, my1)
        val112 = self.paws1.get_value(mx2, my1)
        val113 = self.paws1.get_value(mx1, my2)
        val114 = self.paws1.get_value(mx2, my2)
        val121 = self.paws2.get_value(mx1, my1)
        val122 = self.paws2.get_value(mx2, my1)
        val123 = self.paws2.get_value(mx2, my1)
        val124 = self.paws2.get_value(mx2, my2)
        if val111 == 0 and val112 == 0 and val113 == 0 and val114 == 0 and val121 == 0 and val122 == 0 and val123 == 0 \
                and val124 == 0:
            self.paws1.set_value(mx1, my1)

        mx1 = int(self.x2.value // self.matW)
        mx2 = int((self.x2.value + self.width) // self.matW)
        my1 = int((self.y2.value + self.height) // self.matH)
        my2 = int(self.y2.value // self.matH)
        val111 = self.paws1.get_value(mx1, my1)
        val112 = self.paws1.get_value(mx2, my1)
        val113 = self.paws1.get_value(mx1, my2)
        val114 = self.paws1.get_value(mx2, my2)
        val121 = self.paws2.get_value(mx1, my1)
        val122 = self.paws2.get_value(mx2, my1)
        val123 = self.paws2.get_value(mx2, my1)
        val124 = self.paws2.get_value(mx2, my2)
        if val111 == 0 and val112 == 0 and val113 == 0 and val114 == 0 and val121 == 0 and val122 == 0 and val123 == 0 \
                and val124 == 0:
            self.paws2.set_value(mx1, my1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cubChase = CubChase()
    sys.exit(app.exec_())