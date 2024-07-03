import telegram
import telebot
import socket

bot_token = "7315183576:AAGEb0ERUCo7IoJadMVy2-w75gUhxSgN_Zk"  # Bot tokenini kiriting
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['infocspro'])
def send_server_info(message):
    ip = "185.217.131.10"  # Server IP manzilini kiriting
    port = 27777  # Server portini kiriting

    info = get_server_info(ip, port)
    if info:
        server_name = info['server_name']
        map_name = info['map_name']

        response = f"Server nomi: {server_name}nXarita nomi: {map_name}"
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "Serverdan ma'lumot olishda xato yuz berdi.")

def get_server_info(ip, port):
    try:
        # Serverga ulanish uchun socket yaratamiz
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)

        # A2S_INFO so'rovi paketi
        packet = b'xFFxFFxFFxFFTSource Engine Queryx00'

        # Serverga so'rovni yuborish
        sock.sendto(packet, (ip, port))

        # Javobni qabul qilish
        response, _ = sock.recvfrom(4096)
        response = response[4:]  # Avvalgi 4 baytni o'tkazib yuborish

        # Ma'lumotlarni ajratib olish
        server_name = response[6:response.find(b'x00', 6)].decode()
        map_name = response[response.find(b'x00', 6) + 1:response.find(b'x00', response.find(b'x00', 6) + 1)].decode()

        return {
            'server_name': server_name,
            'map_name': map_name
        }
    except socket.error as e:
        print(f"Serverga ulanishda xato yuz berdi: {e}")
        return None

bot.polling()
