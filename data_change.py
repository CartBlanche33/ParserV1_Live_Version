from datetime import datetime, timedelta
import os
import json

def clear_old_links_if_needed(links_filename="processed_links.json"):
    now = datetime.now()

    if not os.path.exists(links_filename):
        return

    with open(links_filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    # фильтруем только свежие записи
    fresh_data = [
        entry for entry in data
        if "timestamp" in entry and datetime.fromisoformat(entry["timestamp"]) > now - timedelta(hours=24)
    ]

    removed_count = len(data) - len(fresh_data)
    if removed_count > 0:
        print(f"🧹 Удалено {removed_count} устаревших ссылок из processed_links.json")
        with open(links_filename, "w", encoding="utf-8") as f:
            json.dump(fresh_data, f, ensure_ascii=False, indent=2)
    else:
        print("✅ Все ссылки свежие, очистка не требуется")
