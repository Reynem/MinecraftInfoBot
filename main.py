import telebot
from telebot import formatting
from config import TOKEN
from minecraft_server_info import getMcServerInfo

help_text = """Get Minecraft information bot
Я - бот, который позволяет получать иныормацию о серверах Minecraft

Команды:
	/stats <ip>"""


def getDescServer(adress):
    try:
        data = getMcServerInfo(adress)

        msg = f"""*Информация о сервере Minecraft*

Запрос: `{adress}`
Цифровой IP: `{data['adress']}`

Описание:
`{'\n'.join(data['motd'])}`
Онлайн игрков: `{data['players']}` / `{data['max players']}`
Список игроков: {', '.join("`" + i["name"] + "`" for i in data['players list'])}
Версия: `{data['version']}`
"""
    except KeyError as e:
        return f"Некорректные данные от API: отсутствует ключ {e}"
    except Exception as e:
        return f"Неизвестная ошибка: {str(e)}"
    return msg




bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def on_message(msg):
    bot.send_message(msg.chat.id, 'Bot start!')


@bot.message_handler(content_types='text')
def on_message(msg):
    msg_text = msg.text
    msg_text_lower = msg_text.lower()
    if msg_text.lower() in ('hello!', 'привет'):
        bot.send_message(msg.chat.id, 'Привет!')
    elif msg_text.lower() in ("/help", "/?"):
        bot.send_message(msg.chat.id, help_text)

    elif msg_text.lower().startswith("/"):
        spl = msg_text_lower.split()
        if spl[0] in ("/stats", "/info"):
            try:
                ip = spl[1]
                text = getDescServer(ip)
                bot.send_message(msg.chat.id, f"{text}", parse_mode='MarkdownV2')
            except IndexError:
                bot.send_message(msg.chat.id, "**ERROR** \nLen args not 2!")


    else:
        bot.send_message(msg.chat.id, '🚫Запрос не распознан. Введите /help')


bot.infinity_polling(none_stop=True)
