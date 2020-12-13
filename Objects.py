import math
from random import randrange

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog, \
    QPushButton
from PIL import Image, ImageDraw

SCREEN_SIZE = [1000, 1000]


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

    # draw.point((xb,yb), fill=(255,0,0))    # DEBUG: draw point of base in red - comment out draw.polygon() below if using this line
    # im.save('DEBUG-base.png')              # DEBUG: save

    # Now draw the arrowhead triangle
    draw.polygon([vtx0, vtx1, ptB], fill=color)
    # return im


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, *SCREEN_SIZE)
        self.setWindowTitle('Отображение картинки')

        ## Изображение
        self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[
            0]
        try:
            self.pixmap = QPixmap(self.fname)
        except:
            print('Это не картинка')
        # Если картинки нет, то QPixmap будет пустым,
        # а исключения не будет
        self.image = QLabel(self)
        self.image.move(80, 60)
        self.image.resize(250, 250)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)
        self.gen = QPushButton(self)
        self.gen.setText('Генерировать')
        self.gen.move(150, 0)
        self.gen.clicked.connect(self.generate)
        self.pushButton = QPushButton(self)
        self.pushButton.setText('Создать')
        self.pushButton.clicked.connect(self.save)

    def generate(self):
        im = Image.open(self.fname)
        drawer = ImageDraw.Draw(im)
        x, y = im.size
        deb = Image.open('resource/deb.jpg')
        deb = deb.resize((x // 10, y // 10))
        d_x, d_y = deb.size
        coord = (randrange(0, x - d_x), randrange(0, y - d_y))
        coord_end_line = (randrange(0, x), randrange(0, y))
        drawer.rectangle(((coord[0] - 3, coord[1] - 3),
                          (coord[0] + d_x + 3, coord[1] + d_y + 3)),
                         fill=(255, 0, 0))
        drawer.line([
            (coord[0] + (d_x // 2), coord[1] + (d_x // 2)),
            coord_end_line], fill="red", width=3)
        im.paste(deb, coord)
        im.save('tmp/tmp_deb.jpg')

    def save(self):
        pass