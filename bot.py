import os
import json
import logging
from datetime import datetime, date
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ========== НАСТРОЙКИ ==========
TELEGRAM_TOKEN = "8626316824:AAGflK7iqjyp7-6cZdb8CUYE15dw88bQXnw"
GEMINI_API_KEY = "AIzaSyDCYgEB9H-TNztXpR1vKr-Vjh2CKsXBgG0"
SPREADSHEET_ID = "1Yuv91lSJLJClaUudYlgRqnlYNSMADxYTPlyepozAuYw"
YOUR_CHAT_ID = 408480459

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== GOOGLE SHEETS ==========
def get_sheet():
    creds_dict = {
        "type": "service_account",
        "project_id": "my-project-assistant-492810",
        "private_key_id": "c55f83b3bbd9bbb90dcf7f807369986c4ccd7067",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDLVobuCffaGfbp\nvh52KH4xzXWi2InQpW43Tu7s9o4RtJxhpIF/2zfC1V6hGvtUQWRATtRs8kQFiyeq\nm9A1Wm34AInKnE9IswQHBXMWcCTMaqz0BMrXEBJEm/k0ckueB7PS0hkrv6tyfgm9\nc9LBze5dfevWagRYJhII2qcBBN/p3nzDOO39p0LGbDJrFN/HUmAw0F1B2MoaBFTB\nX4qy1Qf2bS0CXZ4B5sZTUTFhw8yrkkeolwGBUEugjH4IEzX5gTucxgIMz1cVC+Qe\nChC8W87pWJHBMj5tg7NtKF2RKPGnanePgH7kjFRA38sY4KAklYjxfZJB21Ryqphu\nEGT4aN45AgMBAAECggEAA4QuNn+a9v1BSoQsfVlF6rvlhONpvrSdq1HaH+RDoLAW\n5DlhY+yj541OYvWB0yXZA05ZrhNNHytrjC/AR1aWVZZCIRbYPXxFsuQNPB4Zr3nz\nc7osJ9FHVO29lC1F0X3LRky2fWMwe9JiKLyQBc9Mh/ay1V+6o4DvtDzTwS4XETGX\n3A3Jzs21nc86FcbLWqdtaBovGPUNL4fYoStmWd5K+1xfjshvSxByhmx+TixMNUdh\nSlskXtcfU2P6PgSW6c0AMyhO2NSsjA89JXrFDgq7I88N3EHLyCy2R6InJ3S9emTw\nMHfR1Wz0QIqFAubCMfBWVGYehOo6HI7cb9U4w/W+4QKBgQD3T1lr2nqQXejfAobb\newPDj+/TuLkmRhkR8nVrzPYBG8TAqtkvzDRURDNJp8LdShDMUo6H0zfJPOwI8oAO\n0S2riitvlFc1iXW+5WXy8XJa+P3avioQurD+g2Lu7hDyfgHb8AEQATD0e8m+ol4N\ndtqsoDwtf2FDVfY0s5HTJhvvHwKBgQDSe6Hy8eQEvPP9WLHnDtdVDf7V7WG3RdTw\nDnTFKX2OAo8RRqcy/bygsflMUc+bTDcc+hOa9ss4VaD9+FLKwj87tR/Xe+PxMPsR\ne4VtHq/2YH+vCSISJcLK0i6D9Va7Spg2aUizk4SOt4JsN527eymiBik+IEZ8AMbW\neHaalwD/pwKBgQCovmaoVbmdOcaEK+gyZ7xIurSMRRVoDRpcCZCfDomodfcI80of\n9/iYqrRIBITMkxXlJEuGV9NPpxbyf+xqr8W2rx82EgRzTiieKU4ntyEs+4nSsEBp\ni8jq0GE34A6GNv4zwI4pCncJylD8lzMPgtJwSSDmdmy6EjRc/013wh/7RwKBgQCb\n0td0SkuqjlB7cJxUGJKl7zSIH7NFwTcBeVJNXIgNCCvueEXz5BEvTlLng3GU4Pm0\nRBcblDWiwRHss1hnryKtC0xFdPytZLual72RqTRPy+T7KmHE2Zu6F5xEKO9KvNCv\nB4bBGyb5mTW+8/WcBHQv9Su3SKGlz9Vklc4IaF5e5QKBgQDS/6diWLPbEvYSrr24\niN+bVdUB5G/apHS43w5CxEZJrw7EFG5EJIcmMN4Gk3aPLfRvTeE7Yw9iXGnpJLpq\nwsE8PsTzAAWOHMU9+Q8nx9KIKRfawO5DxX1Nsb9KMHnMjPaX06Th3W7zYWTW9PV+\nvLK0yejQbugWZI2MlCaUkfsHFg==\n-----END PRIVATE KEY-----\n",
        "client_email": "my-project-assistant@my-project-assistant-492810.iam.gserviceaccount.com",
        "client_id": "107294993902256940327",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-project-assistant%40my-project-assistant-492810.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).sheet1

