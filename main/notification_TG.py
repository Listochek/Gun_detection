from token_tg import TOKEN, users_TG_ID # ФАЙЛ В КОТОРОМ ТОКЕН ТЕЛЕГРАММА
import telebot

bot = telebot.TeleBot(TOKEN)


def send_message_to_users(message):
    for user_id in users_TG_ID:
        bot.send_message(user_id, message)

message_to_send = "Обнаржено оружие\nПожалуйста примите меры, будьте осторожны"

send_message_to_users(message_to_send)

if __name__ == '__main__':
    send_message_to_users(message_to_send)