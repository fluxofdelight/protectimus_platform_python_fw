import psycopg
from loguru import logger as log
from psycopg.rows import dict_row

from src.configs.config import Config


class BaseDB:
    def __init__(self):
        self.creds = Config().postgres

    def read_from_postgres(self, sql, raise_if_not_found=False, json_output=False):
        with psycopg.connect(
            host=self.creds.host, dbname=self.creds.database, user=self.creds.user, password=self.creds.password
        ) as con:
            if not json_output:
                with con.cursor() as cur:
                    cur.execute(sql)
                    db_data = cur.fetchall()
            else:
                with con.cursor(row_factory=dict_row) as cur:
                    cur.execute(sql)
                    db_data = cur.fetchall()
        if bool(db_data):
            log.success(
                f"Success DB result. Full query:\n{sql}\nResult:\n{db_data}"
            )
            return db_data
        else:
            if not raise_if_not_found:
                return None
            else:
                raise Exception(f"Empty result when reading expected data from database\nFull query:\n\n{sql}")

    def write_to_postgres(self, sql):
        with psycopg.connect(
            host=self.creds.host, dbname=self.creds.database, user=self.creds.user, password=self.creds.password
        ) as con:
            with con.cursor(row_factory=dict_row) as cur:
                cur.execute(sql)
                con.commit()
                cur.close()
            con.close()
