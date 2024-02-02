from attr import attrib, attrs, validators
from selene.support.conditions import be, have, not_

from src.ui.driver.driver import Driver


@attrs
class BasePage:
    driver: Driver = attrib(validator=validators.instance_of(Driver))
    be = be
    not_ = not_
    have = have
