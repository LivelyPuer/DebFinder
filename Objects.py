import math
from random import randrange

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QMainWindow, QFileDialog, \
    QPushButton, QSpinBox
from PIL import Image, ImageDraw

SCREEN_SIZE = [700, 700]


def arrowedLine(im, ptA, ptB, width=1, color=(0, 255, 0)):
    """Draw line from ptA to ptB with arrowhead at ptB"""
    # Get drawing context
    draw = ImageDraw.Draw(im)
    # Draw the line without arrows
    draw.line((ptA, ptB), width=width, fill=color)

    # Now work out the arrowhead
    # = it will be a triangle with one vertex at ptB
    # - it will start at 95% of the length of the line
    # - it will extend 8 pixels either side of the line
    x0, y0 = ptA
    x1, y1 = ptB
    # Now we can work out the x,y coordinates of the bottom of the arrowhead triangle
    xb = 0.95 * (x1 - x0) + x0
    yb = 0.95 * (y1 - y0) + y0

    # Work out the other two vertices of the triangle
    # Check if line is vertical
    alpha = math.atan2(y1 - y0, x1 - x0) - 90 * math.pi / 180
    a = 8 * math.cos(alpha)
    b = 8 * math.sin(alpha)
    vtx0 = (xb + a, yb + b)
    vtx1 = (xb - a, yb - b)

    # Now draw the arrowhead triangle
    draw.polygon([vtx0, vtx1, ptB], fill=color)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, *SCREEN_SIZE)
        self.setWindowTitle('Отображение картинки')

        ## Изображение
        self.fname = 'resource/deb.jpg'
        self.image = QLabel(self)
        self.image.move(10, 0)
        self.image.resize(680, 740)
        self.print_image('resource/deb.jpg')

        self.gen = QPushButton(self)
        self.gen.setText('Генерировать')
        self.gen.move(150, 0)
        self.gen.clicked.connect(self.generate)

        self.pushButton = QPushButton(self)
        self.pushButton.setText('Сохранить')
        self.pushButton.clicked.connect(self.save)

        self.sel = QPushButton(self)
        self.sel.setText('Выбрать файл')
        self.sel.move(300, 0)
        self.sel.clicked.connect(self.select)

        self.n = QSpinBox(self)
        self.n.move(450, 0)
        self.n.setValue(1)
        self.n.setMinimum(1)
        self.n.setMaximum(50)

        self.generate()

    def select(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[
            0]
        try:
            self.pixmap = QPixmap(self.fname)
        except:
            print('Это не картинка')
        # Если картинки нет, то QPixmap будет пустым,
        # а исключения не будет
        self.generate()

    def generate(self):
        if self.fname:
            self.im = Image.open(self.fname)
            drawer = ImageDraw.Draw(self.im)
            x, y = self.im.size
            deb = Image.open('resource/deb.jpg')
            deb = deb.resize((x // 10, y // 10))
            d_x, d_y = deb.size
            for i in range(self.n.value()):
                coord = (randrange(0, x - d_x), randrange(0, y - d_y))
                coord_end_line = (randrange(0, x), randrange(0, y))
                drawer.rectangle(((coord[0] - 3, coord[1] - 3),
                                  (coord[0] + d_x + 3, coord[1] + d_y + 3)),
                                 fill=(255, 0, 0))
                arrowedLine(self.im,
                            (coord[0] + (d_x // 2), coord[1] + (d_x // 2)),
                            coord_end_line, color="red", width=3)
                self.im.paste(deb, coord)
            self.im.save('tmp/tmp_deb.png')
            self.print_image('tmp/tmp_deb.png')
            return x, y
        return 0, 0

    def save(self):
        try:
            SaveFileDiolog = QFileDialog. \
                getSaveFileName(self,
                                'Сохранить', 'unnamed.png',
                                'Картинка (*.jpg; *.jpeg; *.png; *.jfif);')
            print(SaveFileDiolog[0])
            self.im.save(SaveFileDiolog[0])
            self.statusBar().setStyleSheet("background-color : green")
            self.statusBar().showMessage(
                'Сохранено успешно в {}'.format(SaveFileDiolog), 100)
        except:
            self.statusBar().setStyleSheet("background-color : red")
            self.statusBar().showMessage('Ошибка при сохранении!', 100)

    def print_image(self, path):
        self.pixmap = QPixmap(path)
        print(path)
        k = 1
        if self.pixmap.width() >= SCREEN_SIZE[0]:
            k = SCREEN_SIZE[0] / (self.pixmap.width() + 20)
        self.pixmap = self.pixmap.scaled(int(self.pixmap.width() * k),
                                         int(self.pixmap.height() * k))
        self.image.setPixmap(self.pixmap)
