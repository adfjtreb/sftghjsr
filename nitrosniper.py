import re, aiohttp, os
from keep_alive import keep_alive
import discord



codeRegex = re.compile("(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")
token = os.getenv("TOKEN")

bot = commands.Bot(command_prefix=".", self_bot=True)


@bot.event
async def on_ready():
    print(f"{bot.user} now has a active nitro sniper!")

@bot.event
async def on_message(message):
    if codeRegex.search(message.content):
        code = codeRegex.search(message.content).group(2)
        if len(code) < 16:
            print(f"Auto Detected Fake Code | {code}")
        if len(code) > 25:
            print(f"Auto Detected Fake Code | {code}")
        async with aiohttp.ClientSession() as session:
            result = await session.post(f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem", json={'channel_id': str(message.channel.id)}, headers={'authorization': token, 'user-agent': 'Mozilla/5.0'})
            if "This gift has been redeemed already" in await result.text():
                print("Code has already been redeemed.")
            elif "Unknown Gift Code" in await result.text():
                pass
            elif "nitro" in await result.text():
                print("Nitro code redeemed!")

bot.run(token, reconnect = True, bot = False)