from random import randint
from sys import argv
from time import sleep
from webbrowser import open_new

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from organizer import *


def initwindow():
    def iniciar():
        load = 0
        while load < 100:
            janela.showMessage(f"Loading Modules: {load}%", align, Qt.GlobalColor.white)
            sleep(0.5)
            load += randint(2, 10)
        janela.close()

    img = QPixmap("./favicon/favicon-512x512.png")
    align = int(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignAbsolute)
    janela = QSplashScreen(img)
    janela.setStyleSheet(theme)
    janela.show()
    iniciar()


class G8Y:
    def __init__(self):
        self.hora = None
        self.labelHora = None
        self.gcapp = QApplication(argv)
        # QFontDatabase.addApplicationFont()

        self.janelaprincipal = QMainWindow()
        self.janelaprincipal.setWindowTitle("GCecretary - File Organizer")
        self.janelaprincipal.setFixedSize(QSize(600, 300))
        self.janelaprincipal.setStyleSheet(theme)

        # ******* hora *******
        self.timer = QTimer(self.janelaprincipal)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.mostra_hora)
        self.timer.start()

        # ******* background-image *******
        setBgImage = QImage("./favicon/bg.jpg").scaled(QSize(600, 300))
        palette = QPalette()
        palette.setBrush(palette.ColorGroup.All, palette.ColorRole.Window, QBrush(setBgImage))
        self.janelaprincipal.setPalette(palette)

        self.ferramentas = QWidget()
        menu = QMenuBar()
        detalhes = menu.addMenu("Details")
        instr = detalhes.addAction("Intructions")
        instr.triggered.connect(self._instr)
        detalhes.addSeparator()
        _sair = lambda: self.gcapp.exit(0)
        sair = detalhes.addAction("Quit")
        sair.triggered.connect(_sair)
        tools = menu.addMenu("Tools")
        createregkey = tools.addAction("Create RegKey")
        createregkey.triggered.connect(create_root_key)
        deleteregkey = tools.addAction("Delete RegKey")
        deleteregkey.triggered.connect(delete_root_key)
        sobre = menu.addAction("About")
        sobre.triggered.connect(self._sobre)

        self.layout_principal()
        self.janelaprincipal.setMenuBar(menu)
        self.janelaprincipal.setCentralWidget(self.ferramentas)
        self.janelaprincipal.show()

    def _sobre(self):
        QMessageBox.information(self.janelaprincipal, "About",
                                "<b>Info about the program</b><hr>"
                                "<p><ul><li><b>Name:</b> GCecretary - File Organizer</li>"
                                "<li><b>Version:</b> 0.1-122022</li>"
                                "<li><b>Maintener:</b> &copy;Nurul-GC</li>"
                                "<li><b>Publisher:</b> &trade;ArtesGC, Inc.</li></ul></p>")

    def _instr(self):
        QMessageBox.information(self.janelaprincipal, "Instructions",
                                "<b>Brief Presentation</b><hr>"
                                "<p>GC-liteQR is a simple and practical QR codes generator"
                                "it was built with `PyQt6 + QSS + PyQRCode` frameworks allowing the user"
                                "to easily create QR codes on his PC (offline) with three simple steps:</p>"
                                "<p>1. Type de content on the text box;<br>"
                                "2. Create the file clicking the button;<br>"
                                "3. Giving a name to the file and confirming the action;</p>"
                                "<p>The program saves the file as a PNG image and also customizes it"
                                "with different colors (automatically) each time you try to create a new one.</p>"
                                "<p>Thanks for your support!<br>"
                                "<b>&trade;ArtesGC, Inc.</b></p>")

    def definir_hora(self):
        self.hora = QDateTime()
        return self.hora.currentDateTime().toString("hh:mm:ss")  # (ap)

    def mostra_hora(self):
        self.labelHora.setText(f"<b><s>{self.definir_hora()}</s></b>")

    def layout_principal(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        self.labelHora = QLabel()
        self.labelHora.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.labelHora.setStyleSheet("padding-right:20px;")
        layout.addWidget(self.labelHora)

        mainlabel = QLabel("<h1>GCecretary</h1><hr><small>The file organizer</small>")
        mainlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(mainlabel)

        hlayout = QHBoxLayout()
        dirtorganize = QLineEdit()
        dirtorganize.setPlaceholderText("Search the folder to be organized, and get its location..")
        dirtorganize.setToolTip("As soon we get the folder, the main job will begin!")
        dirtorganize.setReadOnly(True)
        locatedirbtn = QPushButton("Search Folder")
        hlayout.addWidget(dirtorganize)
        hlayout.addWidget(locatedirbtn)
        layout.addLayout(hlayout)

        # copyright-label
        browser = lambda p: open_new('https://artesgc.home.blog')
        website = QLabel("<a href='#' style='text-decoration:none; color:white;'>™ ArtesGC, Inc.</a>")
        website.setAlignment(Qt.AlignmentFlag.AlignCenter)
        website.setToolTip('Click to access the official website of ArtesGC!')
        website.linkActivated.connect(browser)
        layout.addWidget(website)

        self.ferramentas.setLayout(layout)


if __name__ == '__main__':
    theme = open("./theme/g8y.qss").read().strip()
    app = G8Y()
    # initwindow()
    app.gcapp.exec()
