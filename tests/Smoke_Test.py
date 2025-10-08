# Selenium tests using Firefox for GitHub Actions CI/CD
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

class TestSmokeSuite():
    def setup_method(self, method):
        options = Options()
        options.headless = True  # headless mode for GitHub Actions
        self.driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=options
        )
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()
    
    def test_homePage(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        self.driver.set_window_size(626, 672)
        self.driver.find_element(By.CSS_SELECTOR, ".header-logo img").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".header-logo img")
        assert len(elements) > 0
        self.driver.find_element(By.CSS_SELECTOR, ".header-title > h1").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".header-title > h1").text == "Teton Idaho"
        assert self.driver.find_element(By.CSS_SELECTOR, ".header-title > h2").text == "Chamber of Commerce"
        assert self.driver.title == "Teton Idaho CoC"
    
    def test_homeNavigation(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        self.driver.set_window_size(626, 672)
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".spotlight1 > .centered-image")
        assert len(elements) > 0
        self.driver.find_element(By.LINK_TEXT, "Join Us").click()
        assert self.driver.title == "Teton Idaho CoC"
    
    def test_directoryPage(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        self.driver.set_window_size(1066, 672)
        self.driver.find_element(By.CSS_SELECTOR, "#hamburger-equiv > img").click()
        self.driver.find_element(By.LINK_TEXT, "Directory").click()

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".gold-member"))
        )

        elements = self.driver.find_elements(By.CSS_SELECTOR, ".gold-member")
        assert len(elements) > 0

        self.driver.find_element(By.ID, "directory-list").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".gold-member p")
        assert len(elements) > 0

    def test_joinPage(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        self.driver.set_window_size(723, 672)
        self.driver.find_element(By.CSS_SELECTOR, "#hamburger-equiv > img").click()
        self.driver.find_element(By.LINK_TEXT, "Join").click()
        self.driver.find_element(By.NAME, "fname").click()
        self.driver.find_element(By.NAME, "lname").click()
        elements = self.driver.find_elements(By.NAME, "lname")
        assert len(elements) > 0
        self.driver.find_element(By.NAME, "fname").click()
        elements = self.driver.find_elements(By.NAME, "fname")
        assert len(elements) > 0
        self.driver.find_element(By.NAME, "submit").click()
        self.driver.find_element(By.NAME, "fname").send_keys("john")
        self.driver.find_element(By.NAME, "lname").send_keys("john")
        self.driver.find_element(By.NAME, "bizname").send_keys("uchepromaxservices")
        self.driver.find_element(By.NAME, "biztitle").send_keys("ceo")
        self.driver.find_element(By.NAME, "submit").click()
        elements = self.driver.find_elements(By.NAME, "email")
        assert len(elements) > 0
        self.driver.find_element(By.NAME, "email").send_keys("udgdhh@gmail.com")
    
    def test_adminLogin(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        self.driver.set_window_size(626, 672)
        self.driver.find_element(By.CSS_SELECTOR, "#hamburger-equiv > img").click()
        self.driver.find_element(By.LINK_TEXT, "Admin").click()
        self.driver.find_element(By.ID, "username").send_keys("fakeuser")
        self.driver.find_element(By.ID, "password").send_keys("wrongpass")
        self.driver.find_element(By.CSS_SELECTOR, ".mysubmit:nth-child(4)").click()
        element = self.driver.find_element(By.CSS_SELECTOR, "html")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        actions.move_to_element(element).perform()
        actions.move_to_element(element).release().perform()
        self.driver.find_element(By.CSS_SELECTOR, "fieldset").click()
        self.driver.find_element(By.CSS_SELECTOR, ".mysubmit:nth-child(4)").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".myinput:nth-child(2)")
        assert len(elements) > 0
