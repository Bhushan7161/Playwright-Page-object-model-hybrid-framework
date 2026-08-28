import re
from urllib.parse import urljoin
from utilities import configReader


class CarBase:

    def __init__(self, page):
        self.page = page


    def get_title(self):
        return self.page.locator(
            configReader.readConfig("locators", "carTitle_XPATH")
        ).inner_text()

    def get_car_name_and_prices(self):
        car_names = self.page.locator(
            configReader.readConfig("locators", "carName_XPATH")
        )

        # Save names and URLs before navigating away
        cars = []

        for i in range(car_names.count()):
            car = car_names.nth(i)
            name = car.inner_text().strip()
            href = car.locator("xpath=ancestor::a[1]").get_attribute("href")

            if name and href:
                full_url = urljoin(self.page.url, href)

                # Prevent duplicate cars
                if (name, full_url) not in cars:
                    cars.append((name, full_url))

        car_details = []

        for name, url in cars:
            self.page.goto(url, wait_until="domcontentloaded")

            # Matches only exact price text such as:
            # Rs. 11.70 - 16.87 Lakh
            # Rs. 1.20 Crore
            price_locator = self.page.get_by_text(
                re.compile(
                    r"^Rs\.\s*[\d,.]+"
                    r"(?:\s*-\s*[\d,.]+)?"
                    r"\s*(?:Lakh|Crore)(?:\s*onwards)?$",
                    re.IGNORECASE
                )
            ).first

            try:
                price_locator.wait_for(state="visible", timeout=10000)
                price = price_locator.inner_text().strip()

                car_details.append((name, price))
                print(f"{name} ---- price is ---- {price}")

            except Exception:
                # Upcoming cars may not have an actual price
                print(f"{name} ---- skipped because price is unavailable")

        return car_details