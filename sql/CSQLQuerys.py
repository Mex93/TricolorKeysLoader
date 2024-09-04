from sql.CSQLAgent import CSqlAgent
from sql.sql_data import (SQL_TABLE_NAME,
                          SQL_KEY_HISTORY,
                          SQL_KEY_PROCESS_BASE,
                          SQL_KEY_BASE_SN,
                          SQL_TABLE_ASSEMBLED_TV,
                          SQL_TV_MODELS_DATA)


class CSQLQuerys(CSqlAgent):

    def __init__(self):
        super().__init__()

    def load_tricolor_models(self) -> bool | dict:
        query_string = (f"SELECT "
                        f"{SQL_TV_MODELS_DATA.fd_tv_name}, "
                        f"{SQL_TV_MODELS_DATA.fd_tv_id} "
                        f"FROM {SQL_TABLE_NAME.tb_tv_models} "
                        f"WHERE {SQL_TV_MODELS_DATA.fd_is_tricolor_id} = true "
                        f"LIMIT 20")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        tv_name = result[0].get(SQL_TV_MODELS_DATA.fd_tv_name, None)
        tv_fk = result[0].get(SQL_TV_MODELS_DATA.fd_tv_id, None)
        if None in (tv_fk, tv_name):
            return False
        return result

    def get_assembled_tv_from_tricolor_key(self, key: str) -> tuple | bool:

        query_string = (f"SELECT "
                        f"{SQL_TABLE_NAME.tb_tv_models}.{SQL_TV_MODELS_DATA.fd_tv_name}, "
                        f"{SQL_TABLE_NAME.tb_assembled_tv}.{SQL_TABLE_ASSEMBLED_TV.fd_tv_fk},"
                        f"{SQL_TABLE_NAME.tb_assembled_tv}.{SQL_TABLE_ASSEMBLED_TV.fd_tv_sn}, "
                        f"{SQL_TABLE_NAME.tb_assembled_tv}.{SQL_TABLE_ASSEMBLED_TV.fd_line_fk}, "
                        f"{SQL_TABLE_NAME.tb_assembled_tv}.{SQL_TABLE_ASSEMBLED_TV.fd_completed_scan_time} "

                        f"FROM {SQL_TABLE_NAME.tb_assembled_tv} "

                        f"JOIN {SQL_TABLE_NAME.tb_tv_models} ON "
                        f"{SQL_TABLE_NAME.tb_tv_models}.{SQL_TV_MODELS_DATA.fd_tv_id} = "
                        f"{SQL_TABLE_NAME.tb_assembled_tv}.{SQL_TABLE_ASSEMBLED_TV.fd_tv_fk} "

                        f"WHERE {SQL_TABLE_NAME.tb_assembled_tv}.{SQL_TABLE_ASSEMBLED_TV.fd_tricolor_key} = %s "

                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (key,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        assembled_line = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_line_fk, None)
        tv_fk = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_tv_fk, None)
        tv_sn = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_tv_sn, None)
        completed_scan_time = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_completed_scan_time, None)
        tv_name = result[0].get(SQL_TV_MODELS_DATA.fd_tv_name, None)
        ret_tup = (tv_fk, tv_sn, completed_scan_time, tv_name, assembled_line)
        return ret_tup

    def get_tricolor_key_data_in_key_base(self, tricolor_key: str, tv_fk: int) -> tuple | bool:
        #  f"WHERE {SQL_TABLE_NAME.tb_tricolor_keys_base}.{SQL_KEY_BASE_SN.fd_tv_fk} = %s AND"
        query_string = (f"SELECT "
                        f"{SQL_TABLE_NAME.tb_tv_models}.{SQL_TV_MODELS_DATA.fd_tv_name}, "
                        f"{SQL_TABLE_NAME.tb_tricolor_keys_base}.{SQL_KEY_BASE_SN.fd_tv_fk},"
                        f"{SQL_TABLE_NAME.tb_tricolor_keys_base}.{SQL_KEY_BASE_SN.fd_load_key_date} "

                        f"FROM {SQL_TABLE_NAME.tb_tricolor_keys_base} "

                        f"JOIN {SQL_TABLE_NAME.tb_tv_models} ON "
                        f"{SQL_TABLE_NAME.tb_tv_models}.{SQL_TV_MODELS_DATA.fd_tv_id} = "
                        f"{SQL_TABLE_NAME.tb_tricolor_keys_base}.{SQL_KEY_BASE_SN.fd_tv_fk} "

                        f"WHERE {SQL_TABLE_NAME.tb_tricolor_keys_base}.{SQL_KEY_BASE_SN.fd_tricolor_key} = %s "

                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (tricolor_key,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        tv_fk = result[0].get(SQL_TABLE_ASSEMBLED_TV.fd_tv_fk, None)
        load_key_data = result[0].get(SQL_KEY_BASE_SN.fd_load_key_date, None)
        tv_name = result[0].get(SQL_TV_MODELS_DATA.fd_tv_name, None)
        ret_tup = (tv_fk, tv_name, load_key_data)
        return ret_tup

    def get_tricolor_key_data_in_history_base(self, any_data: str) -> tuple | bool:

        query_string = (f"SELECT "
                        f"{SQL_TABLE_NAME.tb_tv_models}.{SQL_TV_MODELS_DATA.fd_tv_name}, "
                        f"{SQL_TABLE_NAME.tb_tricolor_history}.{SQL_KEY_HISTORY.fd_attached_tv_sn},"
                        f"{SQL_TABLE_NAME.tb_tricolor_history}.{SQL_KEY_HISTORY.fd_load_key_date},"
                        f"{SQL_TABLE_NAME.tb_tricolor_history}.{SQL_KEY_HISTORY.fd_assembled_line},"
                        f"{SQL_TABLE_NAME.tb_tricolor_history}.{SQL_KEY_HISTORY.fd_attach_on_device_fk},"
                        f"{SQL_TABLE_NAME.tb_tricolor_history}.{SQL_KEY_HISTORY.fd_attach_on_device_date} "

                        f"FROM {SQL_TABLE_NAME.tb_tricolor_history} "

                        f"JOIN {SQL_TABLE_NAME.tb_tv_models} ON "
                        f"{SQL_TABLE_NAME.tb_tv_models}.{SQL_TV_MODELS_DATA.fd_tv_id} = "
                        f"{SQL_TABLE_NAME.tb_tricolor_history}.{SQL_KEY_HISTORY.fd_attach_on_device_fk} "

                        f"WHERE {SQL_TABLE_NAME.tb_tricolor_history}.{SQL_KEY_HISTORY.fd_tricolor_key} = %s "

                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (any_data,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        tv_fk = result[0].get(SQL_KEY_HISTORY.fd_attach_on_device_fk, None)
        tv_name = result[0].get(SQL_TV_MODELS_DATA.fd_tv_name, None)
        attached_tv_sn = result[0].get(SQL_KEY_HISTORY.fd_attached_tv_sn, None)
        load_key_date = result[0].get(SQL_KEY_HISTORY.fd_load_key_date, None)
        attach_on_device_date = result[0].get(SQL_KEY_HISTORY.fd_attach_on_device_date, None)
        assemled_line = result[0].get(SQL_KEY_HISTORY.fd_assembled_line, None)

        ret_tup = (tv_fk, tv_name, attached_tv_sn, load_key_date, attach_on_device_date, assemled_line)
        return ret_tup

    def get_tricolor_key_data_in_process_base(self, any_data: str) -> tuple | bool:

        query_string = (f"SELECT "
                        f"{SQL_TABLE_NAME.tb_tv_models}.{SQL_TV_MODELS_DATA.fd_tv_name}, "
                        f"{SQL_TABLE_NAME.tb_process_atached}.{SQL_KEY_PROCESS_BASE.fd_tv_fk},"
                        f"{SQL_TABLE_NAME.tb_process_atached}.{SQL_KEY_PROCESS_BASE.fd_used_device_sn},"
                        f"{SQL_TABLE_NAME.tb_process_atached}.{SQL_KEY_PROCESS_BASE.fd_load_key_date},"
                        f"{SQL_TABLE_NAME.tb_process_atached}.{SQL_KEY_PROCESS_BASE.fd_assembled_line},"
                        f"{SQL_TABLE_NAME.tb_process_atached}.{SQL_KEY_PROCESS_BASE.fd_attach_on_device_date} "

                        f"FROM {SQL_TABLE_NAME.tb_process_atached} "

                        f"JOIN {SQL_TABLE_NAME.tb_tv_models} ON "
                        f"{SQL_TABLE_NAME.tb_tv_models}.{SQL_TV_MODELS_DATA.fd_tv_id} = "
                        f"{SQL_TABLE_NAME.tb_process_atached}.{SQL_KEY_PROCESS_BASE.fd_tv_fk} "

                        f"WHERE {SQL_TABLE_NAME.tb_process_atached}.{SQL_KEY_PROCESS_BASE.fd_tricolor_key} = %s "

                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (any_data,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        tv_fk = result[0].get(SQL_TV_MODELS_DATA.fd_tv_name, None)
        tv_name = result[0].get(SQL_KEY_PROCESS_BASE.fd_tv_fk, None)
        attached_tv_sn = result[0].get(SQL_KEY_PROCESS_BASE.fd_used_device_sn, None)
        load_key_date = result[0].get(SQL_KEY_PROCESS_BASE.fd_load_key_date, None)
        attach_on_device_date = result[0].get(SQL_KEY_PROCESS_BASE.fd_attach_on_device_date, None)
        assemled_line = result[0].get(SQL_KEY_PROCESS_BASE.fd_assembled_line, None)

        ret_tup = (tv_fk, tv_name, attached_tv_sn, load_key_date, attach_on_device_date, assemled_line)
        return ret_tup

    def insert_key_in_keys_base(self, tv_fk: int, tricolor_key: str) -> bool:

        query_string = (f"INSERT INTO {SQL_TABLE_NAME.tb_tricolor_keys_base} "
                        f"({SQL_KEY_BASE_SN.fd_tv_fk}, "
                        f"{SQL_KEY_BASE_SN.fd_tricolor_key})"
                        f"VALUES (%s, %s) RETURNING {SQL_KEY_BASE_SN.fd_assy_id}")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (tv_fk, tricolor_key),
            "_i", transaction=False)  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        return True
