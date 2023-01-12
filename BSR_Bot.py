import discord, os, time, asyncio, random, json, requests, textwrap, datetime, sys
from multiprocessing import Process
from colorama import Fore, Back, Style
from flask import Flask, send_file
from bs4 import BeautifulSoup
from discord.ext import commands, tasks



embed_color = 0xff0000
intents = discord.Intents().default()
intents.members = True
token = "[TOKEN]"
server_ID = 876927143295213609
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.command(name="converter", aliases=["cv", "convert"], pass_context=True)
async def converter(ctx, url, format):

    await ctx.channel.purge(limit=99)
    embed = discord.Embed(title="**⚙️Konwerter url do mp3/mp4⚙️**", description="**Jak używać: {Komenda} {URL} {Format}**", color=embed_color)
    embed.add_field(name="Komenda", value="!convert / !cv", inline=False)
    embed.add_field(name="URL", value="adres URL filmu", inline=False)
    embed.add_field(name="Format", value="format pliku wyjściowego\nmp3/360/480/720/1080/1440", inline=False)
    embed.add_field(name="Wspierane", value="YouTube Vimeo SoundCloud FaceBook Twitch Twitter TikTok\n\nczasem coś się buguje i trzeba drugi raz wysłać😉", inline=False)
    message = await ctx.channel.send(embed=embed)

    if format == "mp3":
        file_type = "mp3"
    else:
        file_type = "mp4"

    print(f"{Fore.YELLOW}Converting {url} to {file_type}{Style.RESET_ALL}")

    session = requests.Session()
    headers = {
        'authority': 'loader.to',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="92", "Opera GX";v="78"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.186',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://loader.to/pl17/youtube-mp4-downloader.html',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '',
    }
    params = {
    'format': format,
    'url': url,
}

    response = session.get('https://loader.to/ajax/download.php', headers=headers, params=params)
    response_text = json.loads(response.text)
    params = (('id', response_text["id"]),)

    embed = discord.Embed(title="**⚙️Konwertowanie⚙️**", description=str(url) + " na " + str(file_type) + "\n\n" + "**--" + "%**", color=embed_color)
    message = await ctx.send(embed=embed)

    while True:
        time.sleep(1)
        response = session.get("https://loader.to/ajax/progress.php", headers=headers, params=params)
        response_text = json.loads(response.text)
        embed = discord.Embed(title="**⚙️Konwertowanie⚙️**", description=str(url) + " na " + str(file_type) + "\n\n**" + "1/2   " + str(int(response_text["progress"])/10) + "%**", color=embed_color)
        await message.edit(embed=embed)

        if response_text["success"] == 1:
            embed = discord.Embed(title="**⚙️Konwertowanie⚙️**", description=str(url) + " na " + str(file_type) + "\n\n" + "2/2   " + "**n/a%**", color=embed_color)
            await message.edit(embed=embed)
            break
    
    try:
        os.system(f"rm converted.mp3")
        os.system(f"rm converted.mp4")
    except:
        pass
    os.system(f"wget -O converted.{file_type} {response_text['download_url']}")
    
    port = 63522
    ip = "193.39.71.15"

    embed = discord.Embed(title="**⚙️Konwertowanie⚙️**", description=str(url) + " na " + str(file_type) + "\n\n" + f"[**Download**](http://{ip}:{port}/{file_type})", color=embed_color)
    await message.edit(embed=embed)
    print(f"{Fore.GREEN}Converted {url} to {file_type}{Style.RESET_ALL}")


@bot.command(name="ping",pass_context=True)
async def ping(ctx):
    ping = round(bot.latency * 1000)
    if ping < 200:
        print(Fore.GREEN + "ping", str(ping))
        color = 0x00ff00
    elif ping < 500:
        print(Fore.YELLOW + "ping", str(ping))
        color = 0xffff00
    else:
        print(Fore.RED + "ping", str(ping))
        color = 0xff0000
    try:
        await ctx.message.delete()
    except:
        pass
    embed = discord.Embed(title="BSR_Bot is active", description=f"Server to Discord ping: {ping}ms", color=color)
    await ctx.send(embed=embed, delete_after=10)