def add_task(task_text: str, due_date: str = "") -> int:
    sheet = get_sheet()
    all_rows = sheet.get_all_values()
    task_id = len(all_rows)  # ID = номер строки
    created_at = datetime.now().strftime("%d.%m.%Y %H:%M")
    sheet.append_row([task_id, task_text, due_date, "❌ Не выполнено", created_at])
    return task_id

def get_pending_tasks() -> list:
    sheet = get_sheet()
    rows = sheet.get_all_values()
    pending = []
    for row in rows[1:]:  # пропускаем заголовок
        if len(row) >= 4 and row[3] == "❌ Не выполнено":
            pending.append(row)
    return pending

def mark_done(task_id: int):
    sheet = get_sheet()
    rows = sheet.get_all_values()
    for i, row in enumerate(rows):
        if row and str(row[0]) == str(task_id):
            sheet.update_cell(i + 1, 4, "✅ Выполнено")
            return True
    return False

# ========== CLAUDE AI ==========
def analyze_message(user_message: str) -> dict:
    import urllib.request
    import urllib.error
    import time
    today = date.today().strftime("%d.%m.%Y")
    
    prompt = f"""Сегодня: {today}.
Анализируй сообщение и отвечай ТОЛЬКО в формате JSON без markdown:
{{
  "is_task": true/false,
  "task_text": "текст задачи",
  "has_date": true/false,
  "due_date": "дата ДД.ММ.ГГГГ или пустая строка",
  "needs_date_clarification": true/false,
  "response": "ответ пользователю на русском"
}}
Сообщение: {user_message}"""

    data = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read())
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(10)
                continue
            raise


def get_ai_response(prompt: str) -> str:
    import urllib.request
    data = json.dumps({
        "contents": [{"parts": [{"text": f"Ты помощник по задачам. Отвечай кратко на русском.\n{prompt}"}]}]
    }).encode()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    
    return result["candidates"][0]["content"]["parts"][0]["text"]

def get_ai_response(prompt: str) -> str:
    """Обычный ответ от Claude для не-задачных сообщений"""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system="Ты дружелюбный помощник по задачам. Отвечай кратко на русском.",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

# ========== TELEGRAM HANDLERS ==========

# Хранилище ожидающих уточнения дат
pending_date_tasks = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        f"👋 Привет! Я твой ИИ-помощник по задачам.\n\n"
        f"📝 Просто напиши мне задачу, например:\n"
        f"• «Купить продукты завтра»\n"
        f"• «Позвонить Ивану 15.06»\n"
        f"• «Сдать отчёт до пятницы»\n\n"
        f"📋 /tasks — список невыполненных задач\n"
        f"✅ /done [номер] — отметить задачу выполненной\n\n"
        f"Твой Chat ID: `{chat_id}` (сохрани его в настройках!)",
        parse_mode="Markdown"
    )

async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = get_pending_tasks()
    if not tasks:
        await update.message.reply_text("🎉 Все задачи выполнены! Нет активных задач.")
        return
    
    text = "📋 *Невыполненные задачи:*\n\n"
    for task in tasks:
        task_id = task[0]
        task_text = task[1]
        due_date = task[2] if task[2] else "без срока"
        text += f"#{task_id} — {task_text}\n📅 Срок: {due_date}\n\n"
    
    text += "Чтобы отметить выполненной: `/done [номер]`"
    await update.message.reply_text(text, parse_mode="Markdown")

