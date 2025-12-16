#This file will include a class with instance methods
#That will be responsible to interact with our website
#Aftee we have some results to apply filtrations
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def apply_star_rating(self, star_value):
        wait = WebDriverWait(self.driver, 10)
        star_filtration_box = wait.until(EC.presence_of_element_located((
            By.XPATH, "//div[contains(@data-testid, 'filters-group-container')]"))
        )
        star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, '*')

        for star_element in star_child_elements:
            if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                wait.until(EC.element_to_be_clickable(star_element)).click()

    def sort_price_highest_first(self):
        wait = WebDriverWait(self.driver, 10)
        sort_button = self.driver.find_element(By.XPATH, "//button[span/span[contains(text(), 'Sort by')]]")
        sort_button.click()

        highest_price = wait.until(EC.presence_of_element_located((
            By.XPATH, "//button[@data-id='price_from_high_to_low']"))
        )
        highest_price.click()
