from re import search
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import booking.constants as const
from selenium.webdriver.common.by import By
import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time
from booking.booking_filtration import BookingFiltration


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\Users\Korisnik\Downloads", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self):
        currency_element = self.find_element(
            By.CSS_SELECTOR, '[data-testid="header-currency-picker-trigger"]'
        )
        currency_element.click()

        selected_currency_element = self.find_elements(
            By.CSS_SELECTOR, '[data-testid="selection-item"]'
        )[1]
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        wait = WebDriverWait(self, 10)

        search_field = wait.until(EC.presence_of_element_located((By.ID, ":rh:")))
        search_field.clear()
        search_field.send_keys(place_to_go)

        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.ID, "autocomplete-result-0")))
        first_result = self.find_element(By.ID, "autocomplete-result-0")
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        wait = WebDriverWait(self, 20)

        check_in_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"span[data-date='{check_in_date}']"))
        )
        check_in_element.click()

        check_out_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"span[data-date='{check_out_date}']"))
        )
        check_out_element.click()

    def select_adults(self, count=1):
        selection_element = self.find_element(By.XPATH, '//button[span[contains(text(), "2 adults")]]')
        selection_element.click()

        while True:
            decrease_adults_element = self.find_element(
                By.CSS_SELECTOR, 'button.a83ed08757.c21c56c305.f38b6daa18.d691166b09'
            )
            decrease_adults_element.click()

            try:
                adults_value_element = WebDriverWait(self, 10).until(
                    EC.visibility_of_element_located((By.ID, "group-adults"))
                )
                adults_value = adults_value_element.get_attribute('value')

                if int(adults_value) == 1:
                    break

            except TimeoutException:
                print("Timeout while waiting for adults value element.")
                break

        increase_button_element = self.find_element(
            By.CSS_SELECTOR, 'button.a83ed08757.c21c56c305.f38b6daa18.d691166b09.f4d78af12a'
        )

        for _ in range(count - 1):
            increase_button_element.click()

    def cliclk_search(self):
        search_button = self.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        search_button.click()

    def apply_filtration(self):
        filtration = BookingFiltration(driver = self)
        filtration.apply_star_rating(star_value = 5)
        filtration.sort_price_highest_first()

