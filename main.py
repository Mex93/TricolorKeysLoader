import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QFontDatabase

import logging
import threading

from ui.untitled import Ui_MainWindow
from config_parser.CConfig import CConfig
from common import (send_message_box, SMBOX_ICON_TYPE, get_current_unix_time,
                    is_pattern_match, get_about_text, get_rules_text,
                    is_tricolor_text_valid, convert_date_from_sql_format_ex,
                    is_tv_sn_text_valid)
from enuuuums import INPUT_TYPE

from sql.CSQLQuerys import CSQLQuerys
from sql.enums import CONNECT_DB_TYPE


# pyside6-uic .\ui\untitled.ui -o .\ui\untitled.py
# pyside6-rcc .\ui\res.qrc -o .\ui\res_rc.py
# Press the green button in the gutter to run the script.


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__base_program_version = "0.1"  # Менять при каждом обновлении любой из подпрограмм

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QFontDatabase.addApplicationFont("designs/Iosevka Bold.ttf")
        self.setWindowTitle(f'Загрузчик ключей Tricolor 2024 v0.1b')

        logging.basicConfig(level=logging.INFO, filename="key_logging.log", filemode="a",
                            format="%(asctime)s %(levelname)s %(message)s")

        self.cconfig = CConfig()

        # ---------------------------------------
        try:
            if self.cconfig.load_data() is False:
                send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                 text="Ошибка в файле конфигурации!\n"
                                      "Один или несколько параметров ошибочны!\n\n"
                                      "Позовите технолога!",
                                 title="Внимание!",
                                 variant_yes="Закрыть", variant_no="", callback=lambda: self.set_close())
                return

        except Exception as err:
            send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                             text="Ошибка в файле конфигурации!\n"
                                  "Один или несколько параметров ошибочны!\n\n"
                                  "Позовите технолога!\n\n"
                                  f"Ошибка: '{err}'",
                             title="Внимание!",
                             variant_yes="Закрыть", variant_no="", callback=lambda: self.set_close())
            return

        self.set_default_program_data()

        #
        # self.ui.action_new_project.triggered.connect(self.on_user_clicked_new_project)
        # self.ui.action_set_parameters.triggered.connect(self.on_user_clicked_config_project)
        # self.ui.action_open.triggered.connect(self.on_user_focus)
        # self.set_program_to_default_state()

    def set_default_program_data(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
