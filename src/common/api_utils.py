from configs.config import Config


class APIUtils:

    @staticmethod
    def path_cutter(url):
        return url.removeprefix(Config().api.api_url[:-1])
