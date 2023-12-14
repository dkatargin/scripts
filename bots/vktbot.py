import requests
import textwrap

CHAT_ID="***"
BOT_TOKEN="***"

def main():
    api_url = f"https://api.internal.myteam.mail.ru/bot/v1/messages/sendText"
    txt = "#публикации за сутки\n\n Название: По полной вверх (fullup)\n Кабинет: https://developers.vkplay.ru/dev/games/32282/admin/\n Дата публикации: 2023-11-28 22:00:02\n\n"
    for m in textwrap.wrap(txt, width=500, break_long_words=False,replace_whitespace=False):
        params = {
                "token": BOT_TOKEN,
                "chatId": CHAT_ID,
                "text": m,
                "parseMode": "HTML",
            }
        res = requests.post(api_url, params=params, timeout=10).json()
        print(res)

if __name__ == "__main__":
    main()