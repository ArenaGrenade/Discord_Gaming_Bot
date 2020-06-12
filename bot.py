import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=SERVER)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_member_join(member):
    guild = discord.utils.get(client.guilds, name=SERVER)
    print(guild.channels.find(lambda x: x.name == 'welcoming'))
    general_channel = discord.utils.get(guild.channels, name="welcoming")
    hello_messages = ["Hello, sunshine! {}", "Howdy, partner! {}", "Hey, howdy, hi! {}", "Peek-a-boo! {}",
                      "Howdy-doody! {}", "Hey there, {}!", "I come in peace! {}", "Ahoy, matey! {}", "Hiya! {}",
                      "What’s crackin’? {}", "‘Ello, gov'nor! {}", "Here's {}. Say Hi!!", "Yo! {}", "Aloha! {}",
                      "At least, we meet for the first time for the last time! {}", "Hola! {}", "Que Pasa! {}",
                      "Bonjour! {}", "Hallo! {}", "Ciao! {}", "Konnichiwa! {}"]
    welcome_message = random.choice(hello_messages).format(member.name)
    await general_channel.send(welcome_message)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await message.channel.send(message.content)

if __name__ == '__main__':
    client.run(TOKEN)
