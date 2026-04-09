TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
YOUR_CHAT_ID = int(os.environ.get("YOUR_CHAT_ID", "0"))

# Отладка — покажет что видит бот
print("=== ПРОВЕРКА ПЕРЕМЕННЫХ ===")
print(f"TELEGRAM_TOKEN: {TELEGRAM_TOKEN[:10] if TELEGRAM_TOKEN else 'ПУСТО!'}")
print(f"ANTHROPIC_API_KEY: {'OK' if ANTHROPIC_API_KEY else 'ПУСТО!'}")
print(f"SPREADSHEET_ID: {'OK' if SPREADSHEET_ID else 'ПУСТО!'}")
print(f"YOUR_CHAT_ID: {YOUR_CHAT_ID}")
print("===========================")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден! Проверь Variables в Railway.")
