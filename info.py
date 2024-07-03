import asyncio
from aiogram import Bot, Dispatcher, types
from a2s import ServerQuerier
from cachetools import TTLCache
from PIL import Image
from io import BytesIO
import requests  # import the requests library

# Your existing code...

TOKEN = '7315183576:AAGEb0ERUCo7IoJadMVy2-w75gUhxSgN_Zk'
SERVER_ADDRESS = ('185.217.131.10', 27777)  # Replace with your CS 1.6 server IP and port

# Cache configuration
cache = TTLCache(maxsize=1, ttl=60)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['infocspro'])
async def cs_pro_info(message: types.Message):
    try:
        with ServerQuerier(SERVER_ADDRESS) as server:
            info = server.info()
            players = server.players()

            response = f"<b>Server Name:</b> {info['server_name']}\n"
            response += f"<b>Map:</b> {info['map']}\n"
            response += f"<b>Players:</b> {len(players)}/{info['max_players']}\n\n"

            for player in players:
                response += f"Player: {player['name']} | Kills: {player['frags']}\n"

            # Map image
            map_image_url = f"https://image.gametracker.com/images/maps/160x120/cs/{info['map']}.jpg"

            # Send message with map image
            image = Image.open(BytesIO(requests.get(map_image_url).content))
            bio = BytesIO()
            image.save(bio, format='JPEG')
            bio.seek(0)
            await bot.send_photo(message.chat.id, bio, caption=response, parse_mode=types.ParseMode.HTML)
            
    except Exception as e:
        await message.reply("Failed to fetch CS server info.")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start_polling())
    loop.run_forever()
