from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def login_to_swoop():
    firefox_options = Options()

    driver = webdriver.Firefox(options=firefox_options)

    try:

        print("Opening swoop.ge...")
        driver.get("https://swoop.ge/")

        time.sleep(3)

        print("Looking for the 'შესვლა' (Login) button...")

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'შესვლა')]"))
        )

        print("Found login button, clicking...")
        login_button.click()

        print("Waiting for login page to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Email"))
        )

        print("Filling in login credentials...")
        email_field = driver.find_element(By.ID, "Email")
        password_field = driver.find_element(By.ID, "Password")

        email_field.send_keys("DavitiTeslia@wow.com")
        password_field.send_keys("RagacaParoli")

        print("Login credentials entered successfully!")

        time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Closing browser...")
        driver.quit()


if __name__ == "__main__":
    login_to_swoop()
