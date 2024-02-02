from selenium.webdriver.common.by import By


def locator_format_validator(instance, attribute, value):
    if value is not None and (
        not isinstance(value, tuple)
        or not getattr(By, value[0].upper().replace("-", "").replace(" ", "_").replace("_STRING", ""), None)
    ):
        raise ValueError(f"Error locator format value: {value}. Expected like: (By.ID, locator_id)")
    return value
