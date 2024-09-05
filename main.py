import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QFontDatabase

import logging

from ui.untitled import Ui_MainWindow
from config_parser.CConfig import CConfig
from common import (send_message_box, SMBOX_ICON_TYPE, get_current_unix_time,
                    is_pattern_match, get_about_text, get_rules_text,
                    is_tricolor_text_valid,
                    )

from sql.CSQLQuerys import CSQLQuerys, SQL_TV_MODELS_DATA
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

        self.anti_flood = 0
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

            self.ktemplate = self.cconfig.get_tricolor_template()

        except Exception as err:
            send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                             text="Ошибка в файле конфигурации!\n"
                                  "Один или несколько параметров ошибочны!\n\n"
                                  "Позовите технолога!\n\n"
                                  f"Ошибка: '{err}'",
                             title="Внимание!",
                             variant_yes="Закрыть", variant_no="", callback=lambda: self.set_close())
            return
        self.cmodel = TVmodels(self)
        self.clabels = Labels(self)
        self.ckeys = KeysList(self)

        self.set_default_program_data()

        self.ui.pushButton_clear_all.clicked.connect(self.on_user_clicked_on_clear_all)
        self.ui.pushButton_clear_list.clicked.connect(self.on_user_clicked_on_clear_list)
        self.ui.pushButton_start_load.clicked.connect(self.on_user_clicked_on_load)

        self.ui.combo_tv_list.activated.connect(self.on_user_clicked_on_model_change)
        self.ui.action_about.triggered.connect(self.on_user_pressed_info)
        self.load_models()
        #
        # self.ui.action_new_project.triggered.connect(self.on_user_clicked_new_project)
        # self.ui.action_set_parameters.triggered.connect(self.on_user_clicked_config_project)
        # self.ui.action_open.triggered.connect(self.on_user_focus)
        # self.set_program_to_default_state()

    @staticmethod
    def on_user_pressed_info():
        send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_INFO,
                         text=f"{get_about_text()}"
                              f"\n"
                              f"\n"
                              f"{get_rules_text()}",
                         title="О программе",
                         variant_yes="Закрыть", variant_no="")

    def set_default_program_data(self):
        self.cmodel.reset_changed_model()
        self.clabels.set_error_count(0)
        self.clabels.set_success_count(0)
        self.ckeys.clear()

    def load_models(self):
        csql = CSQLQuerys()
        try:
            result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
            if result_connect is True:
                result = csql.load_tricolor_models()
                count = 0
                if result is not False:
                    for tv in result:
                        tv_name = tv.get(SQL_TV_MODELS_DATA.fd_tv_name, None)
                        tv_fk = tv.get(SQL_TV_MODELS_DATA.fd_tv_id, None)
                        if None in (tv_name, tv_fk):
                            continue

                        self.cmodel.add_item_on_change(tv_fk, tv_name)
                        count += 1

                if not count:
                    self.send_error_message(
                        "Во время выполнения программы произошла ошибка #3.\n"
                        "Обратитесь к системному администратору!\n\n"
                        f"Код ошибки: 'load_models -> [No Data]'")
                    return
                else:
                    self.ui.combo_tv_list.setCurrentIndex(0)
                    self.on_user_clicked_on_model_change()
            else:
                raise ValueError("Нет подключения к БД!")

        except Exception as err:
            print(err)
            logging.critical(err)
            self.send_error_message(
                "Во время выполнения программы произошла ошибка #2.\n"
                "Обратитесь к системному администратору!\n\n"
                f"Код ошибки: 'load_models -> [{err}]'")
            return False
        finally:
            csql.disconnect_from_db()

    def set_close(self):
        sys.exit()

    def send_error_message(self, text: str):
        self.blocked_window()

        send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                         text=text,
                         title="Фатальная ошибка",
                         variant_yes="Закрыть программу", variant_no="", callback=lambda: self.set_close())

    def blocked_window(self):
        self.ui.horizontalLayout_2.setEnabled(False)

    def on_user_clicked_on_model_change(self):
        text = self.ui.combo_tv_list.currentText()
        if text:
            tv_fk = self.cmodel.get_item_from_tv_name(text)
            if tv_fk != -1:
                self.cmodel.set_changed_model(tv_fk)
                return

        self.send_error_message(
            "Во время выполнения программы произошла ошибка #4.\n"
            "Обратитесь к системному администратору!\n\n"
            f"Код ошибки: 'on_user_clicked_on_model_change -> [Not find changed models]'")

    def on_user_clicked_on_clear_all(self):
        self.set_default_program_data()

    def on_user_clicked_on_clear_list(self):
        self.ckeys.clear()

    def on_user_clicked_on_load(self):
        if self.cmodel.is_model_changed():

            if self.anti_flood > get_current_unix_time():
                send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_WARNING,
                                 text="Не флуди!",
                                 title="Предупреждение!",
                                 variant_yes="Закрыть", variant_no="", callback=None)
                return
            self.anti_flood = get_current_unix_time() + 5

            text = self.ckeys.get_keys_text()
            if text:
                csql = CSQLQuerys()
                try:
                    keys = text.split("\n")
                    all_first_parsed = 0
                    changed_tv_fk = self.cmodel.get_model_fk_changed()
                    changed_model_name = self.cmodel.get_model_name_changed()
                    if isinstance(keys, list):
                        filtered_list = [item for item in keys if item]
                        keys = filtered_list
                        all_first_parsed = len(filtered_list)
                    else:
                        self.clabels.set_error_count(1)
                        self.clabels.set_success_count(0)
                        send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                         text="Ни один ключ не вставлен!\n\n"
                                              f"Модель {changed_model_name}[{changed_tv_fk}]\n"
                                              f"Всего первично отпарсено: {all_first_parsed}\n"
                                              f"Несовпадение по шаблону: -\n"
                                              f"Были найдены в каких либо таблицах: -\n\n"
                                              f"Ошибка вызвана тем, что вообще ничего распарсить неполучилось!",
                                         title="Ошибка!",
                                         variant_yes="Закрыть", variant_no="", callback=None)
                        return
                    count_success = 0
                    count_errors = 0
                    count_match_pattern = 0
                    count_no_match_pattern = 0

                    result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
                    if result_connect is True:
                        success_keys = list()
                        logging.info(f"Старт загрузки ключей!!!")
                        for key in keys:
                            if is_pattern_match(self.ktemplate, key) and is_tricolor_text_valid(key):
                                count_match_pattern += 1
                                key_replaced = key.replace(" ", "").replace("\n", "")
                                success_keys.append(key_replaced)
                            else:
                                count_no_match_pattern += 1

                        if count_match_pattern:
                            in_insert_keys = list()
                            success_query_check_count = 0
                            for key in success_keys:

                                result = csql.get_assembled_tv_from_tricolor_key(key)
                                if isinstance(result, tuple):
                                    count_errors += 1
                                    tv_fk, tv_sn, completed_scan_time, tv_name, assemled_line = result
                                    text = (f"Внимание! Обнаружен ключ '{key}' в устройстве SN: "
                                            f"'{tv_sn}'[{tv_name}][{tv_fk}]"
                                            f"[{str(completed_scan_time)}][Линия {assemled_line}]")
                                    print(text)
                                    logging.critical(text)
                                    continue

                                result = csql.get_tricolor_key_data_in_key_base(key, changed_tv_fk)
                                if isinstance(result, tuple):
                                    count_errors += 1
                                    tv_fk, tv_name, load_key_data = result

                                    text = (f"Внимание! Обнаружен ключ '{key}' в общей базе ключей: "
                                            f"[{tv_name}][{tv_fk}][{str(load_key_data)}]")

                                    logging.critical(text)
                                    print(text)
                                    continue

                                result = csql.get_tricolor_key_data_in_history_base(key)
                                if isinstance(result, tuple):
                                    count_errors += 1
                                    tv_fk, tv_name, attached_tv_sn, load_key_date, attach_on_device_date, assemled_line = result

                                    text = (f"Внимание! Обнаружен ключ '{key}' в базе истории ключей: "
                                            f"SN: '{attached_tv_sn}' [{tv_name}][{tv_fk}][{str(load_key_date)}]"
                                            f"[{str(attach_on_device_date)}][Линия {assemled_line}]")

                                    logging.critical(text)
                                    print(text)
                                    continue

                                result = csql.get_tricolor_key_data_in_process_base(key)
                                if isinstance(result, tuple):
                                    count_errors += 1
                                    tv_fk, tv_name, attached_tv_sn, load_key_date, attach_on_device_date, assemled_line = result

                                    text = (f"Внимание! Обнаружен ключ '{key}' в базе привязки ключей: "
                                            f"SN: '{attached_tv_sn}' [{tv_name}][{tv_fk}][{str(load_key_date)}]"
                                            f"[{str(attach_on_device_date)}][Линия {assemled_line}]")

                                    logging.critical(text)
                                    print(text)
                                    continue

                                in_insert_keys.append(key)
                                success_query_check_count += 1

                            if success_query_check_count:
                                for key in in_insert_keys:
                                    csql.insert_key_in_keys_base(changed_tv_fk, key)
                                    count_success += 1
                                    text = (f"Ключ '{key}' успешно импортирован в общую базу ключей: "
                                            f"Key: '{key}' [{changed_model_name}][{changed_tv_fk}]")

                                    logging.info(text)
                                    print(text)

                                self.clabels.set_error_count(count_errors)
                                self.clabels.set_success_count(success_query_check_count)

                                text = (
                                    f"Импорт ключей завершён: Количество успешно вставленных: {success_query_check_count} единиц"
                                    f"[Модель {changed_model_name}[{changed_tv_fk}]]"
                                    f"[Всего первично отпарсено: {all_first_parsed}]"
                                    f"[Несовпадение по шаблону: {count_no_match_pattern}]"
                                    f"[Были найдены в каких либо таблицах: {count_errors}]")

                                logging.info(text)
                                print(text)
                                send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_INFO,
                                                 text="Ключи успешно вставлены!\n\n"
                                                      f"Модель {changed_model_name}[{changed_tv_fk}]\n"
                                                      f"Всего первично отпарсено: {all_first_parsed}\n"
                                                      f"Несовпадение по шаблону: {count_no_match_pattern}\n"
                                                      f"Были найдены в каких либо таблицах: {count_errors}\n"
                                                      f"Вставлены успешно: {success_query_check_count}\n\n"
                                                      "Подробности можно посмотреть в логе, в папке с программой.",
                                                 title="Успех!",
                                                 variant_yes="Закрыть", variant_no="", callback=None)
                                return
                            else:
                                text = (f"Из отсортированных ключей ни один не может быть вставлен. "
                                        f"[Всего первично отпарсено: {all_first_parsed}]"
                                        f"[Несовпадение по шаблону: {count_no_match_pattern}]"
                                        f"[Были найдены в каких либо таблицах: {count_errors}]"
                                        f"[Модель {changed_model_name}[{changed_tv_fk}]]")

                                logging.warning(text)
                                print(text)
                                self.clabels.set_error_count(count_errors)
                                self.clabels.set_success_count(success_query_check_count)
                                send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                                 text="Ни один ключ не вставлен!\n\n"
                                                      f"Модель {changed_model_name}[{changed_tv_fk}]\n"
                                                      f"Всего первично отпарсено: {all_first_parsed}\n"
                                                      f"Несовпадение по шаблону: {count_no_match_pattern}\n"
                                                      f"Были найдены в каких либо таблицах: {count_errors}\n"
                                                      f"Вставлены успешно: {success_query_check_count}\n\n"
                                                      "Подробности можно посмотреть в логе, в папке с программой.",
                                                 title="Ошибка!",
                                                 variant_yes="Закрыть", variant_no="", callback=None)
                                return
                        else:
                            text = (f"Из отсортированных ключей ни один не может быть вставлен. "
                                    f"[Всего первично отпарсено: {all_first_parsed}]"
                                    f"[Несовпадение по шаблону: {count_no_match_pattern}]"
                                    f"[Были найдены в каких либо таблицах: {count_errors}]"
                                    f"[Модель {changed_model_name}[{changed_tv_fk}]]")

                            logging.warning(text)
                            print(text)
                            self.clabels.set_error_count(count_errors)
                            self.clabels.set_success_count(0)
                            send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                             text="Ни один ключ не вставлен!\n\n"
                                                  f"Модель {changed_model_name}[{changed_tv_fk}]\n"
                                                  f"Всего первично отпарсено: {all_first_parsed}\n"
                                                  f"Несовпадение по шаблону: {count_no_match_pattern}\n"
                                                  f"Были найдены в каких либо таблицах: {count_errors}\n\n"
                                                  "Подробности можно посмотреть в логе, в папке с программой.",
                                             title="Ошибка!",
                                             variant_yes="Закрыть", variant_no="", callback=None)
                            return
                    else:
                        raise ValueError("Нет подключения к БД!")

                except Exception as err:
                    print(err)
                    send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                     text="Ошибка в парсинге ключей!\n"
                                          "Все ключи должны быть разделены пробелом.\n\n"
                                          "Удобно копирнуть из exel файла.",
                                     title="Внимание!",
                                     variant_yes="Закрыть", variant_no="", callback=None)

                finally:
                    csql.disconnect_from_db()


