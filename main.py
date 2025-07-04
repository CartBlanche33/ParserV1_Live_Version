import time
from driver_setup import setup_driver
from tours_parsing import open_live_tab
from hrefs_filter import find_live_match_links_all
from check_strategy import analyze_first_set_winner_stats
from data_change import clear_old_links_if_needed

def main():
    clear_old_links_if_needed()

    print("🔄 Запущен цикл проверки каждые 10 минут. Нажми Ctrl+C для выхода.")

    while True:
        print("\n⏱️ Новая итерация парсинга...")

        driver = setup_driver()
        try:
            open_live_tab(driver)

            live_links = find_live_match_links_all(driver,
                allowed_categories=["ATP - SINGLES", "CHALLENGER MEN - SINGLES"],
                allowed_surfaces=["hard", "grass", "hard(indoor)"]
            )

            if live_links:
                print("Найденные ссылки:")
                for link in live_links:
                    print(link)
                    analyze_first_set_winner_stats(driver, link)
            else:
                print("Ссылок не найдено.")

        finally:
            driver.quit()  # <<< Обязательно закрываем драйвер после одной итерации

        print("⏳ Ожидание 10 минут до следующей проверки...")
        time.sleep(900)  # <<< 600 секунд = 10 минут

if __name__ == "__main__":
    main()
