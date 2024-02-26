import sys
from PyQt5 import QtWidgets, QtCore
from PIL import ImageGrab, Image
import pytesseract

# Configure Tesseract to use the Japanese language
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'  # Path to tesseract executable
lang = 'jpn'  # Set language to Japanese

class OCRApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('OCR Results')
        self.setGeometry(300, 300, 400, 300)  # Set window size and position
        self.setWindowOpacity(0.8)  # Set the transparency level
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.label = QtWidgets.QLabel(self)
        self.label.setWordWrap(True)

        # Set up the timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_ocr_results)
        self.timer.start(5000)  # Update interval in milliseconds (5000ms = 5s)

    def update_ocr_results(self):
        # Specify the screen area to capture (top-left and bottom-right coordinates)
        capture_area = (145, 625, 1106, 655)  # Example coordinates
        captured_image = self.capture_screen_area(*capture_area)
        captured_image.save('captured_image.png')
        print("Capturing screen area...")
        text = self.ocr_image(captured_image)
        print("OCR results:", text)
        self.label.setText(text)

    def capture_screen_area(self, x1, y1, x2, y2):
        """Captures a portion of the screen given by the top-left coordinates (x1, y1)
        and bottom-right coordinates (x2, y2)."""
        return ImageGrab.grab(bbox=(x1, y1, x2, y2))

    def ocr_image(self, image):
        return pytesseract.image_to_string(image, lang=lang)

# Create the application object
app = QtWidgets.QApplication(sys.argv)
ex = OCRApp()
ex.show()
sys.exit(app.exec_())
