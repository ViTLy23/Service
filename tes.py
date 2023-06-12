import sys
import json
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QCheckBox, QGroupBox, QHBoxLayout, QVBoxLayout, QWidget, QTabWidget, QPushButton, QTextEdit
from PyQt6.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Installer")
        self.resize(640, 480)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.load_installation_data()
        self.create_tabs()

    def load_installation_data(self):
        with open("data.json", "r") as file:
            self.installation_data = json.load(file)

    def create_tabs(self):
        tab_widget = QTabWidget(self.central_widget)

        install_tab = self.create_install_tab()
        tweaks_tab = self.create_tweaks_tab()
        config_tab = self.create_config_tab()

        tab_widget.addTab(install_tab, QIcon("install_icon.png"), "Install")
        tab_widget.addTab(tweaks_tab, QIcon("tweaks_icon.png"), "Tweaks")
        tab_widget.addTab(config_tab, QIcon("config_icon.png"), "Config")

        self.layout.addWidget(tab_widget)

    def create_install_tab(self):
        installation_tab = QWidget(self)

        layout = QVBoxLayout(installation_tab)
        installation_tab.setObjectName("Install")

        for section, programs in self.installation_data.items():
            group_box = QGroupBox(section)

            group_layout = QHBoxLayout()
            for program in programs:
                name = program["name"]
                checkbox = QCheckBox(name)
                group_layout.addWidget(checkbox)

            group_box.setLayout(group_layout)
            layout.addWidget(group_box)

        install_button = QPushButton("Install")
        install_button.clicked.connect(self.install_selected_programs)
        layout.addWidget(install_button)

        return installation_tab

    def create_tweaks_tab(self):
        tweaks_tab = QWidget(self)
        layout = QVBoxLayout(tweaks_tab)

        with open("tweaks.json", "r") as file:
            tweaks_data = json.load(file)

        group_box = QGroupBox("Tweaks")
        group_layout = QVBoxLayout()

        for tweak in tweaks_data:
            tweak_name = tweak.get("name")
            tweak_data = tweak.get("data")

            if tweak_name and tweak_data and "InvokeScript" in tweak_data:
                checkbox = QCheckBox(tweak_name)
                group_layout.addWidget(checkbox)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

        apply_button = QPushButton("Apply Tweaks")
        apply_button.clicked.connect(self.apply_tweaks)
        layout.addWidget(apply_button)

        return tweaks_tab

    
    def create_config_tab(self):
        config_tab = QWidget(self)

        layout = QVBoxLayout(config_tab)

        return config_tab

    def install_selected_programs(self):
        install_tab = self.centralWidget().findChild(QWidget, "Install")
        if install_tab is not None:
            selected_programs = []

            for group_box in install_tab.findChildren(QGroupBox):
                for checkbox in group_box.findChildren(QCheckBox):
                    if checkbox.isChecked():
                        program_name = checkbox.text()
                        selected_programs.append(program_name)

            if selected_programs:
                print("Selected Programs:")
                for program_name in selected_programs:
                    command = self.get_install_command(program_name)
                    if command:
                        print(f"Installing {program_name}...")
                        subprocess.run(command, shell=True)
                    else:
                        print(f"No installation command found for {program_name}.")
            else:
                print("No programs selected.")
        else:
            print("Install tab not found.")

    def get_install_command(self, program_name):
        for section, programs in self.installation_data.items():
            for program in programs:
                if program["name"] == program_name:
                    if "choco" in program:
                        choco_command = "choco install " + program["choco"]
                        return choco_command
                    elif "winget" in program:
                        winget_command = "winget install chocolatey"
                        return winget_command
        return None

    def apply_tweaks(self):
        selected_tweaks = []

        for checkbox in self.tweak_checkboxes:
            if checkbox.isChecked():
                tweak_name = checkbox.text()
                selected_tweaks.append(tweak_name)

        if selected_tweaks:
            print("Selected Tweaks:")
            for tweak_name in selected_tweaks:
                tweak_commands = self.get_tweak_commands(tweak_name)
                if tweak_commands:
                    print(f"Applying {tweak_name} tweaks...")
                    for command in tweak_commands:
                        subprocess.run(command, shell=True)
                else:
                    print(f"No tweak commands found for {tweak_name}.")
        else:
            print("No tweaks selected.")

    def get_tweak_commands(self, tweak_name):
        with open("tweaks.json", "r") as file:
            tweaks_data = json.load(file)

        for tweak in tweaks_data:
            tweak_data = tweak.get(tweak_name)
            if tweak_data:
                return tweak_data.get("InvokeScript", [])

        return []


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