class KeysList:

    def __init__(self, main_menu: MainWindow):
        self.__keys_list = main_menu.ui.textEdit_keys_list

    def get_keys_text(self) -> str:
        return self.__keys_list.toPlainText()

    def clear(self) -> None:
        self.__keys_list.clear()


class Labels:
    def __init__(self, main_menu: MainWindow):
        self.__main_menu = main_menu

    def set_error_count(self, errors: int) -> None:
        self.__main_menu.ui.label_key_no_loaded.setText(f"Ключей не загружено: {errors}")

    def set_success_count(self, success: int) -> None:
        self.__main_menu.ui.label_key_success_loaded.setText(f"Ключей загружено: {success}")


class TVmodels:
    def __init__(self, main_menu: MainWindow):
        self.__main_menu = main_menu
        self.__tv_list = list()
        self.__current_model_fk = 0
        self.__current_model_name = ""
        self.__list_max_index = 0
        self.reset_changed_model()

    def add_item_on_change(self, tv_fk: int, tv_name: str):

        mm = self.__main_menu.ui
        mm.combo_tv_list.addItem(tv_name)
        mm.combo_tv_list.setItemText(self.__list_max_index, tv_name)

        self.__list_max_index += 1
        self.__tv_list.append([tv_fk, tv_name])

    def get_item_index_from_tv_fk(self, tv_fk: int) -> int:
        for index, item in enumerate(self.__tv_list):
            if item[0] == tv_fk:
                return index
        return -1

    def get_item_index_from_tv_name(self, tv_name: str) -> int:
        for index, item in enumerate(self.__tv_list):
            if item[1] == tv_name:
                return index
        return -1

    def get_item_from_tv_name(self, tv_name: str) -> int:
        for index, item in enumerate(self.__tv_list):
            if item[1] == tv_name:
                return item[0]
        return 0

    def set_changed_model(self, tv_fk: int) -> bool:
        index = self.get_item_index_from_tv_fk(tv_fk)
        if index != -1:
            mm = self.__main_menu.ui
            self.__current_model_fk = tv_fk
            model_name = self.__tv_list[index][1]
            self.__current_model_name = model_name
            mm.label_model.setText(f"Модель: {model_name} [{tv_fk}]")
            return True

    def reset_changed_model(self) -> None:
        self.__current_model_fk = 0
        self.__current_model_name = ""
        self.__main_menu.ui.label_model.setText(f"Модель: Нет")

    def is_model_changed(self) -> bool:
        if self.__current_model_fk == 0:
            return False
        else:
            return True

    def get_model_fk_changed(self) -> int:
        return self.__current_model_fk

    def get_model_name_changed(self) -> str:
        return self.__current_model_name


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
