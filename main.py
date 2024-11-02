import sys
import socket
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView


class CustomBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("wjs Browser")
        self.setGeometry(100, 100, 1200, 800)

        # URL 입력 필드와 버튼
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter URL (wjs:// format)")
        
        self.go_button = QPushButton("Go", self)
        self.go_button.clicked.connect(self.load_url)

        # 웹 브라우저 뷰
        self.browser = QWebEngineView(self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.url_input)
        layout.addWidget(self.go_button)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_url(self):
        url = self.url_input.text().strip()  # 입력된 URL에서 공백 제거
        
        # wjs://로 시작하면 서버에 요청
        if url.startswith("wjs://"):
            # wjs://을 제거하고 path만 서버에 요청
            path = url.replace("wjs://", "", 1)
            server_host = "113.10.30.60"  # 서버 IP
            server_port = 12346           # 서버 포트 번호
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((server_host,server_port))
                client_socket.sendall(path.encode())
                data = client_socket.recv(1024)
                url = 'https://'+data.decode()
                self.browser.setUrl(QUrl(url))
        else:
            # http 또는 https가 아닌 경우 기본적으로 http 추가
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url

            self.browser.setUrl(QUrl(url))

# PyQt5 애플리케이션 실행
app = QApplication(sys.argv)
window = CustomBrowser()
window.show()
sys.exit(app.exec_())
