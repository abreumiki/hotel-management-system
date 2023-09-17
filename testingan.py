# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QCheckBox
# from PyQt5.QtGui import QFont
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle("Checkbox Example")
#         self.setGeometry(100, 100, 200, 200)
#
#         self.widget = QWidget(self)  # Existing widget as a container
#         self.layout = QVBoxLayout(self.widget)
#
#         self.names = ['John', 'Alice', 'Bob']  # Replace with your list of names
#         self.createCheckboxes()
#
#     def createCheckboxes(self):
#         for name in self.names:
#             checkbox = QCheckBox(name)
#             checkbox.setFont(QFont("Century Gothic", 10))  # Set font to Century Gothic, size 10
#             checkbox.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")  # Set checkbox size
#             self.layout.addWidget(checkbox)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())


def calculate_payment(hours):
    minimum_hours = 12
    minimum_payment = 1000
    payment_per_multiple = 1000  # Additional payment per multiple of minimum hours

    if hours <= minimum_hours:
        return minimum_payment

    additional_hours = hours - minimum_hours
    additional_payment = (additional_hours // minimum_hours) * payment_per_multiple

    total_payment = minimum_payment + additional_payment
    return total_payment

hours_stayed = 5
total_payment = calculate_payment(hours_stayed)
print("Total payment:", total_payment)