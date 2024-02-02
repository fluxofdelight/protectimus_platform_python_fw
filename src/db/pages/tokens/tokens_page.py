import allure
from loguru import logger as log

from src.db.base import BaseDB


class TokensPageDB(BaseDB):
    @allure.step("Get all token info by ID from DB")
    def get_all_token_info_by_id(self, token_id, json_output=False):
        sql = f"SELECT * FROM token WHERE id = {token_id};"
        return self.read_from_postgres(sql, json_output=json_output)

    @allure.step("Get all token info by serial number from DB")
    def get_all_token_info_by_serial(self, serial, json_output=False):
        sql = f"SELECT * FROM token WHERE serial = '{serial}';"
        return self.read_from_postgres(sql, json_output=json_output)

    @allure.step("Get random token from DB")
    def get_random_token(self, json_output=False):
        sql = "SELECT * FROM token ORDER BY RANDOM() LIMIT 1;"
        return self.read_from_postgres(sql, json_output=json_output)

    @allure.step("Get random token not assigned to any user from DB")
    def get_random_token_not_assigned_to_user(self, json_output=False):
        sql = "SELECT * FROM token WHERE user_id IS NULL ORDER BY RANDOM() LIMIT 1;"
        return self.read_from_postgres(sql, json_output=json_output)

    @allure.step("Get random token assigned to a user from DB")
    def get_random_token_assigned_to_user(self, json_output=False):
        sql = "SELECT * FROM token WHERE user_id IS NOT NULL ORDER BY RANDOM() LIMIT 1;"
        return self.read_from_postgres(sql, json_output=json_output)

    @allure.step("Get number of all tokens in DB")
    def get_number_of_tokens(self) -> str:
        sql = "SELECT COUNT(id) FROM token"
        try:
            number_of_tokens = self.read_from_postgres(sql)[0][0]
        except IndexError:
            log.info("No tokens created")
            return "0"
        return number_of_tokens


if __name__ == "__main__":
    db = TokensPageDB()
    t = db.get_all_token_info_by_id(12, json_output=True)
    import pprint; pprint.pp(t)  # noqa: E702
