from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def apply_vashlijvari_filter(driver):
    try:
        print("Opening swoop.ge...")
        driver.get("https://swoop.ge/")

        print("Looking for 'დასვენება' link...")
        leisure_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "დასვენება"))
        )

        print("Found 'დასვენება' link, clicking...")
        leisure_link.click()

        print("Waiting for page to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "grid"))
        )

        time.sleep(3)

        print("Looking for 'ვაშლიჯვარი' filter checkbox...")

        try:
            disclosure_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "headlessui-disclosure-button-:rgs:"))
            )
            if disclosure_button.is_displayed():
                print("Opening location filter panel...")
                disclosure_button.click()
                time.sleep(2)
        except:
            print("Filter panel is likely already open or structured differently")

        vashlijvari_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "checkbox-მდებარეობა-0"))
        )

        label_element = driver.find_element(By.XPATH, f"//label[@for='checkbox-მდებარეობა-0']")
        if "ვაშლიჯვარი" in label_element.text:
            print(f"Found 'ვაშლიჯვარი' checkbox, clicking...")
            vashlijvari_checkbox.click()
            print("Filter applied successfully!")

            time.sleep(5)
        else:
            print(f"Warning: Expected 'ვაშლიჯვარი' but found '{label_element.text}' instead")

        print("Filter application complete. Browser will remain open for 10 seconds so you can see the results.")
        time.sleep(10)

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Closing browser...")
        driver.quit()


if __name__ == "__main__":
    firefox_options = Options()
    firefox_options.add_argument("--headless")

    driver = webdriver.Firefox(options=firefox_options)
    
    apply_vashlijvari_filter(driver)