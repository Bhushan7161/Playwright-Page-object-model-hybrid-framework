class KeywordEngine:
    """Executes reusable browser-action keywords against Playwright locators."""

    def __init__(self, page):
        self.page = page

    def execute(self, keyword, selector, value=None):
        actions = {
            "click": self._click,
            "type": self._type,
            "hover": self._hover,
        }

        normalized_keyword = keyword.strip().lower()
        if normalized_keyword not in actions:
            raise ValueError(
                f"Unsupported keyword: {keyword}. "
                f"Choose from: {', '.join(actions)}"
            )

        return actions[normalized_keyword](selector, value)

    def _click(self, selector, _value=None):
        self.page.locator(selector).click()

    def _type(self, selector, value=None):
        if value is None:
            raise ValueError("The 'type' keyword requires a value")
        self.page.locator(selector).fill(str(value))

    def _hover(self, selector, _value=None):
        self.page.locator(selector).hover()
