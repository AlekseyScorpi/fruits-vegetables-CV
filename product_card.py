from PyQt5.QtWidgets import QListWidgetItem, QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from math import floor

class ProductCard(QWidget):
    def __init__(self, product_info: dict) -> None:
        """Init Product Card QWidget
        
        Args:
            product_info (dict): dictionary which are responding to one product and contains next fields: name, image, price and discount
        """
        
        super().__init__()
        
        self.name = product_info['name']
        self.image = product_info['image']
        self.price = product_info['price']
        self.discount = product_info['discount']

        main_layout = QHBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap.fromImage(QImage.fromData(self.image)).scaled(100, 100))

        right_layout = QVBoxLayout()
        
        self.name_label = QLabel(f"Товар: {self.name}")
        
        self.price_label = QLabel(f"{self.price}")
        self.update_price_label()

        right_layout.addWidget(self.name_label)
        right_layout.addWidget(self.price_label)

        main_layout.addWidget(self.image_label)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)
        
    def update_price_label(self) -> None:
        if self.discount > 0:
            self.price_label.setText(
                f"<s>{self.price : .2f} руб.</s> <b>{round_floor((1 - self.discount) * self.price, 2)} руб.</b>"
            )
        else:
            self.price_label.setText(f"{self.price} руб.")

        self.price_label.setStyleSheet("font-size: 16px; color: black;")
     
        
def add_product_to_list(product_list_widget, product_info) -> None:
    item = QListWidgetItem(product_list_widget)
    
    product_card = ProductCard(product_info)
    
    item.setSizeHint(product_card.sizeHint())
    
    product_list_widget.setItemWidget(item, product_card)
    
    item.setData(Qt.UserRole, product_info)

def round_floor(value: float, decimals: int) -> float:
    """rounds the float number (by floor rule) to the specified precision

    Args:
        value (float): original float value
        decimals (int): precision

    Returns:
        float: rounded float number
    """
    if decimals <= 0:
        return floor(value)
    
    factor = 10 ** decimals
    return floor(value * factor) / factor