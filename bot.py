import os
import random
import time
import datetime
import traceback

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


@client.event
async def on_member_join(member):
    guild = discord.utils.get(client.guilds, name=SERVER)
    general_channel = discord.utils.get(guild.channels, name="welcoming")
    hello_messages = ["Hello, sunshine! {}", "Howdy, partner! {}", "Hey, howdy, hi! {}", "Peek-a-boo! {}",
                      "Howdy-doody! {}", "Hey there, {}!", "I come in peace! {}", "Ahoy, matey! {}", "Hiya! {}",
                      "What’s crackin’? {}", "‘Ello, gov'nor! {}", "Here's {}. Say Hi!!", "Yo! {}", "Aloha! {}",
                      "At least, we meet for the first time for the last time! {}", "Hola! {}", "Que Pasa! {}",
                      "Bonjour! {}", "Hallo! {}", "Ciao! {}", "Konnichiwa! {}"]
    welcome_message = random.choice(hello_messages).format(member.mention)
    await general_channel.send(welcome_message)


@client.event
async def on_message(message):
    random.seed(time.time())
    if message.author == client.user:
        return
    if message.channel.name == "roles":
        if message.content == "list roles":
            await message.channel.send('\n'.join([role.name for role in message.guild.roles]))
        elif message.content.split(' ')[0] == "setrole":
            if message.author.top_role.name == "Admin":
                await message.mentions[0].add_roles(message.role_mentions[0])
                await message.channel.send("{role} is now added to the user {user}".format(
                    role=message.role_mentions[0].mention,
                    user=message.mentions[0].mention
                ))
        elif message.content.split(' ')[0] == "addrole":
            if "Admin" in [role.name for role in message.author.roles]:
                if message.content.split(' ')[1] not in [role.name for role in message.guild.roles]:
                    await message.guild.create_role(name=message.content.split(' ')[1],
                                                    color=discord.Color.from_rgb(random.randrange(255),
                                                                                 random.randrange(255),
                                                                                 random.randrange(255)))
                    await message.channel.send("A new role {role} has been added by {user}".format(
                        role=discord.utils.get(message.guild.roles, name=message.content.split(' ')[1]),
                        user=message.author.mention
                    ))
                else:
                    await message.channel.send(
                        "I am unable to add {rolename} as a role because it already exists as {role}".format(
                            rolename=message.content.split(' ')[1],
                            role=discord.utils.get(message.guild.roles, name=message.content.split(' ')[1]).mention
                        ))
        elif message.content.split(' ')[0] == "delrole":
            if "Admin" in [role.name for role in message.author.roles]:
                await message.role_mentions[0].delete()
                await message.channel.send("{role} does not exist anymore. It has been deleted by {user}".format(
                    role=message.role_mentions[0].mention,
                    user=message.author.mention
                ))
        elif message.content.split(' ')[0] == "getrole":
            admin_users = filter(
                lambda user: "Admin" in [role.name for role in user.roles],
                [user for user in message.guild.members]
            )
            for admin in admin_users:
                if admin.dm_channel is None:
                    await admin.create_dm()
                await admin.dm_channel.send(
                    "There is a new {role} role request for user {user}. Please check roles channel of {guild}.".format(
                        role=message.role_mentions[0].name,
                        user=message.author.mention,
                        guild=message.guild
                    ))


@client.event
async def on_error(event, *args, **kwargs):
    embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c)
    embed.add_field(name='Event', value=event)
    embed.description = '```py\n%s\n```' % traceback.format_exc()
    embed.timestamp = datetime.datetime.utcnow()
    channel = discord.utils.get(discord.utils.get(client.guilds, name=SERVER).channels, name="manager-bot-error-logs")
    await channel.send(embed=embed)

if __name__ == '__main__':
    client.run(TOKEN)
