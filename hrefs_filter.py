from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def find_live_match_links_all(driver, allowed_categories=None, allowed_surfaces=None):
    if allowed_categories is None:
        allowed_categories = ["ATP - SINGLES", "CHALLENGER MEN - SINGLES"]
    if allowed_surfaces is None:
        allowed_surfaces = ["hard", "grass", "hard(indoor)", "clay"]

    excluded_keywords = ["Qualification", "Australian Open", "Wimbledon", "US Open", "French Open"]
    live_match_links = []

    tournament_blocks = driver.find_elements(By.CLASS_NAME, "wcl-header_uBhYi.wclLeagueHeader.wclLeagueHeader--collapsed")
    print(f"Найдено блоков турниров: {len(tournament_blocks)}")

    for block in tournament_blocks:
        try:
            tournament_type_element = block.find_element(
                By.CSS_SELECTOR,
                ".wcl-overline_rOFfd.wcl-scores-overline-05_P-fjE.wclLeagueHeader__countryName"
            )
            tournament_type = tournament_type_element.text.strip()

            tournament_full_name_element = block.find_element(
                By.CSS_SELECTOR,
                "div.event__titleBox a.wclLeagueHeader__link strong[data-testid='wcl-scores-simpleText-01']"
            )
            tournament_full_name = tournament_full_name_element.text.strip()

            if tournament_type in allowed_categories and not any(keyword in tournament_full_name for keyword in excluded_keywords):
                found_surface = None
                for surface in allowed_surfaces:
                    if surface.lower() in tournament_full_name.lower():
                        found_surface = surface.lower()
                        break

                if found_surface:
                    print(f"\nТурнир '{tournament_full_name}' ({tournament_type}, {found_surface}) соответствует фильтрам. Поиск матчей...")
                    parent_element = block.find_element(By.XPATH, "..")
                    found_tournament_block = False

                    for child in parent_element.find_elements(By.XPATH, "./*"):
                        if child == block:
                            found_tournament_block = True
                            continue

                        if found_tournament_block and child.tag_name == 'div':
                            child_class = child.get_attribute("class")
                            if "event__match" in child_class and "event__match--live" in child_class:
                                try:
                                    link_element = child.find_element(By.CSS_SELECTOR, "a.eventRowLink")
                                    match_link = link_element.get_attribute("href")
                                    live_match_links.append(match_link)
                                    print(f"  Найдена ссылка на матч: {match_link}")
                                except Exception as e:
                                    print(f"  Ошибка при извлечении ссылки: {e}")
                            elif "wcl-header_uBhYi" in child_class and "wclLeagueHeader--collapsed" in child_class:
                                print("  Встречен следующий блок турнира. Завершаем поиск матчей для текущего турнира.")
                                break
                    if not live_match_links:
                        print("  Не найдено лайв-матчей для этого турнира.")
                else:
                    print(f"Турнир '{tournament_full_name}' не соответствует фильтрам по поверхности.")
            else:
                print(f"Турнир '{tournament_full_name}' не соответствует фильтрам (тип или исключен по ключевым словам).")

        except Exception as e:
            print(f"Произошла ошибка при обработке блока турнира: {e}")
            continue

    return live_match_links
