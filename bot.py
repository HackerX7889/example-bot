import os
# os.system('pip install discord')
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
# intents.message_content = True 
bot = commands.Bot(command_prefix='$', intents=intents)
TOKEN = 'your-token-here'

async def set_custom_presence():
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Someting" #change this to anything you want to show as the bot status
        )
    )

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # Set custom presence
    await set_custom_presence()

@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000
    await ctx.send(f'Pong! Latency: {latency:.2f}ms')

@bot.event
async def on_message(message):
    if message.content.startswith('$spam'):
        await message.channel.send('What word do you want to spam?')
        word = await bot.wait_for('message', check=lambda m: m.author == message.author)
        await message.channel.send(f'Spamming "{word.content}" now. Type "$stop" to stop.')
        while True:
            await message.channel.send(word.content)
            await asyncio.sleep(1)
            stop = await bot.wait_for('message', check=lambda m: m.content == '$stop' and m.author == message.author)
            if stop:
                await message.channel.send('Stopped spamming.')
                break

bot.run(TOKEN)
