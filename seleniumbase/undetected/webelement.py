import selenium.webdriver.remote.webelement
from seleniumbase.fixtures import js_utils


class WebElement(selenium.webdriver.remote.webelement.WebElement):
    def uc_click(
        self,
        driver=None,
        selector=None,
        by=None,
        reconnect_time=None,
        tag_name=None,
    ):
        if driver and selector and by:
            if tag_name == "span" and ":contains" not in selector:
                selector = js_utils.convert_to_css_selector(selector, by)
                script = 'document.querySelector("%s").click();' % selector
                js_utils.call_me_later(driver, script, 111)
            else:
                driver.js_click(selector, by=by, timeout=1)
        else:
            super().click()
        if not reconnect_time:
            self._parent.reconnect(0.5)
        else:
            self._parent.reconnect(reconnect_time)

    def uc_reconnect(self, reconnect_time=None):
        if not reconnect_time:
            self._parent.reconnect(0.2)
        else:
            self._parent.reconnect(reconnect_time)
