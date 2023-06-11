import sys
from PyQt6.QtWidgets import  QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QStackedWidget, QStyleFactory, QGroupBox
from PyQt6.QtGui import QIcon

class InstallationTab(QWidget):
    def __init__(self):
        super().__init__()

         # Розділ "Browsers"
        browsers_groupbox = QGroupBox('Browsers')
        browsers_layout = QVBoxLayout()
        browsers_checkboxes = [
            QCheckBox('Google Chrome'),
            QCheckBox('Mozilla Firefox'),
            QCheckBox('Microsoft Edge')
        ]
        for checkbox in browsers_checkboxes:
            browsers_layout.addWidget(checkbox)
        browsers_groupbox.setLayout(browsers_layout)
        layout.addWidget(browsers_groupbox)

        # Розділ "Messengers"
        messengers_groupbox = QGroupBox('Messengers')
        messengers_layout = QVBoxLayout()
        messengers_checkboxes = [
            QCheckBox('WhatsApp'),
            QCheckBox('Telegram'),
            QCheckBox('Skype')
        ]
        for checkbox in messengers_checkboxes:
            messengers_layout.addWidget(checkbox)
        messengers_groupbox.setLayout(messengers_layout)

        layout.addWidget(messengers_groupbox)

        self.setLayout(layout)

class TweaksTab(QWidget):
    def __init__(self):
        super().__init__()


class ConfigurationTab(QWidget):
    def __init__(self):
        super().__init__()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Service')
        self.setFixedSize(640, 480)

        #Встановлюємо тему вікон Fusion
        QApplication.setStyle(QStyleFactory.create("Fusion"))

        # Встановлюємо іконку для вікна
        icon = QIcon('src\server.png')
        self.setWindowIcon(icon)

        # Створюємо контейнер вкладок
        self.tab_widget = QStackedWidget()

        # Головна вкладка - Інсталяція
        self.installation_tab = InstallationTab()
        self.tab_widget.addWidget(self.installation_tab)

        # Вкладка - Tweaks
        self.tweaks_tab = TweaksTab()
        self.tab_widget.addWidget(self.tweaks_tab)

        # Вкладка - Конфігурація
        self.configuration_tab = ConfigurationTab()
        self.tab_widget.addWidget(self.configuration_tab)


        # Створюємо кнопки меню
        self.installation_button = QPushButton('Install')
        self.tweaks_button = QPushButton('Tweaks')
        self.configuration_button = QPushButton('Config')

        # Встановлюємо активну вкладку при натисканні кнопок меню
        self.installation_button.clicked.connect(self.show_installation_tab)
        self.tweaks_button.clicked.connect(self.show_tweaks_tab)
        self.configuration_button.clicked.connect(self.show_configuration_tab)

        # Створюємо головний контейнер
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.installation_button)
        button_layout.addWidget(self.tweaks_button)
        button_layout.addWidget(self.configuration_button)

        main_layout.addLayout(button_layout)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)



    def show_installation_tab(self):
        self.tab_widget.setCurrentWidget(self.installation_tab)

    def show_tweaks_tab(self):
        self.tab_widget.setCurrentWidget(self.tweaks_tab)

    def show_configuration_tab(self):
        self.tab_widget.setCurrentWidget(self.configuration_tab)

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
