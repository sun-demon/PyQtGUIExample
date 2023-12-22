import math
import pyqtgraph as pg
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


author_image_name = 'image/icon-sun-demon.png'


# def image_to_bitmap(image_name: str) -> list:
#     with Image.open(image_name) as image:
#         return [image.getpixel((x, y_)) for x in range(image.width) for y_ in range(image.height)]


class Product:
    def __init__(self, name: str, cost: float):
        if name == '':
            raise RuntimeError('Product name must be not zero string')
        self.__product_name__ = name
        if cost < 0:
            raise RuntimeError('Product cost must be zero or positive')
        self.__cost__ = cost

    def __str__(self) -> str:
        return f'{self.__product_name__}'

    def name(self) -> str:
        return self.__product_name__

    def cost(self) -> float:
        return self.__cost__

    def __lt__(self, other):
        is_name_equal = self.name() == other.name()
        if not is_name_equal:
            return self.name() < other.name()
        return self.cost() < other.cost()


# sin(x - 1) != 0
def is_in_definition(x: float) -> bool:
    return math.sin(x - 1) != 0


# y = |sin(5*x)|/sin(x-1)
def y(x: float) -> float:
    return math.fabs(math.sin(5 * x)) / math.sin(x - 1)


# x in range(-2*PI,2*PI,1e-6)
def plot_data() -> (list, list):
    x_min, x_max = -2 * math.pi, 2 * math.pi
    x_step = 1e-3
    x_array = [x_small * x_step for x_small in range(math.ceil(x_min / x_step), math.ceil(x_max / x_step))
               if is_in_definition(x_small * x_step)]
    y_array = [math.fabs(math.sin(5 * x)) / math.sin(x - 1) for x in x_array]
    return x_array, y_array


def about_author(*args, **kwargs) -> None:
    message_box = QMessageBox(text='FCs: Demin Daniil Petrovich\n'
                                   'Specialty: software engineering\n'
                                   'Group: IMK4-32B')
    message_box.setWindowTitle('About author')
    message_box.setIcon(QMessageBox.Icon.Information)
    message_box.exec()


def find_widget_by_object_name(layout: QLayout, object_name: str) -> QWidget | None:
    for i in range(layout.count()):
        if layout.itemAt(i).widget().objectName() == object_name:
            return layout.itemAt(i).widget()
    return None


class ProductsWindow(QMainWindow):
    def __init__(self, products_set: set):
        super().__init__()

        self.setWindowTitle("Home work №1")
        central_widget = QWidget()
        central_widget.setLayout(QVBoxLayout())

        plot_widget = pg.PlotWidget()
        plot_widget.objectName = lambda: 'plot'
        plot_widget.plot(*plot_data())

        products_widget = QScrollArea()
        products_widget.setObjectName('products')
        grid_layout = QGridLayout()
        for i, product in enumerate(sorted(products_set)):
            grid_layout.addWidget(QCheckBox(product.name()), i, 0)
            grid_layout.addWidget(QLabel(str(product.cost())), i, 1)
        products_widget.setLayout(grid_layout)

        purchase_widget = QPushButton('price')
        purchase_widget.setObjectName('price')
        purchase_widget.clicked.connect(lambda: self.purchase())

        products_and_purchase_widget = QWidget()
        products_and_purchase_widget.setObjectName('products and price')
        products_and_purchase_widget.setLayout(QHBoxLayout())
        products_and_purchase_widget.layout().addWidget(products_widget)
        products_and_purchase_widget.layout().addWidget(purchase_widget)

        author_widget = QLabel()
        author_widget.setObjectName('author')
        author_widget.setPixmap(QPixmap(author_image_name).scaled(100, 100))
        author_widget.mousePressEvent = about_author
        author_widget.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        for widget in [plot_widget, products_and_purchase_widget, author_widget]:
            central_widget.layout().addWidget(widget)
        self.setCentralWidget(central_widget)

    def purchase(self):
        price = 0.00
        products_and_purchase_widget = find_widget_by_object_name(self.centralWidget().layout(), 'products and price')
        products_widget = find_widget_by_object_name(products_and_purchase_widget.layout(), 'products')
        for i in range(products_widget.layout().rowCount()):
            if products_widget.layout().itemAtPosition(i, 0).widget().isChecked():
                price += float(products_widget.layout().itemAtPosition(i, 1).widget().text())
        message_box = QMessageBox(text=f'Price:  {price}')
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.exec()


def products() -> set:
    return {
        Product('coffee', 19.22),
        Product('cake', 22.10),
        Product('pie', 20.80),
        Product('ice cream', 11.40),
        Product('tea', 10.35)
    }


def main():
    app = QApplication(sys.argv)
    window = ProductsWindow(products())
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