async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажи номер задачи: `/done 3`", parse_mode="Markdown")
        return
    
    try:
        task_id = int(context.args[0])
        success = mark_done(task_id)
        if success:
            await update.message.reply_text(f"✅ Задача #{task_id} отмечена как выполненная!")
        else:
            await update.message.reply_text(f"❌ Задача #{task_id} не найдена.")
    except ValueError:
        await update.message.reply_text("Введи число, например: `/done 3`", parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.effective_chat.id
    
    # Проверяем, ждём ли дату для предыдущей задачи
    if chat_id in pending_date_tasks:
        task_text = pending_date_tasks.pop(chat_id)
        # Пробуем извлечь дату из ответа
        result = analyze_message(f"Дата для задачи: {user_message}")
        due_date = result.get("due_date", user_message)
        task_id = add_task(task_text, due_date)
        await update.message.reply_text(
            f"✅ Задача сохранена!\n\n"
            f"📝 *{task_text}*\n"
            f"📅 Срок: {due_date}\n"
            f"🔖 ID: #{task_id}",
            parse_mode="Markdown"
        )
        return
    
    # Анализируем сообщение через Claude
    try:
        result = analyze_message(user_message)
    except Exception as e:
        logger.error(f"Ошибка Claude: {e}")
        await update.message.reply_text("⚠️ Ошибка обработки. Попробуй ещё раз.")
        return
    
    if result.get("is_task"):
        task_text = result.get("task_text", user_message)
        due_date = result.get("due_date", "")
        
        if result.get("needs_date_clarification"):
            # Сохраняем задачу, ждём дату
            pending_date_tasks[chat_id] = task_text
            await update.message.reply_text(
                f"📝 Понял, задача: *{task_text}*\n\n"
                f"📅 До какого числа нужно выполнить? (или напиши «без срока»)",
                parse_mode="Markdown"
            )
        else:
            task_id = add_task(task_text, due_date)
            reply = result.get("response", "Задача сохранена!")
            date_line = f"\n📅 Срок: {due_date}" if due_date else ""
            await update.message.reply_text(
                f"✅ {reply}\n\n"
                f"📝 *{task_text}*{date_line}\n"
                f"🔖 ID: #{task_id}",
                parse_mode="Markdown"
            )
    else:
        response = result.get("response") or get_ai_response(user_message)
        await update.message.reply_text(response)

# ========== ПЛАНИРОВЩИК НАПОМИНАНИЙ ==========
async def send_reminders(app: Application):
    tasks = get_pending_tasks()
    if not tasks:
        return
    
    today = date.today().strftime("%d.%m.%Y")
    overdue = []
    due_today = []
    
    for task in tasks:
        task_due = task[2] if len(task) > 2 else ""
        if task_due:
            if task_due < today:
                overdue.append(task)
            elif task_due == today:
                due_today.append(task)
    
    if not overdue and not due_today:
        return
    
    text = "⏰ *Напоминание о задачах!*\n\n"
    
    if due_today:
        text += "🔔 *Срок сегодня:*\n"
        for t in due_today:
            text += f"• #{t[0]} — {t[1]}\n"
        text += "\n"
    
    if overdue:
        text += "🚨 *Просроченные:*\n"
        for t in overdue:
            text += f"• #{t[0]} — {t[1]} (срок был {t[2]})\n"
    
    text += "\nОтметь выполненные: `/done [номер]`"
    
    try:
        await app.bot.send_message(
            chat_id=YOUR_CHAT_ID,
            text=text,
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Ошибка отправки напоминания: {e}")

# ========== ЗАПУСК ==========
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tasks", show_tasks))
    app.add_handler(CommandHandler("done", done_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Напоминания каждый день в 9:00 и 18:00
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_reminders, "cron",
        hour=9, minute=0,
        args=[app]
    )
    scheduler.add_job(
        send_reminders, "cron",
        hour=18, minute=0,
        args=[app]
    )
    scheduler.start()
    
    logger.info("Бот запущен!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
