import time
from driver_setup import setup_driver
from tours_parsing import open_live_tab, extract_href_and_id
from utils import save_to_json, load_from_json
from hrefs_filter import find_live_match_links_all
from check_strategy import analyze_first_set_winner_stats
from data_change import clear_old_links_if_needed

def main():
    clear_old_links_if_needed()
    driver = setup_driver()

    print("🔄 Запущен цикл проверки каждые 10 минут. Чтобы остановить — закрой процесс.")
    while True:
        print("\n⏱️ Новая итерация парсинга...")

        # Переходим на вкладку "Live" перед каждым анализом
        open_live_tab(driver)

        live_links = find_live_match_links_all(driver,
                                               allowed_categories=["ATP - SINGLES", "CHALLENGER MEN - SINGLES"],
                                               allowed_surfaces=["hard", "grass", "hard(indoor)", "clay"])
        if live_links:
            print("Найденные ссылки:")
            for link in live_links:
                print(link)
                analyze_first_set_winner_stats(driver, link)
        else:
            print("Ссылок не найдено.")

        print("⏳ Ожидание 7 минут до следующей проверки...")
        time.sleep(420)  # 10 минут


if __name__ == "__main__":
    main()
