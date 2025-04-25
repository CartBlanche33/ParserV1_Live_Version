from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from datetime import datetime, timedelta

CHECKED_LINKS_FILE = "checked_links.json"
LINK_EXPIRATION_HOURS = 24

def load_checked_links():
    try:
        with open(CHECKED_LINKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_checked_links(checked_links):
    with open(CHECKED_LINKS_FILE, "w") as f:
        json.dump(checked_links, f, indent=4)

def cleanup_old_links():
    checked_links = load_checked_links()
    now = datetime.now()
    expired_links = []
    for url, timestamp_str in checked_links.items():
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            if now - timestamp > timedelta(hours=LINK_EXPIRATION_HOURS):
                expired_links.append(url)
        except ValueError:
            print(f"Ошибка при парсинге timestamp для ссылки: {url}. Пропускаем удаление.")

    for url in expired_links:
        del checked_links[url]

    save_checked_links(checked_links)
    print(f"Выполнена очистка. Удалено {len(expired_links)} устаревших ссылок.")

def check_and_save_link(url):
    checked_links = load_checked_links()
    if url in checked_links:
        print(f"Ссылка '{url}' уже была проверена {checked_links[url]}. Пропускаем.")
        return

    driver = webdriver.Chrome()
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        stat_rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".wcl-row_OFViZ[data-testid='wcl-statistics']")))

        target_stats = ["Double Faults", "1st Serve Points Won"]
        results = {}
        player1_matches = False
        player2_matches = False
        reasons_p1 = []
        reasons_p2 = []

        for row in stat_rows:
            try:
                category_element = row.find_element(By.CSS_SELECTOR, ".wcl-category_7qsgP strong")
                category = category_element.text.strip()

                if category in target_stats:
                    results[category] = {}
                    home_value_element = row.find_element(By.CSS_SELECTOR, ".wcl-value_IuyQw.wcl-homeValue_-iJBW strong")
                    away_value_element = row.find_element(By.CSS_SELECTOR, ".wcl-value_IuyQw.wcl-awayValue_rQvxs strong")

                    results[category]["player1"] = home_value_element.text.strip()
                    results[category]["player2"] = away_value_element.text.strip()

            except Exception as e:
                print(f"Ошибка при обработке строки статистики: {e}")

        # Проверка условий для Игрока 1
        double_faults_p1 = int(results.get("Double Faults", {}).get("player1", -1))
        serve_points_p1_str = results.get("1st Serve Points Won", {}).get("player1", "0%")
        serve_points_p1 = int(serve_points_p1_str.replace("%", "")) if "%" in serve_points_p1_str else -1
        player1_matches = (double_faults_p1 <= 0 and serve_points_p1 >= 70)

        # Проверка условий для Игрока 2
        double_faults_p2 = int(results.get("Double Faults", {}).get("player2", -1))
        serve_points_p2_str = results.get("1st Serve Points Won", {}).get("player2", "0%")
        serve_points_p2 = int(serve_points_p2_str.replace("%", "")) if "%" in serve_points_p2_str else -1
        player2_matches = (double_faults_p2 <= 0 and serve_points_p2 >= 70)

        if player1_matches or player2_matches:
            print(f"Хотя бы один игрок на ссылке '{url}' соответствует условиям. Добавляем в проверенные.")
            checked_links[url] = datetime.now().isoformat()
            save_checked_links(checked_links)

    except Exception as e:
        print(f"Произошла ошибка при обработке ссылки '{url}': {e}")
    finally:
        driver.quit()

# Пример использования (предполагается, что твой парсер возвращает список новых ссылок)
def your_parser_function():
    # Здесь должна быть логика твоего парсера, который находит новые ссылки
    # В качестве примера вернем несколько статических ссылок
    return [
        "https://www.flashscore.com/match/tennis/je4fbhL8/#/match-summary/match-statistics/2",
        "https://www.flashscore.com/match/tennis/someotherlink1/#/match-summary/match-statistics/2",
        "https://www.flashscore.com/match/tennis/someotherlink2/#/match-summary/match-statistics/2"
    ]

if __name__ == "__main__":
    # Запускаем очистку устаревших ссылок при старте скрипта
    cleanup_old_links()

    while True:
        new_links = your_parser_function()
        for link in new_links:
            check_and_save_link(link)
        print("Ожидание 10 минут до следующей проверки...")
        time.sleep(600) # 600 секунд = 10 минут