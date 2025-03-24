import sys
import design
import cv2
import os
from dotenv import load_dotenv
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QMessageBox
from ultralytics import YOLO
import random
import time
from product_card import add_product_to_list, round_floor
from query_engine import QueryEngine


class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self) -> None:
        """Init function for App
        """
        super().__init__()
        self.setupUi(self)
        
        random.seed(time.time())
        
        self.cap = cv2.VideoCapture(0)
        self.camera_scene = QGraphicsScene()
        self.camera_view.setScene(self.camera_scene)
        self.camera_timer = QTimer(self)
        
        display_function = self.display_image_stream if os.getenv('DEBUG', default="FALSE") == "TRUE" else self.display_image
        
        self.camera_timer.timeout.connect(display_function)
        self.camera_timer.start(30)
        
        self.product_weight = 0.0
        self.model = YOLO('./weights_small/best.pt') if os.getenv('MODEL', default='SMALL') == 'SMALL' else YOLO('./weights_nano/best.pt')
        self.predict_button.clicked.connect(lambda: self.predict_image())
        self.receipt_button.clicked.connect(self.print_receipt)
        
        self.query_engine = QueryEngine(
            dbname=os.getenv('DATABASE_DBNAME', default='default'),
            user=os.getenv('DATABASE_USERNAME', default='postgres'),
            password=os.getenv('DATABASE_PASSWORD', default='postgres'),
            host=os.getenv('DATABASE_HOST', default='localhost'),
            port=os.getenv('DATABASE_PORT', default=5432)
        )
    
    def __get_random_weight(self, start=0, end=5) -> float:
        """This function are using to generate realistic random weights for product
        In future version it won't be needed, because expected using really scales and get data from it

        Args:
            start (int, optional): minimum weights. Defaults to 0.
            end (int, optional): maximum weights. Defaults to 5.

        Returns:
            float: random weigths of product which rounded to 3 number after point (precision kg and gramms)
        """
        return round_floor(random.uniform(start, end), 3)
    
    def print_receipt(self) -> None:
        selected_item = self.products_list.currentItem()
        if selected_item is None:
            QMessageBox.warning(self, "Ошибка", "Не выбран ни один товар.")
            return

        product_info = selected_item.data(Qt.UserRole)

        if product_info is None:
            QMessageBox.warning(self, "Ошибка", "Не удалось получить информацию о товаре.")
            return
        
        product_name = product_info['name']
        product_price = round_floor(float((1 - product_info['discount']) * product_info['price']), 2)
        weight = self.product_weight
        total_price = product_price * weight
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Печать чека")
        msg.setText(f"Товар: {product_name}\nЦена за кг: {product_price} руб\nВес: {weight} кг\nСумма: {round_floor(total_price, 2)} руб")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    
    def predict_image(self, frames: int = 5) -> None:
        """This functions is using to predict product from camera frame(s)
        Next step is get info about detected products from database with using query_engine
        Finally it adds product to products list
        
        Args:
            frames (int, optional): number of frames which are using to predict product. Defaults to 5.
        """
        self.products_list.clear()
        products = []
        detected_classes = set()
        for _ in range(frames):
            ret, frame = self.cap.read()
            if not ret:
                continue
            frame_resized = cv2.resize(frame, (640, 640))
            results = self.model(frame_resized, conf=0.5)
            classes = results[0].boxes.cls
            for class_id in classes:
                detected_classes.add(self.model.names[int(class_id)])
        
        if len(detected_classes) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Внимание")
            msg.setText(f"Продукты не обнаружены")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        
        try:
            products = self.query_engine.get_products_info(detected_classes)
            
            for product in products:
                add_product_to_list(self.products_list, product)
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Ошибка")
            msg.setText(f"Сейчас невозможно получить информацию о продуктах")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
                
        # set random weights for trial version
        weight = self.__get_random_weight()
        self.product_weight = weight
        self.weights_label.setText(f"Вес товара: {self.product_weight : .3f} кг")
    
    def display_image(self) -> None:
        """This function gets image data from camera and displays it on GUI
        """
        ret, frame = self.cap.read()
        if ret:
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_img)

            self.camera_scene.clear()
            self.camera_scene.addPixmap(pixmap)
        
    def display_image_stream(self) -> None:
        """WARNING - this function are used for testing program and it doesn't involve use in the release version
        This function gets image data from camera and displays it on GUI
        In addition it makes prediction by each frame and displays boxes and probabilities of detected classes
        """
        ret, frame = self.cap.read()
        if ret:
            
            frame_resized = cv2.resize(frame, (640, 640))
            
            results = self.model(frame_resized, conf=0.5)
            
            for result in results:
                boxes = result.boxes.xyxy
                confidences = result.boxes.conf
                classes = result.boxes.cls

                for box, conf, cls in zip(boxes, confidences, classes):
                    x1, y1, x2, y2 = map(int, box)
                    label = f"{self.model.names[int(cls)]} {conf:.2f}"
                    
                    height_orig, width_orig = frame.shape[:2]
                    x1 = int(x1 * (width_orig / 640))
                    y1 = int(y1 * (height_orig / 640))
                    x2 = int(x2 * (width_orig / 640))
                    y2 = int(y2 * (height_orig / 640))

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qt_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_img)

            self.camera_scene.clear()
            self.camera_scene.addPixmap(pixmap)
            
def main() -> None:
    """Main function to create the application instance and run it
    """
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()

if __name__ == "__main__":
    load_dotenv(override=True)
    main()