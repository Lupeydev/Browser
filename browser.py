from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

class MyWebBrowser(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MyWebBrowser, self).__init__(*args, **kwargs)

        self.setWindowTitle("Web Browser V1")
        self.resize(1200, 800) 

        self.home_url = "https://www.google.com"  

        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        self.back_btn = QPushButton("<")
        self.back_btn.setMinimumHeight(30)

        self.forward_btn = QPushButton(">")
        self.forward_btn.setMinimumHeight(30)

        self.home_btn = QPushButton("🏠")  
        self.home_btn.setMinimumHeight(30)

        self.refresh_btn = QPushButton("⟳")
        self.refresh_btn.setMinimumHeight(30)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL...")
        self.url_bar.setMinimumHeight(30)

        self.go_btn = QPushButton("Go")
        self.go_btn.setMinimumHeight(30)
        
        self.horizontal.addWidget(self.back_btn)
        self.horizontal.addWidget(self.forward_btn)
        self.horizontal.addWidget(self.refresh_btn)       
        self.horizontal.addWidget(self.home_btn)
        self.horizontal.addWidget(self.url_bar, 1) 
        self.horizontal.addWidget(self.go_btn)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(self.home_url))


        self.browser.page().profile().downloadRequested.connect(self.on_download_requested)

        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.go_btn.clicked.connect(self.navigate_to_url)
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.home_btn.clicked.connect(self.navigate_home)
        self.refresh_btn.clicked.connect(self.browser.reload)
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.browser.urlChanged.connect(self.update_url)

        QShortcut(QKeySequence("Ctrl+Q"), self, activated=self.close)

    def on_download_requested(self, download):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", download.path())
        if path:
            download.setPath(path)
            download.accept()  

            download.downloadProgress.connect(self.download_progress)
            download.finished.connect(self.download_finished)

    def download_progress(self, received, total):
        print(f"Downloaded {received}/{total} bytes")

    def download_finished(self):
        print("Download finished!")
    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if url and not url.startswith(("http://", "https://")):
            url = "https://" + url  
        self.browser.setUrl(QUrl(url))

    def navigate_home(self):
        self.browser.setUrl(QUrl(self.home_url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

app = QApplication([])
window = MyWebBrowser()
window.show()
app.exec_()
