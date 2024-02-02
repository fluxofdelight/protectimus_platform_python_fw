from typing import Union

from loguru import logger as log
from selene.core import command, query
from selene.core.condition import Condition
from selene.core.configuration import Config
from selene.core.entity import Element
from selene.core.wait import Command


class ProvidableElement(Element):
    def set_value(self, value: Union[str, int]) -> Element:
        def fn(element: Element):
            webelement = (
                element._actual_not_overlapped_webelement if self.config.wait_for_no_overlap_found_by_js else element()
            )
            webelement.clear()
            webelement.send_keys(str(value))

        self.wait.for_(
            command.js.set_value(value) if self.config.set_value_by_js else Command(f"set value: {value}", fn)
        )
        return self

    def scroll_to(self):
        self.perform(command.js.scroll_into_view)
        return self

    def should(self, condition: Condition[Element], timeout: int = None) -> "ProvidableElement":
        log.info(
            f"[UI Element] Validate that the element by locator "
            f"{self._locator._description} has a condition\n[{condition._description}]"
        )
        if timeout:
            return ProvidableElement(self._locator, Config(timeout=timeout)).should(condition)
        super().should(condition)
        return self

    @property
    def text(self) -> str:
        return self.get(query.text)
