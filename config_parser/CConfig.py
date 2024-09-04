import configparser
from os import path
from cryptography.fernet import Fernet

from sql.CSQLAgent import CSqlAgent


class ConfigError(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class CConfig:
    def __init__(self):
        self.__SQL_USER_NAME = ''
        self.__SQL_PASSWORD = ''
        self.__SQL_HOST = ''
        self.__SQL_PORT = ''
        self.__SQL_DATABASE = ''

        self.__config = configparser.ConfigParser()
        self.__config.add_section('program')

    def set_default_for_values(self):
        self.__SQL_USER_NAME = ''
        self.__SQL_PASSWORD = ''
        self.__SQL_HOST = ''
        self.__SQL_PORT = ''
        self.__SQL_DATABASE = ''

    def get_config(self):
        self.__config.read('config.ini', encoding="utf-8")

        self.__SQL_USER_NAME = self.__config.get('database', 'SQL_USER_NAME')
        self.__SQL_PASSWORD = self.__config.get('database', 'SQL_PASSWORD')
        self.__SQL_HOST = self.__config.get('database', 'SQL_HOST')
        self.__SQL_PORT = self.__config.get('database', 'SQL_PORT')
        self.__SQL_DATABASE = self.__config.get('database', 'SQL_DATABASE')


    @staticmethod
    def is_config_created():
        if path.isfile('config.ini') is True:
            return True
        return False

    def create_config(self):
        with open('config.ini', 'w') as config_file:
            self.__config.set('database', 'SQL_USER_NAME', 'This place for user!')
            self.__config.set('database', 'SQL_PASSWORD', 'This place for user password!')
            self.__config.set('database', 'SQL_HOST', 'This place for db host!')
            self.__config.set('database', 'SQL_PORT', 'This place for db port!')
            self.__config.set('database', 'SQL_DATABASE', 'This place for db name!')

            self.set_default_for_values()
            self.__config.write(config_file)


    def get_dbpassword(self):
        return self.__SQL_PASSWORD

    def get_dbuser(self):
        return self.__SQL_USER_NAME

    def get_dbhost(self):
        return self.__SQL_HOST

    def get_dbport(self):
        return self.__SQL_PORT

    def get_dname(self):
        return self.__SQL_DATABASE

    def save_config(self):
        if self.is_config_created() is False:
            with open('config.ini', 'w') as config_file:
                self.__config.write(config_file)

    def load_data(self):
        if self.is_config_created():
            self.get_config()
        else:
            self.create_config()
            self.get_config()

        db_name = self.get_dname()
        db_user = self.get_dbuser()
        db_pass = self.get_dbpassword()
        db_port = self.get_dbport()
        db_host = self.get_dbhost()

        crypto_key = Fernet.generate_key()
        # print("keu: " + str(crypto_key))
        crypto_key = "UnYrZd2J3x0yuCNzemf4WFBbIW_nzngwLYDM9JaXN1I="  # ключ для расшифровки
        cipher_suite = Fernet(crypto_key)

        # db_standart_connect_params = {
        #     KEY_VALUE_NAME_USER: 'test_user',
        #     KEY_VALUE_NAME_PASS: 'sadmin',
        #     KEY_VALUE_NAME_DATABASE: 'test_db',
        #     KEY_VALUE_NAME_HOST: '192.168.7.182',
        #     KEY_VALUE_NAME_PORT: '5432'
        # }

        # cipher_text = cipher_suite.encrypt(b"program_tricolor_scanned")
        # print(cipher_text)
        # cipher_text = cipher_suite.encrypt(b"OUHGhgtjcfUOjopHIYf")
        # print(cipher_text)
        # cipher_text = cipher_suite.encrypt(b"assemblyproduction")
        # print(cipher_text)

        set_config_error = False
        db_params = (db_name, db_user, db_pass, db_port, db_host)
        for value in db_params:
            if value is False or value is None or value.find("This") != -1:
                # this error
                set_config_error = True
                break

        if set_config_error is False:
            # decode
            try:
                db_name = cipher_suite.decrypt(db_name)
                db_name = db_name.decode()
                db_user = cipher_suite.decrypt(db_user)
                db_user = db_user.decode()
                db_pass = cipher_suite.decrypt(db_pass)
                db_pass = db_pass.decode()

            except:
                set_config_error = True

            if set_config_error is False:

                db_params = (db_name, db_user, db_pass)
                for value in db_params:
                    if value is False or value is None or value.find("This") != -1:
                        # this error
                        set_config_error = True
                        break

                if set_config_error is False:
                    sql_data: dict = {
                        CSqlAgent.get_value_name_database(): db_name,
                        CSqlAgent.get_value_name_user(): db_user,
                        CSqlAgent.get_value_name_host(): db_host,
                        CSqlAgent.get_value_name_port(): db_port,
                        CSqlAgent.get_value_name_pass(): db_pass,
                    }

                    # print(sql_data)
                    CSqlAgent.set_sql_data_line(sql_data)

        if set_config_error is True:
            return False

        return True
