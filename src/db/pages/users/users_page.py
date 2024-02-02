import allure
from loguru import logger as log

from src.db.base import BaseDB


class UsersPageDB(BaseDB):
    @allure.step("Get all user info by ID from DB")
    def get_all_user_info_by_id(self, user_id, json_output=False):
        sql = f"SELECT * FROM user WHERE id = {user_id};"
        return self.read_from_postgres(sql, json_output=json_output)

    @allure.step("Get all user info by login from DB")
    def get_all_user_info_by_login(self, login, json_output=False):
        sql = f"SELECT * FROM user WHERE login = '{login}';"
        return self.read_from_postgres(sql, json_output=json_output)

    @allure.step("Get all user info by alias from DB")
    def get_all_user_info_by_alias(self, alias, json_output=False):
        sql = f"SELECT * FROM user WHERE alias = '{alias}';"
        return self.read_from_postgres(sql, json_output=json_output)

    @allure.step("Get all user info by email from DB")
    def get_all_user_info_by_email(self, email, json_output=False):
        sql = f"SELECT * FROM user WHERE email = '{email}';"
        return self.read_from_postgres(sql, json_output=json_output)

    @allure.step("Get all user info by phone from DB")
    def get_all_user_info_by_phone(self, phone, json_output=False):
        sql = f"SELECT * FROM user WHERE phone = '{phone}';"
        return self.read_from_postgres(sql, json_output=json_output)

    @allure.step("Get user login by ID from DB")
    def get_user_login_by_id(self, user_id, json_output=False):
        sql = f"SELECT login FROM user WHERE id = {user_id};"
        login = self.read_from_postgres(sql, raise_if_not_found=True, json_output=json_output)[0][0]
        return login

    @allure.step("Get first user login in the table from DB")
    def get_first_user_login(self, json_output=False):
        sql = "SELECT login FROM user ORDER BY id DESC LIMIT 1;"
        try:
            login = self.read_from_postgres(sql, json_output=json_output)[0][0]
        except IndexError:
            log.info("No users created")
            return None
        return login

    @allure.step("Get first user info in the table from DB")
    def get_first_user_id(self, json_output=False):
        sql = "SELECT id FROM user ORDER BY id DESC LIMIT 1;"
        try:
            user_id = self.read_from_postgres(sql, json_output=json_output)[0][0]
        except IndexError:
            log.info("No users created")
            return None
        return user_id

    @allure.step("Get number of all users in DB")
    def get_number_of_users(self) -> str:
        sql = "SELECT COUNT(login) FROM user"
        try:
            number_of_users = self.read_from_postgres(sql)[0][0]
        except IndexError:
            log.info("No users created")
            return "0"
        return number_of_users

    @allure.step("Get random user from DB")
    def get_random_user(self, json_output=False):
        sql = "SELECT * FROM user ORDER BY RANDOM() LIMIT 1;"
        return self.read_from_postgres(sql, json_output=json_output)

    @allure.step("Get random user that has tokens from DB")
    def get_random_user_with_tokens(self, json_output=False):
        sql = "SELECT * FROM user WHERE has_tokens = TRUE ORDER BY RANDOM() LIMIT 1;"
        return self.read_from_postgres(sql, json_output=json_output)
