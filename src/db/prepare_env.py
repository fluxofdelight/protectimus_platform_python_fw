from loguru import logger as log

from src.configs.config import Config
from src.db.base import BaseDB


class PrepareEnv(BaseDB):
    def __init__(self):
        super().__init__()
        self.config = Config()

    def truncate_all_tables(self):
        sql = (
            "TRUNCATE TABLE a_lot_of_db_tables CASCADE;"
        )
        log.info("Clear all data in tables in the DB")
        return self.write_to_postgres(sql)

    def drop_all_db_info(self):
        sql = """
            DO $$
            DECLARE
                table_to_drop text;
                function_to_drop text;
                sequence_to_drop text;
            BEGIN
                FOR table_to_drop IN (SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'
                    AND table_type = 'BASE TABLE')
                LOOP
                    EXECUTE 'DROP TABLE IF EXISTS public.' || table_to_drop || ' CASCADE';
                END LOOP;
                FOR function_to_drop IN (SELECT routine_name FROM information_schema.routines
                    WHERE routine_schema = 'public' AND routine_type = 'FUNCTION')
                LOOP
                    EXECUTE 'DROP FUNCTION IF EXISTS public.' || function_to_drop || ' CASCADE';
                END LOOP;
                FOR sequence_to_drop IN (SELECT sequence_name FROM information_schema.sequences
                    WHERE sequence_schema = 'public')
                LOOP
                    EXECUTE 'DROP SEQUENCE IF EXISTS public.' || sequence_to_drop || ' CASCADE';
                END LOOP;
            END $$;
        """
        log.info("Drop all DB info")
        return self.write_to_postgres(sql)

    def fill_out_db(self):
        dump = self.config.postgres.dump_path
        with open(dump) as sql:
            sql = sql.read()
            log.info("Write data from dump file into the DB")
            return self.write_to_postgres(sql)
