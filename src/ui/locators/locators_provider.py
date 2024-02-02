from attr import Factory, attrib, attrs

from src.ui.locators.common.validators import locator_format_validator


@attrs
class LocatorsProvider:
    web = attrib(
        kw_only=True,
        default=Factory(lambda self: None, takes_self=True),
        validator=locator_format_validator,
        on_setattr=locator_format_validator,
    )