@bot.command(name="mclear",pass_context=True)
async def clear(ctx, number=1):
        print("clearing function")
        for role in ctx.message.author.roles:
            if role.name == "Moderator" or role.name == "Admin":
                await ctx.channel.purge(limit=number+1)


@bot.event
async def on_reaction_add(reaction, user):
    guild = bot.get_guild(876927143295213609)
    Uczen = discord.utils.get(guild.roles, name="BSR-uczeń")
    channel = bot.get_channel(876934729507696690)
    msg_id = channel.last_message.id
    if msg_id != None:
        if user != bot.user:
            if reaction.message.id == msg_id:
                for role in user.roles:
                    if role.name in ["Absolwent", "Palindrom", "*****", "Vidoc", "Proszę bez brawa", "Armagoudon", "Kontrabanda", "Dobre Pytanie", "Concordia", "Znam Skrót", "Terrafelix", "Axolotl", "To Się Może Podobać", "Gość"]:
                        print(Fore.BLUE + user.name + Fore.RESET, "has role", Fore.BLUE + role.name + Fore.RESET)
                        return
                if reaction.emoji == "🍒":
                    Role = discord.utils.get(guild.roles, name="Absolwent")
                    await user.add_roles(Role)
                    await user.add_roles(Uczen)
                if reaction.emoji == "🍓":
                    Role = discord.utils.get(guild.roles, name="Armagoudon")
                    await user.add_roles(Role)
                    Role = discord.utils.get(guild.roles, name="Palindrom")
                    await user.add_roles(Role)
                    await user.add_roles(Uczen)
                if reaction.emoji == "🍋":
                    Role = discord.utils.get(guild.roles, name="Kontrabanda")
                    await user.add_roles(Role)
                    Role = discord.utils.get(guild.roles, name="Palindrom")
                    await user.add_roles(Role)
                    await user.add_roles(Uczen)
                if reaction.emoji == "🍎":
                    Role = discord.utils.get(guild.roles, name="Dobre Pytanie")
                    await user.add_roles(Role)
                    Role = discord.utils.get(guild.roles, name="*****")
                    await user.add_roles(Role)
                    await user.add_roles(Uczen)
                if reaction.emoji == "🍉":
                    Role = discord.utils.get(guild.roles, name="Concordia")
                    await user.add_roles(Role)
                    Role = discord.utils.get(guild.roles, name="*****")
                    await user.add_roles(Role)
                    await user.add_roles(Uczen)
                if reaction.emoji == "🍊":
                    Role = discord.utils.get(guild.roles, name="Znam Skrót")
                    await user.add_roles(Role)
                    Role = discord.utils.get(guild.roles, name="Vidoc")
                    await user.add_roles(Role)
                    await user.add_roles(Uczen)
                if reaction.emoji == "🍍":
                    Role = discord.utils.get(guild.roles, name="Terrafelix")
                    await user.add_roles(Role)
                    Role = discord.utils.get(guild.roles, name="Vidoc")
                    await user.add_roles(Role)
                    await user.add_roles(Uczen)
                if reaction.emoji == "🍌":
                    Role = discord.utils.get(guild.roles, name="Axolotl")
                    await user.add_roles(Role)
                    Role = discord.utils.get(guild.roles, name="Proszę bez brawa")
                    await user.add_roles(Role)
                    await user.add_roles(Uczen)
                if reaction.emoji == "🍇":
                    Role = discord.utils.get(guild.roles, name="To Się Może Podobać")
                    await user.add_roles(Role)
                    Role = discord.utils.get(guild.roles, name="Proszę bez brawa")
                    await user.add_roles(Role)
                    await user.add_roles(Uczen)
                if reaction.emoji == "🥝":
                    Role = discord.utils.get(guild.roles, name="Gość")
                    await user.add_roles(Role)



