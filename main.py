import discord
import os
import csv

token = os.environ["DOOTDOOT_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged on as {client.user}")

@client.event
async def on_message(message):
    if (message.content.startswith("/swear")
            and message.author.id != client.user.id
            and len(message.mentions) > 0):
        message_split = message.content.split(" ")
        print(message_split)
        swear_num = 1
        if len(message_split) > 2:
            try: #if the message cant be converted to int send message and exit
                swear_num = int(message_split[2])
            except (TypeError, ValueError):
                author_str = "<@" + str(message.author.id) + ">"
                await message.channel.send(author_str + " YOU FOOL! YOU GOOF! AHAHAHHA THATS NOT A NUMBER AHAHAHHAHAHAHHAH ")
                return
        with open ("swear_jar.csv", "a", newline="") as swear_jar:
            csv_writer = csv.writer(swear_jar, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([message.author.id ,message.mentions[0].id, swear_num])
        user_str = "<@" + str(message.mentions[0].id) + ">"
        await message.channel.send(user_str + " NO SWEARING IN MY CHRISTIAN MINECRAFT SERVER!!! D:<<<")
    elif message.content.startswith("/swearjar"):
        with open ("swear_jar.csv", "r", newline="") as swear_jar:
            csv_reader = csv.reader(swear_jar, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            swearers = {}
            for row in csv_reader:
                member_id = int(row[1])
                if member_id not in swearers:
                    swearers[member_id] = int(row[2])
                else:
                    swearers[member_id] += int(row[2])
            swearers = {k: v for k, v in sorted(swearers.items(), key=lambda x: x[1])} # sorts dict
            leaderboards_message = ""
            for (key, val) in swearers.items():
                leaderboards_message += f"<@{key}>: {val}\n"
            await message.channel.send(leaderboards_message, silent=True)
    elif (message.content.startswith("/swear")):
        await message.channel.send("usage: /swear @name [number of infractions]")


client.run(token)
