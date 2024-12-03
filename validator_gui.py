# -*- coding: utf-8 -*-
import sys
import socket
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFormLayout, QMessageBox, QColorDialog
)
from PyQt5.QtGui import QIntValidator, QIcon

def send_udp_message(ip, port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(message.encode(), (ip, port))
    client_socket.close()

def is_valid_ip(ip):
    regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(regex, ip) is not None

class ClientApp(QWidget):
    def __init__(self):
        super(ClientApp, self).__init__()
        self.selected_color = "#000000"  # Default hali siyah
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('UDP Kullanıcı Girişi')
        self.setGeometry(300, 300, 400, 400)

        # App Icon Ayarı
        self.setWindowIcon(QIcon('/Users/emrekoy/Desktop/app_icon_yeni.png'))  

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText('IP Adresi (e.g., 192.168.1.1)')
        self.ip_input.setInputMask('000.000.000.000;_')  

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText('Port Numarası (e.g., 8080)')
        self.port_input.setValidator(QIntValidator(0, 65535, self))  

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText('Mesajınızı Girin')

        self.color_button = QPushButton('Mesaj Rengini Seç')
        self.color_button.clicked.connect(self.select_color)

        form_layout.addRow('IP Address:', self.ip_input)
        form_layout.addRow('Port:', self.port_input)
        form_layout.addRow('Message:', self.message_input)
        form_layout.addRow(self.color_button)

        self.send_button = QPushButton('Mesajı Gönder')
        self.send_button.clicked.connect(self.handle_send)

        self.result_label = QLabel('')
        layout.addLayout(form_layout)
        layout.addWidget(self.send_button)
        layout.addWidget(self.result_label)
        
        self.setLayout(layout)

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color.name()

    def handle_send(self):
        ip = self.ip_input.text()
        port = self.port_input.text()
        message = self.message_input.text()

        if not is_valid_ip(ip):
            self.result_label.setText('Geçersiz IP Adresi!')
            self.result_label.setStyleSheet("color: red;")
            return

        if not port.isdigit():
            self.result_label.setText('Geçersiz Port!')
            self.result_label.setStyleSheet("color: red;")
            return

        if not message:
            self.result_label.setText('Lütfen Mesajınızı Giriniz!')
            self.result_label.setStyleSheet("color: red;")
            return

        # Portu integer'a çevirme
        port = int(port)

        # Mesajı ve renk kodunu birleştiriyoruz
        message_with_color = f"{message} | Renk Kodu : {self.selected_color}"

        confirmation = QMessageBox.question(
            self, "Confirmation",
            f"IP: {ip}\nPort: {port}\n\nMessage: {message_with_color}\n\nBu girdiler doğru mu?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            send_udp_message(ip, port, message_with_color)
            self.result_label.setText(f'Mesaj Gönderildi : {ip} , Port: {port}')
            self.result_label.setStyleSheet("color: green;")
        else:
            self.result_label.setText('Operation Cancelled.')
            self.result_label.setStyleSheet("color: red;")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # App Icon Ayarı
    app.setWindowIcon(QIcon('/Users/emrekoy/Desktop/app_icon_yeni.png'))  # Buraya simge dosyasının yolunu yazın.

    window = ClientApp()
    window.show()
    sys.exit(app.exec_())