@bot.event
async def on_ready():
    channel_role = bot.get_channel(876934729507696690)
    channel_converter = bot.get_channel(887456542448840745)
    channel_regulamin = bot.get_channel(876934758188326922)

    await channel_regulamin.purge(limit=99)
    embed = discord.Embed(title="**📄️Regulamin📄️**", color=embed_color)
    embed.add_field(name="\u200b", value="•    Zakaz wysyłania linków/plików zawierających serwisy/oprogramowanie działające na szkodę użytkownika.", inline=False)
    embed.add_field(name="\u200b", value="•    Zakaz udostępniania zdjęć i danych osobowych osób które nie wyraziły na to zgody.", inline=False)
    # embed.add_field(name="\u200b", value="•    Zakaz publikowania treści pornograficznych oraz brutalnych.", inline=False)
    embed.add_field(name="\u200b", value="•    Pisz na kanałach przeznaczonych do tematu o którym piszesz.", inline=False)
    embed.add_field(name="\u200b", value="•    Nie znajomość regulaminu nie zwalnia z przestrzegania go.", inline=False)
    embed.add_field(name="\u200b", value="•    Jeżeli chesz kogoś zaprosić na serwer użyj tego linku: https://discord.gg/H3YEyGWjzG", inline=False)
    embed.add_field(name="\u200b", value="•    W razie wątpliwości skonsultuj się z adminem/modem.", inline=False)
    msg = await channel_regulamin.send(embed=embed)

    await channel_converter.purge(limit=99)
    embed = discord.Embed(title="**⚙️Konwerter url do mp3/mp4⚙️**", description="**Jak używać: {Komenda} {URL} {Format}**", color=embed_color)
    embed.add_field(name="Komenda", value="!convert / !cv", inline=False)
    embed.add_field(name="URL", value="adres URL filmu", inline=False)
    embed.add_field(name="Format", value="format pliku wyjściowego\nmp3/360/480/720/1080/1440", inline=False)
    embed.add_field(name="Wspierane", value="YouTube Vimeo SoundCloud FaceBook Twitch Twitter TikTok\n\nczasem coś się buguje i trzeba drugi raz wysłać😉", inline=False)
    message = await channel_converter.send(embed=embed)

    await channel_role.purge(limit=99)
    embed = discord.Embed(title="**Wybierz swoją klasę**", description="**Jeśli nie chodzisz do BSR to wybierz 🥝(Gość)/🍒(Absolwent)**\n-", color=embed_color)
    embed.add_field(name="🍒 -> Absolwent", value="-", inline=False)
    embed.add_field(name="🍓 -> Armagoudon", value="-", inline=False)
    embed.add_field(name="🍋 -> Kontrabanda", value="-", inline=False)
    embed.add_field(name="🍎 -> Dobre pytanie", value="-", inline=False)
    embed.add_field(name="🍉 -> Concordia", value="-", inline=False)
    embed.add_field(name="🍊 -> Znam skrót", value="-", inline=False)
    embed.add_field(name="🍍 -> Terrafelix", value="-", inline=False)
    embed.add_field(name="🍌 -> Axolotl", value="-", inline=False)
    embed.add_field(name="🍇 -> To Się Może Podobać", value="-", inline=False)
    embed.add_field(name="🥝 -> Gość", value="-", inline=False)
    msg = await channel_role.send(embed=embed)
    for i in ["🍒", "🍓", "🍋", "🍎", "🍉", "🍊", "🍍", "🍌", "🍇", "🥝"]:
        await msg.add_reaction(i)
        
    print(Fore.BLUE + "BSR_Bot is active" + Fore.RESET)


@bot.event
async def on_message(message):
    if not message.guild:
        target_channel = bot.get_channel(877731629546737724)
        print("got DM from", message.author)
        open("DMs_log.txt", "a").write(f"{message.author}: {message.content}\n")

        attachments = message.attachments
        msg_attachments = ""
        for attachment in attachments:
            msg_attachments = msg_attachments + "\n" + str(attachment.url)

        await target_channel.send(str(message.content + msg_attachments))
    await bot.process_commands(message)


@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    if before.channel is not None:
        if before.channel.name != "Stwórz kanał głosowy":
            if len(before.channel.members) == 0:
                await before.channel.delete()

    if after.channel is not None:
        if after.channel.name == "Stwórz kanał głosowy":
            guild = bot.get_guild(server_ID)
            channel = await guild.create_voice_channel(name=member.name, category=after.channel.category)
            await channel.set_permissions(member, connect=True, move_members=True, mute_members=True, deafen_members=True, manage_channels=True)
            if channel is not None:
                return await member.move_to(channel)


bot.run(token)