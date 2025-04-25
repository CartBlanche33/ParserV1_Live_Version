from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_live_tab(driver):
    driver.get("https://www.flashscore.com/tennis/")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'filters__tab') and div[contains(text(), 'LIVE')]]"))
    ).click()
    time.sleep(5)

def extract_href_and_id(driver):
    """
    Извлекает href и id матчей из текущего HTML-кода, используя Selenium WebDriver.

    Args:
        driver: Объект Selenium WebDriver.

    Returns:
        list: Список словарей, где каждый словарь содержит 'Ид матча' и 'Ссылка'.
    """
    matches = driver.find_elements(By.CLASS_NAME, "event__match")
    data = []
    for match in matches:
        match_id_element = match.get_attribute("id")
        link_elements = match.find_elements(By.CLASS_NAME, "eventRowLink")
        if match_id_element and link_elements:
            href = link_elements[0].get_attribute("href")
            match_id = match_id_element.split('_')[-1]
            data.append({"Ид матча": match_id, "Ссылка": href})
    return data
