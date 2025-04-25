from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
from datetime import datetime
from telegram_sender import send_telegram_message


def load_processed_links(filename="processed_links.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)  # теперь список словарей
    return []

def save_processed_link(link, winner_name, filename="processed_links.json"):
    links = load_processed_links(filename)

    # Проверим, есть ли уже такая ссылка
    if any(entry["link"] == link for entry in links):
        return

    entry = {
        "link": link,
        "winner_name": winner_name,
        "timestamp": datetime.now().isoformat()
    }

    links.append(entry)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(links, file, ensure_ascii=False, indent=2)


def analyze_first_set_winner_stats(driver, link):
    processed_links = load_processed_links()
    if any(entry["link"] == link for entry in processed_links):
        print("🔁 Ссылка уже обработана. Пропускаем.")
        return

    driver.get(link)
    time.sleep(2)  # дожидаемся полной загрузки

    try:
        score_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "detailScore__wrapper"))
        )
        spans = score_element.find_elements(By.TAG_NAME, "span")
        if len(spans) >= 3:
            p1_score = spans[0].text.strip()
            p2_score = spans[2].text.strip()
            print(f"Счёт: {p1_score}-{p2_score}")
        else:
            print("⚠️ Неверный формат счёта.")
            return

        if (p1_score, p2_score) not in [("1", "0"), ("0", "1")]:
            print("⚠️ Матч не подходит по счёту.")
            return

        winner = "player1" if p1_score == "1" else "player2"

        # Получаем имена игроков
        try:
            player1_name = driver.find_element(By.CSS_SELECTOR, ".duelParticipant__home .participant__participantName").text.strip()
            player2_name = driver.find_element(By.CSS_SELECTOR, ".duelParticipant__away .participant__participantName").text.strip()
        except Exception as e:
            print(f"⚠️ Не удалось получить имена игроков: {e}")
            return

        # Кликаем на вкладку "Stats"
        try:
            stats_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Stats')]"))
            )
            stats_button.click()
            time.sleep(1.5)
        except Exception as e:
            print(f"⚠️ Не удалось нажать на 'Stats': {e}")
            return

        # Кликаем на вкладку "Set 1"
        try:
            set1_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Set 1')]"))
            )
            set1_button.click()
            time.sleep(1.5)
        except Exception as e:
            print(f"⚠️ Не удалось нажать на 'Set 1': {e}")
            return

        # Парсим статистику победителя 1-го сета
        target_stats = ["Double Faults", "1st Serve Points Won"]
        results = {}
        stat_rows = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".wcl-row_OFViZ[data-testid='wcl-statistics']")))

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

        # Выводим значения для победителя первого сета
        for stat_name in target_stats:
            stat_value = results.get(stat_name, {}).get(winner)
            print(f"{stat_name} ({winner}): {stat_value}")

        # Проверка условий для победителя сета
        double_faults = results.get("Double Faults", {}).get(winner, "-1")
        first_serve_won = results.get("1st Serve Points Won", {}).get(winner, "0%")

        try:
            double_faults_int = int(double_faults)
            serve_won_percent = int(first_serve_won.replace("%", ""))

            winner_name = player1_name if winner == "player1" else player2_name

            if double_faults_int == 0 and serve_won_percent > 70:
                print(f"✅ Матч подходит. Игрок: {winner_name}")
                save_processed_link(link, winner_name)
                send_telegram_message(f"✅ Матч: {winner_name}\nСсылка: {link}")
            else:
                print(f"❌ Матч не подходит. Игрок: {winner_name}")
        except Exception as e:
            print(f"⚠️ Ошибка при проверке условий: {e}")

    except Exception as e:
        print(f"❌ Ошибка в обработке матча по ссылке {link}: {e}")
